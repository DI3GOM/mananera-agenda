"""Elige los temas del análisis con la regla de la metodología v3 y el plan.

Un tema del CAP entra si:
  1. la sección lo tocó en al menos 8 de las 64 emisiones de la muestra;
  2. los diputados hablan de él: al menos 1% de sus palabras en las sesiones de las
     ventanas, todas juntas (sin separar por bloque ni por antes y después);
  3. lo distinguimos bien de los demás: se revisa con el alfa por tema de 08. Si dos
     temas se confunden, se juntan en TEMAS_JUNTOS antes de correr el principal.
"Sin tema de política" (0) no entra. Entre los que cumplen, se toman los más frecuentes
en la sección: 7 para el análisis principal, 5 y 10 para la robustez.

No mira ningún resultado: solo cuenta emisiones de la sección y palabras totales.
Salidas: analisis/temas_elegidos.csv (7), temas_elegidos_5.csv y temas_elegidos_10.csv.
"""
import re
import sys
from importlib import import_module
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
m = import_module("11_estimar")

MIN_EMISIONES = 8
MIN_PCT_DIPUTADOS = 1.0
TEMAS_JUNTOS = {}  # p. ej. {16: 12} si el alfa muestra que Defensa y Justicia se confunden


def main():
    libro = (AQUI / "libro_de_codigos.md").read_text(encoding="utf-8")
    nombre = {int(n): t for n, t in re.findall(r"^- \*\*(\d+) ([^*]+)\*\*", libro, re.M)}
    v = m.ventanas()
    junta = lambda c: TEMAS_JUNTOS.get(int(c), int(c))

    it = pd.read_csv(m.CLAS / "temas_seccion.csv")
    it = it[it.emision.isin(set(v.emision))].assign(tema=lambda x: x.tema.map(junta))
    emisiones = it.groupby("tema").emision.nunique()

    d = pd.read_csv(m.CLAS / "temas_intervenciones.csv")
    d = d[~d.corta & d.sesion.isin(set(v.sesion))].dropna(subset=["tema"]).assign(tema=lambda x: x.tema.map(junta))
    pct = 100 * d.groupby("tema").palabras.sum() / d.palabras.sum()

    t = pd.DataFrame({"emisiones": emisiones, "pct_diputados": pct}).fillna(0)
    t["cumple"] = (t.index != 0) & (t.emisiones >= MIN_EMISIONES) & (t.pct_diputados >= MIN_PCT_DIPUTADOS)
    t = t.sort_values(["cumple", "emisiones", "pct_diputados"], ascending=False)
    t["nombre"] = t.index.map(lambda c: nombre.get(int(c), "?"))
    print(t.head(15).round(1).to_string())

    elegibles = t[t.cumple].index.astype(int).tolist()
    for n, archivo in [(7, "temas_elegidos.csv"), (5, "temas_elegidos_5.csv"), (10, "temas_elegidos_10.csv")]:
        if len(elegibles) < n:
            print(f"Aviso: solo {len(elegibles)} temas cumplen la regla; la lista de {n} queda corta.")
        if n < len(elegibles) and t.emisiones[elegibles[n - 1]] == t.emisiones[elegibles[n]]:
            print(f"Aviso: empate en el lugar {n}; se desempata por palabras de los diputados.")
        caps = [c for c, j in [(c, junta(c)) for c in nombre] if j in elegibles[:n]]
        pd.DataFrame({"cap": caps, "tema": [f"t{junta(c)}" for c in caps]}).to_csv(AQUI / archivo, index=False)
        print(f"{archivo}: {', '.join(f'{c} {nombre[c]}' for c in elegibles[:n])}")


if __name__ == "__main__":
    main()
