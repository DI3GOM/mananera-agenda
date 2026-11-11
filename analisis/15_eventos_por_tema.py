"""ANÁLISIS EXPLORATORIO (decidido el 11 de noviembre, después de ver los resultados).

Estudio de eventos por tema, para la presentación: el mismo modelo que el estudio de eventos
de 11_estimar.py (referencia: sesión -1), pero estimado por separado para cada uno de los 7 temas.
Para el tema t se usan solo las emisiones en que t fue tratado; en ellas entran la fila de t,
los controles y el resto (se quitan los otros temas tratados de esa emisión).

Se corre una vez, se registra en registro_corridas.csv con modo "exploratorio" y se reportan
los 7 temas, salgan como salgan. Con pocas emisiones por tema los intervalos son anchos y los
errores agrupados son poco confiables; no es una prueba, es una descripción.

Uso: python 15_eventos_por_tema.py
"""
from datetime import datetime
from importlib import import_module

import pandas as pd

e = import_module("11_estimar")

NOMBRES = {1: "Economía", 2: "Derechos civiles", 3: "Salud", 8: "Energía",
           10: "Transporte", 12: "Justicia y seguridad", 20: "Gobierno"}


def main():
    e.exigir_plan_congelado()
    elegidos = e.leer_elegidos()
    d, toc = e.cargar_reales(elegidos)
    b = e.armar(d, toc, e.ventanas(), elegidos.values())
    filas = []
    for cap, t in elegidos.items():
        emis = b[(b.tema == t) & (b.toc == 1)].emision.unique()
        bt = b[b.emision.isin(emis) & ((b.toc == 0) | (b.tema == t))]
        for f in e.eventos(bt):
            f["tema"] = NOMBRES[cap]
            filas.append(f)
        print(f"{NOMBRES[cap]}: {len(emis)} emisiones con el tema tratado")
    r = e.registrar("exploratorio", "estudio de eventos por tema (referencia: sesión -1)", filas)
    e.RESULTADOS.mkdir(exist_ok=True)
    r.to_csv(e.RESULTADOS / f"eventos_por_tema_{datetime.now():%Y%m%d_%H%M}.csv", index=False)
    e.mostrar(filas)


if __name__ == "__main__":
    main()
