"""Estima el efecto de la sección sobre la agenda de cada bloque (metodología v3 y plan congelado).

Arma Y_ptse con las clasificaciones de 07, aplica la regla de tratados y controles, y
estima la doble diferencia por bloque:
    Y_ptse = β_O·Opos×Toc×Post + β_M·Morena×Toc×Post + α_pte + γ_pse + ε
con mínimos cuadrados ponderados por las palabras del partido en la sesión y errores
agrupados por emisión y por sesión.

Modos (en el orden del plan):
  prueba [n]        Datos simulados con un efecto conocido sobre las intervenciones reales
                    (sin temas reales). La tubería debe recuperar el efecto. No usa datos reales.
  descriptivos      Temas tratados por emisión, palabras por bloque y sesión, y los dos tipos
                    de ceros. No estima nada.
  placebo [n]       Datos reales con las fechas de emisión barajadas. Debe dar cerca de cero.
  principal         La especificación principal, una sola vez. Pide la etiqueta plan-congelado.
  robustez          Todas las variantes de "También reportamos" y el estudio de eventos.
  permutacion [n]   Valor p por permutación de fechas, como confirmación de los errores.

Los temas elegidos se leen de analisis/temas_elegidos.csv (columnas cap y tema; varios códigos
del CAP pueden ir al mismo tema si se juntaron). Para la robustez de 5 y 10 temas, de
temas_elegidos_5.csv y temas_elegidos_10.csv.

Cada corrida con datos reales queda en analisis/registro_corridas.csv, se reporte o no.

Uso: python 11_estimar.py prueba|descriptivos|placebo|principal|robustez|permutacion [n]
"""
import subprocess
import sys
from datetime import datetime
from importlib import import_module
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
vm = import_module("02_ventanas_y_volumen")

CLAS = RAIZ / "datos" / "clasificar"
RESULTADOS = AQUI / "resultados"
REGISTRO = AQUI / "registro_corridas.csv"
PARTIDOS = ["PAN", "PRI", "PRD", "MC", "MORENA"]
VCOV = {"CRV1": "emision+sesion"}
MIN_LARGAS = 150
SEMILLA = 20261107


# ---------------------------------------------------------------- datos

def emisiones_todas():
    """Todas las emisiones de la sección, en orden. La anterior y la siguiente de una
    emisión se buscan aquí, aunque caigan fuera de las 64 (por ejemplo, en un receso)."""
    return sorted(pd.read_csv(RAIZ / "datos" / "emisiones_quien_es_quien.csv").fecha)


def ventanas(mismo_dia_es_post=False):
    return vm.ventanas(vm.sesiones_lxv(), mismo_dia_es_post=mismo_dia_es_post)


def intervenciones():
    d = pd.read_csv(CLAS / "intervenciones.csv", usecols=["id", "sesion", "partido", "palabras", "corta"])
    return d[~d.corta].drop(columns="corta")


def leer_elegidos(n=None):
    f = AQUI / ("temas_elegidos.csv" if n is None else f"temas_elegidos_{n}.csv")
    if not f.exists():
        sys.exit(f"Falta {f.relative_to(RAIZ)}: primero se eligen los temas con la regla del plan.")
    t = pd.read_csv(f)
    return dict(zip(t.cap.astype(int), t.tema.astype(str)))


def etiqueta(cap, elegidos):
    return elegidos.get(int(cap), f"cap{int(cap)}")


def cargar_reales(elegidos):
    """Intervenciones con su tema y temas tocados por cada emisión, ya con las etiquetas
    del análisis: un tema elegido o 'capN' para los demás."""
    d = intervenciones()
    t = pd.read_csv(CLAS / "temas_intervenciones.csv")[["id", "tema"]].dropna()
    d = d.merge(t, on="id", how="left")
    sesiones = set(ventanas().sesion) | set(ventanas(True).sesion)
    falta = d.tema.isna() & d.sesion.isin(sesiones)
    if falta.any():
        print(f"Aviso: {falta.sum()} intervenciones de sesiones en ventanas sin clasificar; no entran.")
    d = d.dropna(subset=["tema"])
    d["tema"] = [etiqueta(c, elegidos) for c in d.tema]
    s = pd.read_csv(CLAS / "temas_seccion.csv")
    toc = {e: {etiqueta(c, elegidos) for c in g.tema} for e, g in s.groupby("emision")}
    # Solo importan las emisiones de la muestra y sus vecinas (la anterior y la siguiente).
    orden = emisiones_todas()
    muestra = set(ventanas().emision)
    vecinas = {orden[j] for i, e in enumerate(orden) if e in muestra for j in (i - 1, i, i + 1) if 0 <= j < len(orden)}
    faltan = sorted(e for e in vecinas if e not in toc)
    if faltan:
        print(f"Aviso: {len(faltan)} emisiones sin sección clasificada (cuentan como sin temas): "
              f"{', '.join(faltan[:6])}{'…' if len(faltan) > 6 else ''}")
    return d, toc


