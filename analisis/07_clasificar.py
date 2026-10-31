"""Clasifica por tema los textos que juntó 06_textos_a_clasificar.py.

Dos tareas:
  seccion    Cada emisión de "Quién es quién en las mentiras": el modelo divide la
             sección en ítems (desmentidos) y a cada uno le asigna tema y blanco.
  diputados  Cada intervención libre de los diputados: un tema. El modelo no ve ni
             el partido ni la fecha, igual que nosotros al codificar a mano.

El modelo, las instrucciones (libro_de_codigos.md) y cada respuesta completa quedan
guardados, para que la clasificación se pueda revisar y repetir. Ya no se puede fijar
la temperatura: la API la rechaza desde octubre de 2026.

Cada corrida cuesta dinero. Por eso:
  --estimar   no llama al modelo: cuenta textos y estima el costo.
  --piloto    solo textos fuera de la muestra (emisiones que no entran a las 64 y
              sesiones que no están en ninguna ventana).
  --solo N    solo los primeros N textos pendientes.
Las respuestas se guardan conforme llegan; si la corrida se corta, al volver a
correrla solo pide lo que falta.

Requiere credenciales de la API de Claude (ANTHROPIC_API_KEY o `ant auth login`).

Sin API, la clasificación la hacen subagentes de Claude Code, por lotes:
  --lotes      parte los textos pendientes en lotes (datos/clasificar/lotes/) que solo
               traen el identificador y el texto. --tam fija el tamaño del lote y
               --repetir cuántos textos se repiten en otro lote, para medir consistencia.
  --importar   lee lo que escribieron los subagentes (datos/clasificar/salidas/), lo
               revisa, mide la consistencia de los repetidos y exporta la tabla.

Uso: python 07_clasificar.py seccion|diputados [--estimar] [--piloto] [--solo N]
     python 07_clasificar.py seccion|diputados --lotes [--piloto] [--solo N] [--tam N] [--repetir N]
     python 07_clasificar.py seccion|diputados --importar
"""
import argparse
import hashlib
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from importlib import import_module
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
CARPETA = RAIZ / "datos" / "clasificar"
LOTES = CARPETA / "lotes"
SALIDAS = CARPETA / "salidas"
MODELO = "claude-opus-5-5"
ESFUERZO = "low"
# Precios de claude-opus-5-5 por millón de tokens (octubre de 2026), solo para --estimar.
PRECIO_ENTRADA, PRECIO_SALIDA = 4.00, 20.00
HILOS = 8

LIBRO = (Path(__file__).parent / "libro_de_codigos.md").read_text(encoding="utf-8")
CODIGOS = sorted({int(c) for c in re.findall(r"^- \*\*(\d+) ", LIBRO, re.M)})
VERSION_LIBRO = hashlib.sha256(LIBRO.encode()).hexdigest()[:12]

INSTRUCCIONES = {
    "diputados": (
        "Eres un codificador de un proyecto de investigación sobre la agenda del Congreso "
        "mexicano. Vas a recibir una intervención de un diputado en el Pleno de la Cámara de "
        "Diputados (2021-2024). Asígnale un solo tema siguiendo el libro de códigos de abajo. "
        "Responde solo con el número del tema.\n\n" + LIBRO
    ),
    "seccion": (
        "Eres un codificador de un proyecto de investigación sobre la agenda del Congreso "
        "mexicano. Vas a recibir la transcripción de la sección \"Quién es quién en las "
        "mentiras de la semana\" de una conferencia matutina del Presidente, dividida en "
        "turnos numerados. La sección desmiente varias notas, una tras otra. Divídela en "
        "ítems: cada ítem es un desmentido, y ocupa uno o varios turnos seguidos. Deja fuera "
        "los turnos de saludo, presentación y despedida. Para cada ítem da el primer y el "
        "último turno, un resumen de una línea, el tema según el libro de códigos de abajo y "
        "el blanco (a quién desmiente).\n\n" + LIBRO
    ),
}

