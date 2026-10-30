"""Divide cada versión estenográfica de la LXV en turnos de palabra y asigna
a cada turno la sección de la sesión donde ocurrió (iniciativas, dictámenes,
efemérides, etc.) y el partido del orador.

Salida: datos/turnos_secciones.csv, un renglón por turno.
No usa temas ni fechas de emisiones: solo describe dónde y cuánto habla cada partido.
"""
import html
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]

PARTIDOS = {"MORENA": "MORENA", "PAN": "PAN", "PRI": "PRI", "PRD": "PRD", "PT": "PT",
            "PVEM": "PVEM", "PMC": "MC", "MC": "MC", "PES": "PES"}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", " ", re.sub(r"\s+", " ", s)).strip()


def limpiar(fragmento):
    s = re.sub(r"<br\s*/?>", " ", fragmento, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def categoria(encabezado, actual):
    """Traduce un encabezado del sumario a una categoría de sección.
    Si el encabezado no es de categoría (p. ej. el título de un dictamen),
    se conserva la categoría vigente."""
    h = norm(encabezado)
    reglas = [
        ("efemeride", r"^efemer|^con motivo"),
        ("agenda_politica", r"^agenda politica"),
        ("proposiciones", r"^proposicion"),
        ("intervenciones", r"^intervenciones"),
        ("iniciativas", r"^iniciativas$|ronda de iniciativas"),
        ("dictamenes", r"^dictamen|^minuta|^declaratoria de publicidad|dispensa de tramites"),
        ("comparecencia_informe", r"^comparecencia|^analisis del|ronda de preguntas"),
        ("posicionamientos", r"^posicionamiento|^poscionamiento"),
        ("acuerdos", r"^acuerdos?"),
        ("comunicaciones", r"^comunicacion"),
    ]
    for cat, patron in reglas:
        if re.search(patron, h):
            return cat
    return actual


def leer_sumario(t, fin):
    """Regresa {ancla: (categoria, etiqueta)} y {nombre normalizado: partido}."""
    anclas, partidos = {}, {}
    cat = "apertura"
    for p in re.findall(r"<p[^>]*>(.*?)</p>", t[:fin], flags=re.S):
        texto = limpiar(p)
        if not texto:
            continue
        hrefs = re.findall(r'href="#([^"]+)"', p)
        nueva = categoria(texto, None)
        if nueva:
            cat = nueva
        for h in hrefs:
            anclas[h] = (cat, texto)
        m = re.match(r"(.+),\s*([A-Za-z]+)$", texto)
        if hrefs and m and m.group(2).upper() in PARTIDOS:
            partidos[norm(m.group(1))] = PARTIDOS[m.group(2).upper()]
    return anclas, partidos


ORADOR = re.compile(r"^(El|La|Los|Las)\s+(.{0,120}?)(\s*\((?:desde la curul|desde su curul)\))?\s*:")


def turnos_de_sesion(archivo):
    t = open(f"{RAIZ}/{archivo}", "rb").read().decode("latin-1")
    inicio_cuerpo = t.find("<a name=")
    anclas, partidos_sumario = leer_sumario(t, inicio_cuerpo)
    cuerpo = t[inicio_cuerpo:]
    cat_actual, etiqueta = "apertura", ""
    turnos, turno = [], None
    # Cada párrafo; las anclas cambian la sección vigente.
    for p in re.findall(r"<p[^>]*>(.*?)</p>", cuerpo, flags=re.S):
        for a in re.findall(r'<a name="([^"]+)"', p):
            if a in anclas:
                cat_actual, etiqueta = anclas[a]
        texto = limpiar(p)
        if not texto:
            continue
        m = ORADOR.match(re.sub(r"\s+\(", " (", texto))
        if m and len(m.group(2).split()) <= 12:
            cabeza = m.group(1) + " " + m.group(2)
            turno = {"rol": cabeza, "desde_curul": bool(m.group(3)), "seccion": cat_actual,
                     "etiqueta": etiqueta, "texto": texto[m.end():].strip()}
            turnos.append(turno)
        elif turno is not None:
            turno["texto"] += " " + texto
    return turnos, partidos_sumario


def rol_y_nombre(cabeza):
    c = norm(cabeza)
    if re.search(r"\bpresident|\bsecretari|vicepresident", c):
        return "mesa", None
    m = re.match(r"(el|la) (diputado|diputada) (.+)", c)
    if m:
        return "diputado", m.group(3).strip()
    return "otro", None


def main():
    cal = pd.read_csv(f"{RAIZ}/datos/calendario_sesiones.csv")
    lxv = cal[(cal.legislatura == 65) & (cal.tipo == "ordinaria")]
    fichas = pd.read_csv(f"{RAIZ}/datos/fichas_diputados.csv")
    fichas = fichas[fichas.legislatura == "LXV"]
    mapa = {norm(n): PARTIDOS.get(str(p).upper(), str(p).upper()) for n, p in zip(fichas.nombre, fichas.partido)}

    crudos = []
    for _, s in lxv.iterrows():
        turnos, part = turnos_de_sesion(s.archivo)
        mapa.update(part)
        for t in turnos:
            t.update(fecha=s.fecha, archivo=s.archivo, sufijo=s.sufijo)
            crudos.append(t)

    # Asignación de partido por nombre; si no hay coincidencia exacta,
    # se busca un nombre del mapa contenido en el del orador o viceversa.
    claves = list(mapa)
    filas, sin_partido = [], Counter()
    for t in crudos:
        rol, nombre = rol_y_nombre(t["rol"])
        partido = None
        if rol == "diputado":
            partido = mapa.get(nombre)
            if partido is None:
                tokens = set(nombre.split())
                mejor = max(claves, key=lambda k: len(tokens & set(k.split())))
                if len(tokens & set(mejor.split())) >= 3 or (len(tokens) == 2 and tokens <= set(mejor.split())):
                    partido = mapa[mejor]
            if partido is None:
                sin_partido[nombre] += 1
        filas.append({"fecha": t["fecha"], "sufijo": t["sufijo"], "seccion": t["seccion"],
                      "etiqueta": t["etiqueta"][:120], "rol": rol, "orador": nombre or t["rol"],
                      "partido": partido, "desde_curul": t["desde_curul"],
                      "palabras": len(t["texto"].split()), "texto": t["texto"]})
    df = pd.DataFrame(filas)
    df.to_csv(f"{RAIZ}/datos/turnos_secciones.csv", index=False)
    dip = df[df.rol == "diputado"]
    print(f"{len(lxv)} sesiones, {len(df)} turnos, {len(dip)} de diputados")
    print(f"palabras de diputados sin partido: {dip[dip.partido.isna()].palabras.sum() / dip.palabras.sum():.1%}")
    print("oradores sin partido más frecuentes:", sin_partido.most_common(10))


if __name__ == "__main__":
    main()