# ---------------------------------------------------------------- tratados, controles y base

def conjuntos(e, toc, orden, pos, elegidos, excluir_sig=True):
    """Regla del plan. Tratado: elegido, tocado por e y no por e-1. Control: elegido que no
    tocaron e-1, e ni e+1. Resto: los no elegidos que no tocaron e-1, e ni e+1."""
    t = lambda x: toc.get(x, set())
    i = pos[e]
    prev = t(orden[i - 1]) if i > 0 else set()
    sig = t(orden[i + 1]) if i + 1 < len(orden) else set()
    fuera = prev | t(e) | (sig if excluir_sig else set())
    return (t(e) & elegidos) - prev, elegidos - fuera, fuera


def armar(d, toc, v, elegidos, excluir_sig=True):
    elegidos = set(elegidos)
    orden = emisiones_todas()
    pos = {e: i for i, e in enumerate(orden)}
    otros = set(d.tema) - elegidos
    W = d.groupby(["sesion", "partido", "tema"]).palabras.sum()
    total = d.groupby(["sesion", "partido"]).palabras.sum().rename("total")
    filas = []
    for e, g in v.groupby("emision"):
        trat, ctrl, fuera = conjuntos(e, toc, orden, pos, elegidos, excluir_sig)
        resto = otros - fuera
        idx = pd.MultiIndex.from_product([g.sesion, PARTIDOS, sorted(trat | ctrl)],
                                         names=["sesion", "partido", "tema"])
        b = W.reindex(idx, fill_value=0).reset_index(name="W")
        r = d[d.sesion.isin(g.sesion) & d.tema.isin(resto)].groupby(["sesion", "partido"]).palabras.sum()
        r = r.reindex(pd.MultiIndex.from_product([g.sesion, PARTIDOS], names=["sesion", "partido"]),
                      fill_value=0).reset_index(name="W").assign(tema="resto")
        b = pd.concat([b, r], ignore_index=True).merge(g[["sesion", "k"]], on="sesion")
        b["emision"] = e
        b["toc"] = b.tema.isin(trat).astype(int)
        filas.append(b)
    b = pd.concat(filas, ignore_index=True)
    b = b.merge(total, left_on=["sesion", "partido"], right_index=True, how="left")
    b["total"] = b.total.fillna(0)
    b["opos"] = (b.partido != "MORENA").astype(int)
    b["post"] = (b.k > 0).astype(int)
    b["tp_o"] = b.opos * b.toc * b.post
    b["tp_m"] = (1 - b.opos) * b.toc * b.post
    b["tp"] = b.toc * b.post
    for k, nom in [(-2, "m2"), (1, "p1"), (2, "p2")]:
        b[f"ev_o_{nom}"] = b.opos * b.toc * (b.k == k)
        b[f"ev_m_{nom}"] = (1 - b.opos) * b.toc * (b.k == k)
    b["pte"] = b.partido + "_" + b.tema + "_" + b.emision
    b["pse"] = b.partido + "_" + b.sesion + "_" + b.emision
    return b


def con_y(b):
    """Primer tipo de cero: si el partido no habló en la sesión, no hay porcentaje y la fila sale."""
    b = b[b.total > 0].copy()
    b["Y"] = 100 * b.W / b.total
    return b


# ---------------------------------------------------------------- estimación

def _filas(fit, nombres, modelo, b, pesos, poisson=False):
    out = []
    ci = fit.confint()
    for coef, bloque in nombres:
        est, se, p = fit.coef()[coef], fit.se()[coef], fit.pvalue()[coef]
        fila = {"modelo": modelo, "bloque": bloque, "coef": est, "se": se, "p": p,
                "ic_bajo": ci.loc[coef].iloc[0], "ic_alto": ci.loc[coef].iloc[1],
                "n": fit._N, "emisiones": b.emision.nunique()}
        if poisson:
            fila["relativo"] = np.exp(est) - 1
        elif bloque in ("oposicion", "morena"):
            g = b[(b.toc == 1) & (b.post == 0) & (b.opos == (bloque == "oposicion"))]
            base = np.average(g.Y, weights=g.total) if pesos else g.Y.mean()
            fila["base"], fila["relativo"] = base, est / base
        out.append(fila)
    return out