ESQUEMAS = {
    "diputados": {
        "type": "object",
        "properties": {"tema": {"type": "integer", "enum": CODIGOS}},
        "required": ["tema"],
        "additionalProperties": False,
    },
    "seccion": {
        "type": "object",
        "properties": {"items": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "turno_inicio": {"type": "integer"},
                "turno_fin": {"type": "integer"},
                "resumen": {"type": "string"},
                "tema": {"type": "integer", "enum": CODIGOS},
                "blanco": {"type": "string", "enum": ["medio", "oposicion", "otro"]},
            },
            "required": ["turno_inicio", "turno_fin", "resumen", "tema", "blanco"],
            "additionalProperties": False,
        }}},
        "required": ["items"],
        "additionalProperties": False,
    },
}
MAX_TOKENS = {"diputados": 4000, "seccion": 16000}


def fuera_de_muestra():
    """Emisiones y sesiones que no entran al análisis: sirven para el piloto."""
    sys.path.insert(0, str(Path(__file__).parent))
    vm = import_module("02_ventanas_y_volumen")
    v = vm.ventanas(vm.sesiones_lxv(), mismo_dia_es_post=False)
    return set(v.emision), set(v.sesion)


def textos(tarea, piloto):
    """Lista de (id, texto) por clasificar."""
    if tarea == "diputados":
        d = pd.read_csv(CARPETA / "intervenciones.csv")
        d = d[~d.corta]
        if piloto:
            d = d[~d.sesion.isin(fuera_de_muestra()[1])]
        return [(r.id, f"Intervención:\n\n{r.texto}") for r in d.itertuples()]
    s = pd.read_csv(CARPETA / "seccion_turnos.csv")
    if piloto:
        s = s[~s.emision.isin(fuera_de_muestra()[0])]
    salida = []
    for e, g in s.groupby("emision"):
        turnos = "\n\n".join(f"[{r.turno}] {r.texto}" for r in g.itertuples())
        salida.append((e, f"Sección del {e}:\n\n{turnos}"))
    return salida


def archivo(tarea):
    return CARPETA / f"respuestas_{tarea}.jsonl"


def hechos(tarea):
    if not archivo(tarea).exists():
        return set()
    with open(archivo(tarea), encoding="utf-8") as f:
        return {json.loads(l)["id"] for l in f if json.loads(l).get("ok")}


def clasificar_uno(client, tarea, ident, texto):
    r = client.beta.messages.create(
        model=MODELO,
        max_tokens=MAX_TOKENS[tarea],
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={"effort": ESFUERZO,
                       "format": {"type": "json_schema", "schema": ESQUEMAS[tarea]}},
        system=[{"type": "text", "text": INSTRUCCIONES[tarea], "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": texto}],
    )
    fila = {"id": ident, "modelo_pedido": MODELO, "modelo": r.model, "esfuerzo": ESFUERZO,
            "libro": VERSION_LIBRO, "fecha": datetime.now(timezone.utc).isoformat(),
            "stop_reason": r.stop_reason, "uso": r.usage.to_dict(), "ok": False}
    if r.stop_reason == "end_turn":
        texto_resp = next(b.text for b in r.content if b.type == "text")
        fila.update(ok=True, respuesta=json.loads(texto_resp))
    return fila


def correr(tarea, pendientes):
    import anthropic

    client = anthropic.Anthropic(max_retries=5)
    candado = threading.Lock()
    errores = 0
    with ThreadPoolExecutor(HILOS) as pool, open(archivo(tarea), "a", encoding="utf-8") as f:
        futuros = {pool.submit(clasificar_uno, client, tarea, i, t): i for i, t in pendientes}
        for n, fut in enumerate(as_completed(futuros), 1):
            try:
                fila = fut.result()
            except (anthropic.APIStatusError, anthropic.APIConnectionError, json.JSONDecodeError) as err:
                fila = {"id": futuros[fut], "ok": False, "error": repr(err)}
            errores += not fila["ok"]
            with candado:
                f.write(json.dumps(fila, ensure_ascii=False) + "\n")
                f.flush()
            if n % 50 == 0 or n == len(futuros):
                print(f"  {n}/{len(futuros)} ({errores} con problema)", flush=True)
    return errores


