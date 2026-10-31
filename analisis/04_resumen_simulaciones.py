"""Resume las simulaciones de poder en una tabla comparable entre modelos.

Lee todos los analisis/resultados_simulacion_poder*.csv que haya y, para cada
variante y cada efecto simulado (tau), calcula:
  - rechazo: proporción de simulaciones con p < 0.05. Con tau = 0 es la tasa de
    falsos positivos (debería ser 5%); con tau > 0 es el poder.
  - sesgo: cuánto se aleja, en promedio, el beta estimado de su valor verdadero,
    en % del verdadero. Cada modelo se compara contra su propio verdadero
    (el Poisson en logaritmos, la lineal como efecto en %), así que el sesgo
    relativo sí es comparable entre modelos.
  - ee: error estándar de simulación de cada cifra. Sirve para saber si dos
    modelos son distintos de verdad o solo por azar: si sus cifras difieren
    menos de unos dos ee, la diferencia no es clara.

Escribe la tabla en analisis/resumen_simulaciones.md y la imprime.

Uso: python 04_resumen_simulaciones.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
NOMBRES = {
    "": "Poisson, α por emisión",
    "colapsado": "Poisson, sesiones sumadas",
    "fe_simple": "Poisson, α para toda la legislatura",
    "fe_periodo": "Poisson, α por periodo",
    "lineal": "Lineal sin pesos, α por periodo",
    "lineal_pesos": "Lineal con pesos, α por periodo",
}


def resumir(r):
    filas = []
    for tau, g in r.groupby("tau"):
        ok = g.dropna(subset=["beta", "p"])
        n = len(ok)
        rech = (ok.p < 0.05).mean()
        fila = {
            "tau": tau,
            "n": n,
            "fallas": len(g) - n,
            "rechazo": rech,
            "rechazo_ee": np.sqrt(rech * (1 - rech) / n) if n else np.nan,
            "beta_media": ok.beta.mean(),
            "verdadero": ok.verdadero.mean(),
        }
        if tau > 0 and fila["verdadero"]:
            fila["sesgo"] = fila["beta_media"] / fila["verdadero"] - 1
            fila["sesgo_ee"] = ok.beta.std() / np.sqrt(n) / fila["verdadero"]
        filas.append(fila)
    return pd.DataFrame(filas)


def main():
    archivos = sorted((RAIZ / "analisis").glob("resultados_simulacion_poder*.csv"))
    if not archivos:
        raise SystemExit("No hay resultados. Corre primero 03_simulacion_poder.py.")
    lineas = [
        "# Resumen de las simulaciones de poder",
        "",
        "Generado por `analisis/04_resumen_simulaciones.py`. Temas asignados al azar; no usa resultados reales.",
        "",
        "- **Falsos positivos**: rechazo con efecto 0. Lo ideal es 5%.",
        "- **Poder**: rechazo con efecto positivo.",
        "- **Sesgo**: diferencia promedio entre el beta estimado y su verdadero, en % del verdadero.",
        "- Entre paréntesis, el error estándar de simulación. Diferencias menores a unos dos errores estándar no son claras.",
        "",
        "| Modelo | Simulaciones por efecto | Falsos positivos | Poder con +25% | Poder con +50% | Poder con +100% | Sesgo con +50% |",
        "|---|---|---|---|---|---|---|",
    ]
    for f in archivos:
        variante = f.stem.replace("resultados_simulacion_poder", "").lstrip("_")
        s = resumir(pd.read_csv(f)).set_index("tau")

        def rechazo(tau):
            if tau not in s.index:
                return "no se corrió"
            return f"{s.loc[tau, 'rechazo']:.0%} (±{s.loc[tau, 'rechazo_ee']:.0%})"

        sesgo = "no se corrió"
        if 0.5 in s.index and "sesgo" in s and not pd.isna(s.loc[0.5, "sesgo"]):
            sesgo = f"{s.loc[0.5, 'sesgo']:+.0%} (±{s.loc[0.5, 'sesgo_ee']:.0%})"
        n = int(s.n.min())
        fallas = int(s.fallas.sum())
        nombre = NOMBRES.get(variante, variante)
        if fallas:
            nombre += f" ({fallas} ajustes fallidos)"
        lineas.append(f"| {nombre} | {n} | {rechazo(0.0)} | {rechazo(0.25)} | {rechazo(0.5)} | {rechazo(1.0)} | {sesgo} |")
    texto = "\n".join(lineas) + "\n"
    (RAIZ / "analisis" / "resumen_simulaciones.md").write_text(texto, encoding="utf8")
    print(texto)


if __name__ == "__main__":
    main()