def estimar(b, modelo="lineal_pesos"):
    """β de la oposición, de Morena y su diferencia. Lineal: puntos porcentuales y relativo
    a la base antes de la emisión. Poisson: relativo."""
    b = con_y(b)
    if modelo == "poisson":
        # Los grupos con puros ceros no aportan nada al Poisson.
        while True:
            vivos = np.ones(len(b), bool)
            for fe in ["pte", "pse"]:
                vivos &= b.groupby(fe).W.transform("sum").to_numpy() > 0
            if vivos.all():
                break
            b = b[vivos]
        kw = dict(data=b, vcov=VCOV, weights="total", demeaner_backend="scipy", fixef_tol=1e-6)
        fit = pf.fepois("Y ~ tp_o + tp_m | pte + pse", **kw)
        dif = pf.fepois("Y ~ tp + tp_o | pte + pse", **kw)
        return (_filas(fit, [("tp_o", "oposicion"), ("tp_m", "morena")], modelo, b, True, True)
                + _filas(dif, [("tp_o", "diferencia")], modelo, b, True, True))
    w = "total" if modelo == "lineal_pesos" else None
    fit = pf.feols("Y ~ tp_o + tp_m | pte + pse", data=b, vcov=VCOV, weights=w)
    dif = pf.feols("Y ~ tp + tp_o | pte + pse", data=b, vcov=VCOV, weights=w)
    return (_filas(fit, [("tp_o", "oposicion"), ("tp_m", "morena")], modelo, b, w is not None)
            + _filas(dif, [("tp_o", "diferencia")], modelo, b, w is not None))


def eventos(b):
    """Estudio de eventos: la sesión -1 es la referencia; β en -2 es la prueba de tendencias previas."""
    b = con_y(b)
    regs = [f"ev_{q}_{k}" for q in "om" for k in ["m2", "p1", "p2"]]
    fit = pf.feols(f"Y ~ {' + '.join(regs)} | pte + pse", data=b, vcov=VCOV, weights="total")
    nombres = [(r, f"{'oposicion' if r[3] == 'o' else 'morena'} k={dict(m2=-2, p1=1, p2=2)[r[5:]]}")
               for r in regs]
    return _filas(fit, nombres, "eventos", b, True)


# ---------------------------------------------------------------- registro y guardas

