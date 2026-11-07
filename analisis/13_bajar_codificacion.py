"""Pasa la codificación a mano de la página web a las hojas de 08_validacion.py.

Tania y Paola codifican en la página "Codificación de temas CAP"
(https://claude.ai/artifact/Q2b6azTqbge7jEvdrnqzJ2). Cada una guarda sus respuestas en
un documento `codigos/<su id>` de la base de datos de la página, con su hoja (A o B).

Primero se baja la colección `codigos` a una carpeta (Claude lo hace con la herramienta
ArtifactData, `list` con `out_dir`); luego este script llena las columnas tema, blanco y
notas de datos/validacion/hoja_codificador_A.csv y _B.csv. Después: 08_validacion.py alfa.

Uso: python 13_bajar_codificacion.py <carpeta con los JSON de codigos>
"""
import json
import sys
from pathlib import Path

import pandas as pd

VAL = Path(__file__).resolve().parents[1] / "datos" / "validacion"


def cuerpo(f):
    d = json.loads(f.read_text(encoding="utf-8"))
    # El archivo puede traer el documento solo o envuelto con sus metadatos.
    for k in ("data", "document", "fields"):
        if "respuestas" not in d and isinstance(d.get(k), dict):
            d = d[k]
    return d


def main(carpeta):
    docs = [cuerpo(f) for f in sorted(Path(carpeta).rglob("*.json"))]
    docs = [d for d in docs if "respuestas" in d]
    por_hoja = {}
    for d in docs:
        h = d.get("hoja")
        if h in por_hoja:
            sys.exit(f"Hay dos documentos con la hoja {h}; revisa cuál es el bueno antes de seguir.")
        por_hoja[h] = d["respuestas"]
    for h in "AB":
        if h not in por_hoja:
            print(f"Hoja {h}: nadie la ha llenado todavía.")
            continue
        hoja = VAL / f"hoja_codificador_{h}.csv"
        t = pd.read_csv(hoja)
        r = por_hoja[h]
        t["tema"] = t.unidad.map(lambda u: r.get(u, {}).get("tema"))
        t["blanco"] = t.unidad.map(lambda u: r.get(u, {}).get("blanco"))
        t["notas"] = t.unidad.map(lambda u: r.get(u, {}).get("notas"))
        t["tema"] = t.tema.astype("Int64")
        t.to_csv(hoja, index=False)
        falta = t.tema.isna().sum() + ((t.tipo == "seccion") & t.blanco.isna()).sum()
        print(f"Hoja {h}: {t.tema.notna().sum()} de {len(t)} con tema; {falta} campos por llenar.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
