"""Simulación de poder: si la mañanera de verdad moviera a la oposición,
¿lo detectaría nuestro modelo con los datos que tenemos?

Usa los discursos reales de las secciones libres (quién habló, cuándo y cuánto),
pero les asigna temas inventados, porque todavía no hay clasificador. Así no se
mira ningún resultado real. En cada simulación:
  1. Cada discurso recibe un tema al azar (20 temas, unos más comunes que otros).
  2. Cada emisión "toca" 3 temas al azar.
  3. En las dos sesiones posteriores, los discursos de la oposición se cargan
     hacia los temas tocados lo suficiente para que su peso suba en tau
     (tau = 0.5 significa +50%). Morena no cambia.
  4. Se estima el Poisson con los tres efectos fijos y errores por emisión.
El poder es la proporción de simulaciones con p < 0.05.

Uso: python 03_simulacion_poder.py [n_simulaciones] [colapsado]
"colapsado" suma las dos sesiones previas y las dos posteriores de cada ventana.
"fe_simple" usa un solo efecto partido-tema para todas las emisiones (α_pt en vez de α_pte).
"fe_periodo" usa un efecto partido-tema por periodo ordinario.
"lineal" y "lineal_pesos" estiman, con los mismos efectos fijos que "fe_periodo", una
regresión lineal sobre el porcentaje de las palabras del partido en la sesión (sin pesos
o pesada por las palabras totales). Su beta se reporta como efecto en % (β / porcentaje base)
y "verdadero" es tau.
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf

RAIZ = Path(__file__).resolve().parents[1]
N_TEMAS, TOCADOS = 20, 3
PARTIDOS = ["PAN", "PRI", "PRD", "MC", "MORENA"]
BASE = 1 / np.arange(1, N_TEMAS + 1) ** 0.8
BASE /= BASE.sum()


def cargar():
    d = pd.read_csv(f"{RAIZ}/datos/discursos_libres.csv")
    d = d[d.discurso & d.partido.isin(PARTIDOS)].reset_index(drop=True)
    v = pd.read_csv(f"{RAIZ}/datos/ventanas.csv")
    return d, v


def simular(d, v, tau, rng, colapsar=False, fe_simple=False, fe_periodo=False, lineal=None):
    emisiones = sorted(v.emision.unique())
    tocados = {e: rng.choice(N_TEMAS, TOCADOS, replace=False, p=BASE) for e in emisiones}
    tema = rng.choice(N_TEMAS, len(d), p=BASE)
    # Tratado: tocado por e y no por la emisión anterior. Control: no tocado por e-1, e ni e+1.
    tratados, controles = {}, {}
    for i, e in enumerate(emisiones):
        prev = set(tocados[emisiones[i - 1]]) if i > 0 else set()
        sig = set(tocados[emisiones[i + 1]]) if i + 1 < len(emisiones) else set()
        tratados[e] = set(tocados[e]) - prev
        controles[e] = set(range(N_TEMAS)) - prev - set(tocados[e]) - sig

    objetivo = []
    if tau > 0:
        post = v[v.k > 0]
        for e, ses in post.groupby("emision").sesion:
            t_e = sorted(tratados[e])
            if not t_e:
                continue
            q = BASE[t_e].sum()
            pi = min(q * tau / (1 - q), 1.0)
            # Efecto verdadero sobre la razón tema tocado / temas de control.
            objetivo.append(np.log((1 + tau) / (1 - pi)))
            idx = np.flatnonzero(d.sesion.isin(ses) & (d.bloque == "oposicion"))
            cambia = idx[rng.random(len(idx)) < pi]
            tema[cambia] = rng.choice(t_e, len(cambia), p=BASE[t_e] / q)

    d = d.assign(tema=tema)
    W = d.groupby(["sesion", "partido", "tema"]).palabras.sum()

    filas = []
    for e, g in v.groupby("emision"):
        temas = sorted(tratados[e] | controles[e])
        idx = pd.MultiIndex.from_product([g.sesion, PARTIDOS, temas], names=["sesion", "partido", "tema"])
        b = W.reindex(idx, fill_value=0).reset_index(name="W")
        b = b.merge(g[["sesion", "k"]], on="sesion")
        b["emision"] = e
        b["toc"] = b.tema.isin(tratados[e]).astype(int)
        filas.append(b)
    b = pd.concat(filas, ignore_index=True)
    b["opos"] = (b.partido != "MORENA").astype(int)
    b["post"] = (b.k > 0).astype(int)
    if colapsar:
        # Variante: se suman las dos sesiones previas y las dos posteriores.
        b = (b.groupby(["emision", "partido", "tema", "post", "opos", "toc"], as_index=False).W.sum()
             .assign(sesion=lambda x: np.where(x.post == 1, "despues", "antes")))
    b["ddd"] = b.opos * b.toc * b.post
    if fe_periodo:
        # Periodo ordinario de la emisión: año y semestre (otoño o primavera).
        sufijo_fe = "_" + b.emision.str[:4] + np.where(b.emision.str[5:7].astype(int) >= 9, "o", "p")
    elif fe_simple:
        sufijo_fe = ""
    else:
        sufijo_fe = "_" + b.emision
    b["pte"] = b.partido + "_" + b.tema.astype(str) + sufijo_fe
    b["pse"] = b.partido + "_" + b.sesion + "_" + b.emision
    b["tse"] = b.tema.astype(str) + "_" + b.sesion + "_" + b.emision
    if lineal:
        return estimar_lineal(b, d, tau, pesos=(lineal == "pesos"))
    # Un grupo de efecto fijo con puros ceros no aporta nada al Poisson (su
    # efecto fijo se va a menos infinito); se quitan antes de estimar.
    while True:
        vivos = np.ones(len(b), bool)
        for fe in ["pte", "pse", "tse"]:
            vivos &= b.groupby(fe).W.transform("sum").to_numpy() > 0
        if vivos.all():
            break
        b = b[vivos]
    fit = pf.fepois("W ~ ddd | pte + pse + tse", data=b, vcov={"CRV1": "emision"},
                    demeaner_backend="scipy", fixef_tol=1e-6)
    verdadero = float(np.mean(objetivo)) if objetivo else 0.0
    return fit.coef()["ddd"], fit.pvalue()["ddd"], verdadero


def estimar_lineal(b, d, tau, pesos):
    """Regresión lineal sobre el porcentaje de las palabras del partido en la sesión.
    Regresa el efecto en % (β entre el porcentaje base) para compararlo con el Poisson."""
    total = d.groupby(["sesion", "partido"]).palabras.sum().rename("total")
    b = b.merge(total, left_on=["sesion", "partido"], right_index=True, how="left")
    # Si el partido no habló en la sesión, el porcentaje no existe.
    b = b[b.total > 0].copy()
    b["Y"] = 100 * b.W / b.total
    fit = pf.feols("Y ~ ddd | pte + pse + tse", data=b, vcov={"CRV1": "emision"},
                   weights="total" if pesos else None)
    base = b[(b.opos == 1) & (b.toc == 1) & (b.post == 0)].Y.mean()
    return fit.coef()["ddd"] / base, fit.pvalue()["ddd"], tau


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    variante = sys.argv[2] if len(sys.argv) > 2 else ""
    colapsar, fe_simple, fe_periodo = (variante == x for x in ["colapsado", "fe_simple", "fe_periodo"])
    # Las variantes lineales usan los mismos efectos fijos que el Poisson recomendado (α por periodo).
    lineal = {"lineal": "sin_pesos", "lineal_pesos": "pesos"}.get(variante)
    fe_periodo = fe_periodo or lineal is not None
    taus = [0.0, 0.5, 1.0] if variante else [0.0, 0.25, 0.5, 1.0]
    d, v = cargar()
    print(f"{len(d)} discursos libres largos; {v.emision.nunique()} emisiones", flush=True)
    rng = np.random.default_rng(20261027)
    res = []
    for tau in taus:
        t0 = time.time()
        for _ in range(n):
            try:
                b, p, ver = simular(d, v, tau, rng, colapsar, fe_simple, fe_periodo, lineal)
            except Exception:  # una base sin variación hace fallar el ajuste
                b, p, ver = np.nan, np.nan, np.nan
            res.append({"tau": tau, "beta": b, "p": p, "verdadero": ver})
        r = pd.DataFrame(res)
        r = r[r.tau == tau]
        print(f"tau={tau:.2f}: rechaza H0 en {(r.p < 0.05).mean():.0%} "
              f"(beta mediana {r.beta.median():.2f}, sd {r.beta.std():.2f}, verdadero {r.verdadero.mean():.2f}; "
              f"fallas {r.p.isna().sum()}) [{time.time() - t0:.0f}s]", flush=True)
    sufijo = f"_{variante}" if variante else ""
    pd.DataFrame(res).to_csv(f"{RAIZ}/analisis/resultados_simulacion_poder{sufijo}.csv", index=False)


if __name__ == "__main__":
    main()
