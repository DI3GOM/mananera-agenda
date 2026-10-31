"""Simulación del diseño simplificado (feedback del profesor, 30 de octubre de 2026).

Cambios frente a 03_simulacion_poder.py:
  - Pocos temas (7) más un tema "resto" que junta todos los demás y siempre es control.
  - Doble diferencia por bloque: tema tocado contra no tocado, antes contra después,
    con un efecto para la oposición y otro para Morena. La comparación entre bloques es
    la resta de los dos.
  - La misma Y en los dos modelos: porcentaje de las palabras del partido en la sesión.
  - Lineal pesada por las palabras del partido en la sesión como modelo principal;
    Poisson pesado como robustez. (El Poisson pesado sobre el porcentaje da el mismo β
    que el Poisson sobre palabras con el efecto partido-sesión.)
  - Ventanas sin la sesión del mismo día (64 emisiones).

Como en 03, los temas son inventados: no se mira ningún resultado real.

Uso: python 05_simulacion_rediseno.py [n_simulaciones] [n_temas]
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module

ventanas_mod = import_module("02_ventanas_y_volumen")

RAIZ = Path(__file__).resolve().parents[1]
PARTIDOS = ["PAN", "PRI", "PRD", "MC", "MORENA"]
PESO_RESTO, TOCADOS = 0.4, 2
ESCENARIOS = [("solo_oposicion", 0.0), ("solo_oposicion", 0.25), ("solo_oposicion", 0.5),
              ("solo_oposicion", 1.0), ("ambos", 0.5)]


def pesos_temas(n_temas):
    # Tema 0 es el "resto"; los demás siguen una ley de Zipf, como en 03.
    zipf = 1 / np.arange(1, n_temas + 1) ** 0.8
    return np.concatenate([[PESO_RESTO], (1 - PESO_RESTO) * zipf / zipf.sum()])


def cargar():
    d = pd.read_csv(f"{RAIZ}/datos/discursos_libres.csv")
    d = d[d.discurso & d.partido.isin(PARTIDOS)].reset_index(drop=True)
    v = ventanas_mod.ventanas(ventanas_mod.sesiones_lxv(), mismo_dia_es_post=False)
    return d, v


def armar_base(d, v, tau, escenario, base, rng):
    n_temas = len(base) - 1
    emisiones = sorted(v.emision.unique())
    p_toc = base[1:] / base[1:].sum()
    tocados = {e: set(rng.choice(np.arange(1, n_temas + 1), TOCADOS, replace=False, p=p_toc))
               for e in emisiones}
    tema = rng.choice(len(base), len(d), p=base)
    # Tratado: tocado por e y no por la emisión anterior.
    # Control: el resto y los temas que no tocaron e-1, e ni e+1.
    tratados, controles = {}, {}
    for i, e in enumerate(emisiones):
        prev = tocados[emisiones[i - 1]] if i > 0 else set()
        sig = tocados[emisiones[i + 1]] if i + 1 < len(emisiones) else set()
        tratados[e] = tocados[e] - prev
        controles[e] = set(range(n_temas + 1)) - prev - tocados[e] - sig

    reaccionan = ["oposicion"] if escenario == "solo_oposicion" else ["oposicion", "morena"]
    verdadero, verdadero_p = [], []
    for e, ses in v[v.k > 0].groupby("emision").sesion:
        t_e, c_e = sorted(tratados[e]), sorted(controles[e])
        if not t_e:
            continue
        q = base[t_e].sum()
        pi = min(q * tau / (1 - q), 1.0)
        # Efecto verdadero de la lineal en %: lo que suben los tocados más lo que bajan
        # los controles (de ahí salen los discursos que se mueven), entre la base de los tocados.
        verdadero.append(tau + pi * base[c_e].mean() / base[t_e].mean())
        # Efecto verdadero del Poisson: cuánto sube la razón tocados / controles.
        verdadero_p.append((1 + tau) / (1 - pi) - 1)
        if tau == 0:
            continue
        idx = np.flatnonzero(d.sesion.isin(ses) & d.bloque.isin(reaccionan))
        cambia = idx[rng.random(len(idx)) < pi]
        tema[cambia] = rng.choice(t_e, len(cambia), p=base[t_e] / q)

    d = d.assign(tema=tema)
    W = d.groupby(["sesion", "partido", "tema"]).palabras.sum()
    total = d.groupby(["sesion", "partido"]).palabras.sum().rename("total")
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
    b = b.merge(total, left_on=["sesion", "partido"], right_index=True, how="left")
    b["total"] = b.total.fillna(0)
    b["opos"] = (b.partido != "MORENA").astype(int)
    b["post"] = (b.k > 0).astype(int)
    b["tp_o"] = b.opos * b.toc * b.post
    b["tp_m"] = (1 - b.opos) * b.toc * b.post
    b["tp"] = b.toc * b.post
    b["pte"] = b.partido + "_" + b.tema.astype(str) + "_" + b.emision
    b["pse"] = b.partido + "_" + b.sesion + "_" + b.emision
    return b, float(np.mean(verdadero)), float(np.mean(verdadero_p))


def ceros(b):
    """Cuántas filas se pierden porque el partido no habló en la sesión, y cuántas
    de las que quedan valen cero."""
    vivas = b[b.total > 0]
    return {"sin_palabras_en_sesion": 1 - len(vivas) / len(b), "y_cero": (vivas.W == 0).mean()}


def estimar(b):
    b = b[b.total > 0].copy()
    b["Y"] = 100 * b.W / b.total
    vcov = {"CRV1": "emision+sesion"}
    res = {}
    for nombre, w in [("lineal_pesos", "total"), ("lineal", None)]:
        fit = pf.feols("Y ~ tp_o + tp_m | pte + pse", data=b, vcov=vcov, weights=w)
        dif = pf.feols("Y ~ tp + tp_o | pte + pse", data=b, vcov=vcov, weights=w)
        pre = b[(b.toc == 1) & (b.post == 0)]
        for blq, coef, op in [("o", "tp_o", 1), ("m", "tp_m", 0)]:
            g = pre[pre.opos == op]
            base = np.average(g.Y, weights=g.total) if w else g.Y.mean()
            res[f"{nombre}_{blq}"] = (fit.coef()[coef] / base, fit.pvalue()[coef])
        res[f"{nombre}_dif"] = (np.nan, dif.pvalue()["tp_o"])
    # Poisson pesado sobre el porcentaje. Los grupos con puros ceros no aportan nada.
    while True:
        vivos = np.ones(len(b), bool)
        for fe in ["pte", "pse"]:
            vivos &= b.groupby(fe).W.transform("sum").to_numpy() > 0
        if vivos.all():
            break
        b = b[vivos]
    fit = pf.fepois("Y ~ tp_o + tp_m | pte + pse", data=b, vcov=vcov, weights="total",
                    demeaner_backend="scipy", fixef_tol=1e-6)
    dif = pf.fepois("Y ~ tp + tp_o | pte + pse", data=b, vcov=vcov, weights="total",
                    demeaner_backend="scipy", fixef_tol=1e-6)
    for blq, coef in [("o", "tp_o"), ("m", "tp_m")]:
        res[f"poisson_{blq}"] = (np.exp(fit.coef()[coef]) - 1, fit.pvalue()[coef])
    res["poisson_dif"] = (np.nan, dif.pvalue()["tp_o"])
    return res


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    n_temas = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    base = pesos_temas(n_temas)
    d, v = cargar()
    print(f"{len(d)} discursos libres largos; {v.emision.nunique()} emisiones; "
          f"{n_temas} temas + resto", flush=True)
    rng = np.random.default_rng(20261031)
    filas = []
    for escenario, tau in ESCENARIOS:
        t0 = time.time()
        for _ in range(n):
            b, ver_l, ver_p = armar_base(d, v, tau, escenario, base, rng)
            fila = {"escenario": escenario, "tau": tau, "verdadero_lineal": ver_l,
                    "verdadero_poisson": ver_p, **ceros(b)}
            try:
                for k, (est, p) in estimar(b).items():
                    fila[f"{k}_est"], fila[f"{k}_p"] = est, p
            except Exception as err:  # una base sin variación hace fallar el ajuste
                print("falla:", err, flush=True)
            filas.append(fila)
        r = pd.DataFrame(filas)
        r = r[(r.escenario == escenario) & (r.tau == tau)]
        print(f"\n{escenario}, tau={tau:.2f} [{time.time() - t0:.0f}s]; "
              f"filas sin palabras {r.sin_palabras_en_sesion.mean():.0%}, Y = 0 en {r.y_cero.mean():.0%}; "
              f"verdadero lineal {r.verdadero_lineal.mean():.2f}, Poisson {r.verdadero_poisson.mean():.2f}", flush=True)
        for m in ["lineal_pesos", "lineal", "poisson"]:
            print(f"  {m:13s} oposición: rechaza {(r[f'{m}_o_p'] < 0.05).mean():.0%}, "
                  f"mediana {r[f'{m}_o_est'].median():.2f} (sd {r[f'{m}_o_est'].std():.2f}) | "
                  f"Morena: rechaza {(r[f'{m}_m_p'] < 0.05).mean():.0%}, "
                  f"mediana {r[f'{m}_m_est'].median():.2f} | "
                  f"diferencia: rechaza {(r[f'{m}_dif_p'] < 0.05).mean():.0%}", flush=True)
    pd.DataFrame(filas).to_csv(f"{RAIZ}/analisis/resultados_simulacion_rediseno_{n_temas}temas.csv",
                               index=False)


if __name__ == "__main__":
    main()