def exportar(tarea):
    """Convierte las respuestas en una tabla limpia."""
    with open(archivo(tarea), encoding="utf-8") as f:
        filas = [json.loads(l) for l in f]
    # La última respuesta buena de cada id; las repeticiones solo sirven para medir consistencia.
    ok = {r["id"]: r for r in filas if r.get("ok") and not r.get("repeticion")}
    if tarea == "diputados":
        d = pd.read_csv(CARPETA / "intervenciones.csv")
        d["tema"] = d.id.map(lambda i: ok[i]["respuesta"]["tema"] if i in ok else None)
        d.loc[d.corta, "tema"] = 0
        d.drop(columns="texto").to_csv(CARPETA / "temas_intervenciones.csv", index=False)
        print(f"temas_intervenciones.csv: {d.tema.notna().sum()} de {len(d)} con tema")
        return
    s = pd.read_csv(CARPETA / "seccion_turnos.csv")
    items = []
    for e, r in ok.items():
        g = s[s.emision == e].set_index("turno").palabras
        for k, it in enumerate(r["respuesta"]["items"], 1):
            palabras = int(g.loc[it["turno_inicio"]:it["turno_fin"]].sum())
            items.append({"emision": e, "item": k, **it, "palabras": palabras})
    pd.DataFrame(items).to_csv(CARPETA / "temas_seccion.csv", index=False)
    print(f"temas_seccion.csv: {len(items)} ítems de {len(ok)} emisiones")


def hacer_lotes(tarea, pendientes, tam, repetir, solo=None):
    """Escribe los lotes para los subagentes. Cada texto va con su identificador y nada más."""
    rng = __import__("numpy").random.default_rng(20261031)
    # Se barajan antes de cortar, para que un piloto con --solo no salga todo de las mismas fechas.
    orden = [pendientes[i] for i in rng.permutation(len(pendientes))][:solo]
    lotes = [orden[i:i + tam] for i in range(0, len(orden), tam)]
    indice = [(f"{tarea}_{k:03d}", i, False) for k, lote in enumerate(lotes, 1) for i, _ in lote]
    # Algunos textos se repiten en otro lote, al final, para ver si salen igual.
    if repetir and len(lotes) > 1:
        for j in rng.choice(len(orden), min(repetir, len(orden)), replace=False):
            propio = j // tam
            otro = rng.choice([k for k in range(len(lotes)) if k != propio])
            lotes[otro].append(orden[j])
            indice.append((f"{tarea}_{otro + 1:03d}", orden[j][0], True))
    LOTES.mkdir(parents=True, exist_ok=True)
    for k, lote in enumerate(lotes, 1):
        cuerpo = "\n\n".join(f"### {i}\n{t.split(chr(10), 2)[-1]}" for i, t in lote)
        (LOTES / f"{tarea}_{k:03d}.txt").write_text(cuerpo + "\n", encoding="utf-8")
    pd.DataFrame(indice, columns=["lote", "id", "repeticion"]).to_csv(LOTES / f"indice_{tarea}.csv", index=False)
    print(f"  {len(lotes)} lotes en {LOTES.relative_to(RAIZ)} ({len(indice)} textos, "
          f"{sum(r for *_, r in indice)} repetidos)")


def revisar(tarea, ident, resp, turnos):
    """Problemas en una respuesta de subagente; lista vacía si está bien."""
    if tarea == "diputados":
        return [] if resp.get("tema") in CODIGOS else [f"tema inválido: {resp.get('tema')}"]
    malos = []
    for it in resp.get("items", []):
        if it.get("tema") not in CODIGOS or it.get("blanco") not in ("medio", "oposicion", "otro"):
            malos.append(f"tema o blanco inválido: {it}")
        elif not 1 <= it["turno_inicio"] <= it["turno_fin"] <= turnos.get(ident, 0):
            malos.append(f"turnos fuera de rango: {it['turno_inicio']}-{it['turno_fin']}")
    return malos if resp.get("items") else ["sin ítems"]