def commit():
    r = subprocess.run(["git", "-C", str(RAIZ), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip()


def exigir_plan_congelado():
    r = subprocess.run(["git", "-C", str(RAIZ), "tag", "-l", "plan-congelado"], capture_output=True, text=True)
    if r.stdout.strip() != "plan-congelado":
        sys.exit("No existe la etiqueta plan-congelado. El plan se congela antes de estimar con datos reales.")


def registrar(modo, especificacion, filas):
    ahora = datetime.now().isoformat(timespec="seconds")
    r = pd.DataFrame(filas).assign(fecha=ahora, modo=modo, especificacion=especificacion, commit=commit())
    r.to_csv(REGISTRO, mode="a", header=not REGISTRO.exists(), index=False)
    return r


def mostrar(filas):
    for f in filas:
        rel = f"  ({f['relativo']:+.0%})" if pd.notna(f.get("relativo", np.nan)) else ""
        print(f"  {f['modelo']:13s} {f['bloque']:16s} {f['coef']:+.3f} (ee {f['se']:.3f}, "
              f"IC {f['ic_bajo']:+.3f} a {f['ic_alto']:+.3f}, p {f['p']:.3f}){rel}")


# ---------------------------------------------------------------- modos

def barajar(toc, rng):
    """Fechas inventadas: a cada emisión le toca la sección de otra."""
    orden = emisiones_todas()
    valores = [toc.get(e, set()) for e in orden]
    return {e: valores[j] for e, j in zip(orden, rng.permutation(len(orden)))}


def principal():
    exigir_plan_congelado()
    elegidos = leer_elegidos()
    d, toc = cargar_reales(elegidos)
    filas = estimar(armar(d, toc, ventanas(), elegidos.values()))
    r = registrar("principal", "lineal pesada, 64 emisiones, temas elegidos", filas)
    RESULTADOS.mkdir(exist_ok=True)
    r.to_csv(RESULTADOS / f"principal_{datetime.now():%Y%m%d_%H%M}.csv", index=False)
    mostrar(filas)


def robustez():
    exigir_plan_congelado()
    elegidos = leer_elegidos()
    d, toc = cargar_reales(elegidos)
    v = ventanas()
    b = armar(d, toc, v, elegidos.values())
    variantes = [
        ("poisson", lambda: estimar(b, "poisson")),
        ("lineal sin pesos", lambda: estimar(b, "lineal")),
        ("66 emisiones (cuenta la sesión del mismo miércoles)",
         lambda: estimar(armar(d, toc, ventanas(True), elegidos.values()))),
        ("controles sin excluir e+1",
         lambda: estimar(armar(d, toc, v, elegidos.values(), excluir_sig=False))),
        (f"solo intervenciones de {MIN_LARGAS} palabras o más",
         lambda: estimar(armar(d[d.palabras >= MIN_LARGAS], toc, v, elegidos.values()))),
        ("estudio de eventos (referencia: sesión -1)", lambda: eventos(b)),
    ]
    for n in (5, 10):
        if (AQUI / f"temas_elegidos_{n}.csv").exists():
            el = leer_elegidos(n)
            dn, tn = cargar_reales(el)
            variantes.append((f"{n} temas", lambda dn=dn, tn=tn, el=el: estimar(armar(dn, tn, v, el.values()))))
        else:
            print(f"Aviso: falta temas_elegidos_{n}.csv; la variante de {n} temas no se corre.")
    todas = []
    for nombre, f in variantes:
        print(f"\n{nombre}")
        filas = f()
        mostrar(filas)
        todas += registrar("robustez", nombre, filas).to_dict("records")
    RESULTADOS.mkdir(exist_ok=True)
    pd.DataFrame(todas).to_csv(RESULTADOS / f"robustez_{datetime.now():%Y%m%d_%H%M}.csv", index=False)


def permutacion(n):
    exigir_plan_congelado()
    elegidos = leer_elegidos()
    d, toc = cargar_reales(elegidos)
    v = ventanas()
    obs = {f["bloque"]: f["coef"] for f in estimar(armar(d, toc, v, elegidos.values()))}
    rng = np.random.default_rng(SEMILLA)
    dist = {k: [] for k in obs}
    for _ in range(n):
        for f in estimar(armar(d, barajar(toc, rng), v, elegidos.values())):
            dist[f["bloque"]].append(f["coef"])
    filas = [{"modelo": "permutacion", "bloque": k, "coef": obs[k], "permutaciones": n,
              "p": float(np.mean(np.abs(dist[k]) >= abs(obs[k])))} for k in obs]
    registrar("permutacion", f"lineal pesada, {n} permutaciones de fechas", filas)
    for f in filas:
        print(f"  {f['bloque']:12s} {f['coef']:+.3f}  p por permutación {f['p']:.3f} ({n})")


def placebo(n):
    elegidos = leer_elegidos()
    d, toc = cargar_reales(elegidos)
    v = ventanas()
    rng = np.random.default_rng(SEMILLA + 1)
    filas = []
    for _ in range(n):
        filas += estimar(armar(d, barajar(toc, rng), v, elegidos.values()))
    r = registrar("placebo", f"lineal pesada, fechas barajadas, {n} corridas", filas)
    for blq, g in r.groupby("bloque", sort=False):
        print(f"  {blq:12s} media {g.coef.mean():+.3f} pp; p < 0.05 en {(g.p < 0.05).mean():.0%} de {n}")
    print("Si la media se aleja de cero o p < 0.05 sale mucho más que 5%, hay un error en la tubería.")


def descriptivos():
    elegidos = leer_elegidos()
    d, toc = cargar_reales(elegidos)
    v = ventanas()
    b = armar(d, toc, v, elegidos.values())
    orden = emisiones_todas()
    pos = {e: i for i, e in enumerate(orden)}
    n_trat = pd.Series({e: len(conjuntos(e, toc, orden, pos, set(elegidos.values()))[0])
                        for e in v.emision.unique()})
    print(f"Emisiones: {v.emision.nunique()}; temas tratados por emisión: {n_trat.value_counts().sort_index().to_dict()}")
    sesiones = d[d.sesion.isin(v.sesion)]
    sin_libres = set(v.sesion) - set(sesiones.sesion)
    print(f"Sesiones en ventanas: {v.sesion.nunique()}; sin ninguna intervención libre: {len(sin_libres)}")
    blq = sesiones.assign(bloque=np.where(sesiones.partido == "MORENA", "Morena", "oposición"))
    print("Palabras por bloque y sesión (mediana):",
          blq.groupby(["bloque", "sesion"]).palabras.sum().groupby("bloque").median().round().to_dict())
    print(f"Filas fuera porque el partido no habló en la sesión: {(b.total == 0).mean():.0%}")
    vivas = b[b.total > 0]
    print(f"De las que quedan, Y = 0 (habló de otra cosa): {(vivas.W == 0).mean():.0%}")


# ---------------------------------------------------------------- prueba con datos simulados

def simular(d, v, tau, rng, n_elegidos=7, n_otros=15):
    """Temas inventados sobre las intervenciones reales. Cada emisión toca 2 temas elegidos
    y 1 no elegido. La oposición mueve discursos hacia los tratados en las sesiones posteriores."""
    elegidos = [f"T{i}" for i in range(1, n_elegidos + 1)]
    otros = [f"cap{100 + i}" for i in range(n_otros)]
    zipf = 1 / np.arange(1, n_elegidos + 1) ** 0.8
    p = np.concatenate([0.6 * zipf / zipf.sum(), np.full(n_otros, 0.4 / n_otros)])
    temas = np.array(elegidos + otros)
    base = dict(zip(temas, p))
    orden = emisiones_todas()
    pos = {e: i for i, e in enumerate(orden)}
    p_el = p[:n_elegidos] / p[:n_elegidos].sum()
    toc = {e: set(rng.choice(elegidos, 2, replace=False, p=p_el)) | {rng.choice(otros)} for e in orden}
    tema = rng.choice(temas, len(d), p=p)
    verdadero = []
    for e, ses in v[v.k > 0].groupby("emision").sesion:
        trat, ctrl, fuera = conjuntos(e, toc, orden, pos, set(elegidos))
        if not trat:
            continue
        t_e = sorted(trat)
        q = sum(base[t] for t in t_e)
        pi = min(q * tau / (1 - q), 1.0)
        b_ctrl = [base[t] for t in ctrl] + [sum(base[t] for t in otros if t not in fuera)]
        verdadero.append(tau + pi * np.mean(b_ctrl) / np.mean([base[t] for t in t_e]))
        if tau == 0:
            continue
        idx = np.flatnonzero(d.sesion.isin(ses).to_numpy() & (d.partido != "MORENA").to_numpy())
        cambia = idx[rng.random(len(idx)) < pi]
        tema[cambia] = rng.choice(t_e, len(cambia), p=[base[t] / q for t in t_e])
    return d.assign(tema=tema), toc, elegidos, float(np.mean(verdadero))


def prueba(n):
    d0, v = intervenciones(), ventanas()
    rng = np.random.default_rng(SEMILLA)
    print(f"Prueba con datos simulados: {len(d0)} intervenciones reales con temas inventados, "
          f"{v.emision.nunique()} emisiones, {n} corridas por escenario.")
    for tau in (0.0, 0.5):
        res, ver = [], []
        for _ in range(n):
            d, toc, el, verdadero = simular(d0, v, tau, rng)
            res.append({f["bloque"]: f for f in estimar(armar(d, toc, v, el))})
            ver.append(verdadero)
        o = pd.DataFrame([r["oposicion"] for r in res])
        m = pd.DataFrame([r["morena"] for r in res])
        df = pd.DataFrame([r["diferencia"] for r in res])
        print(f"\nEfecto puesto en la oposición: {tau:+.0%} (verdadero para la lineal: {np.mean(ver):+.0%})")
        print(f"  oposición: mediana {o.relativo.median():+.0%}, rechaza en {(o.p < 0.05).mean():.0%}")
        print(f"  Morena:    mediana {m.relativo.median():+.0%}, rechaza en {(m.p < 0.05).mean():.0%}")
        print(f"  diferencia: rechaza en {(df.p < 0.05).mean():.0%}")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "prueba"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else None
    {"prueba": lambda: prueba(n or 20), "descriptivos": descriptivos, "placebo": lambda: placebo(n or 20),
     "principal": principal, "robustez": robustez, "permutacion": lambda: permutacion(n or 500)}[modo]()