def importar(tarea):
    indice = pd.read_csv(LOTES / f"indice_{tarea}.csv")
    turnos = pd.read_csv(CARPETA / "seccion_turnos.csv").groupby("emision").turno.max().to_dict()
    filas, problemas = [], []
    for lote, g in indice.groupby("lote"):
        f = SALIDAS / f"{lote}.jsonl"
        if not f.exists():
            problemas.append(f"{lote}: falta la salida")
            continue
        resp = {}
        for n, linea in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if linea.strip():
                try:
                    r = json.loads(linea)
                    resp[str(r.pop("id"))] = r
                except (json.JSONDecodeError, KeyError):
                    problemas.append(f"{lote}, línea {n}: no es JSON válido")
        for r in g.itertuples():
            if r.id not in resp:
                problemas.append(f"{lote}: falta {r.id}")
                continue
            malos = revisar(tarea, r.id, resp[r.id], turnos)
            problemas += [f"{lote}, {r.id}: {m}" for m in malos]
            filas.append({"id": r.id, "modelo": f"{MODELO} (subagente de Claude Code)", "lote": lote,
                          "libro": VERSION_LIBRO, "repeticion": bool(r.repeticion),
                          "ok": not malos, "respuesta": resp[r.id]})
    with open(archivo(tarea), "w", encoding="utf-8") as f:
        f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in filas)
    print(f"{len(filas)} respuestas importadas; {len(problemas)} problemas")
    for p in problemas[:20]:
        print("  ", p)
    consistencia(tarea, [x for x in filas if x["ok"]])
    exportar(tarea)


def temas_tocados(resp, palabras):
    """Temas de una sección, con sus palabras; así se compara entre dos clasificaciones."""
    out = {}
    for it in resp["items"]:
        out[it["tema"]] = out.get(it["tema"], 0) + int(palabras.loc[it["turno_inicio"]:it["turno_fin"]].sum())
    return out


def consistencia(tarea, filas):
    por_id = {}
    for x in filas:
        por_id.setdefault(x["id"], []).append(x)
    pares = [(v[0]["respuesta"], v[1]["respuesta"]) for v in por_id.values() if len(v) > 1]
    if not pares:
        return
    if tarea == "diputados":
        igual = sum(a["tema"] == b["tema"] for a, b in pares)
        print(f"Consistencia: {igual} de {len(pares)} intervenciones repetidas salieron con el mismo tema")
        return
    s = pd.read_csv(CARPETA / "seccion_turnos.csv")
    ids = [i for i, v in por_id.items() if len(v) > 1]
    for i, (a, b) in zip(ids, pares):
        pal = s[s.emision == i].set_index("turno").palabras
        print(f"Consistencia {i}: {len(a['items'])} contra {len(b['items'])} ítems; "
              f"temas {temas_tocados(a, pal)} contra {temas_tocados(b, pal)}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("tarea", choices=["seccion", "diputados"])
    p.add_argument("--estimar", action="store_true")
    p.add_argument("--piloto", action="store_true")
    p.add_argument("--solo", type=int)
    p.add_argument("--lotes", action="store_true")
    p.add_argument("--tam", type=int, default=80)
    p.add_argument("--repetir", type=int, default=0)
    p.add_argument("--importar", action="store_true")
    a = p.parse_args()
    if a.importar:
        importar(a.tarea)
        return

    todos = textos(a.tarea, a.piloto)
    listos = hechos(a.tarea)
    pendientes = [(i, t) for i, t in todos if i not in listos][: a.solo]
    print(f"{a.tarea}: {len(todos)} textos, {len(listos & {i for i, _ in todos})} ya clasificados, "
          f"{len(pendientes)} por pedir. Modelo {MODELO}, esfuerzo {ESFUERZO}, libro {VERSION_LIBRO}")

    if a.lotes:
        hacer_lotes(a.tarea, [(i, t) for i, t in todos if i not in listos], a.tam, a.repetir, a.solo)
        return
    if a.estimar:
        # Unos 3.5 caracteres por token en español. La salida incluye el razonamiento
        # del modelo, que no se puede apagar; las cifras son aproximadas.
        instr = len(INSTRUCCIONES[a.tarea]) / 3.5
        entrada = sum(len(t) for _, t in pendientes) / 3.5 + instr * len(pendientes)
        salida = len(pendientes) * (300 if a.tarea == "diputados" else 2500)
        costo = entrada / 1e6 * PRECIO_ENTRADA + salida / 1e6 * PRECIO_SALIDA
        print(f"  ~{entrada / 1e6:.1f} M tokens de entrada, ~{salida / 1e6:.2f} M de salida: "
              f"cerca de US${costo:.0f} (menos si las instrucciones quedan en caché)")
        return
    if pendientes:
        errores = correr(a.tarea, pendientes)
        if errores:
            print(f"  {errores} textos sin clasificar; vuelve a correr el script para reintentarlos")
    exportar(a.tarea)


if __name__ == "__main__":
    main()
