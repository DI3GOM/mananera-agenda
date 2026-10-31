"""Junta los textos que va a clasificar el modelo de lenguaje.

1. La sección "Quién es quién en las mentiras" de cada emisión, turno por turno.
   La sección empieza con el primer turno de la presentadora (Ana Elizabeth García
   Vilchis) o con la frase "Esta es la sección 'Quién es quién...'", y termina con
   su cierre ("Es cuanto, señor presidente", "Hasta aquí la sección"...). En algunas
   fechas la transcripción le atribuye al Presidente lo que dice la presentadora;
   por eso también se busca por las frases de apertura y cierre.
2. Las intervenciones de los diputados en las secciones libres de la LXV. La
   versión estenográfica no marca párrafos, así que la unidad es la intervención.

No se mira ningún resultado: solo se extrae texto.
Salidas: datos/clasificar/seccion_turnos.csv y datos/clasificar/intervenciones.csv
"""
import re
import unicodedata
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "datos" / "clasificar"
LIBRES = {"iniciativas", "proposiciones", "agenda_politica", "intervenciones"}
PARTIDOS = {"PAN", "PRI", "PRD", "MC", "MORENA"}
# Intervenciones más cortas que esto son de trámite ("Con su venia", "Gracias") y
# se marcan como "sin tema" sin mandarlas al modelo.
MIN_PALABRAS = 10

APERTURA = re.compile(r"(?:(?:esta es|con) la secci[oó]n|este es el|vamos (?:a comenzar )?con el).{0,15}qui[eé]n es qui[eé]n", re.I)
CIERRE = re.compile(r"(?:es cuanto|es todo),? (?:se[ñn]or )?presidente|hasta aqu[ií] la secci[oó]n", re.I)


def normalizar(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()


def seccion(d):
    """Turnos de la sección dentro de la mañanera de un día (d en orden original)."""
    d = d.reset_index(drop=True)
    vil = d.participante.map(normalizar).str.contains("GARCIA VI.?CHIS")
    abre = d.texto.str.contains(APERTURA)
    candidatos = d.index[vil | abre]
    if len(candidatos) == 0:
        return d.iloc[0:0]
    ini = candidatos[0]
    cierra = d.index[(d.index > ini) & d.texto.str.contains(CIERRE)]
    if len(cierra):
        fin = cierra[0]
    elif vil.any():
        fin = d.index[vil][-1]
    else:
        # Sin presentadora ni cierre: hasta antes de la siguiente pregunta de la prensa.
        preg = d.index[(d.index > ini) & d.participante.map(normalizar).str.startswith("PREGUNTA")]
        fin = preg[0] - 1 if len(preg) else d.index[-1]
    s = d.loc[ini:fin]
    quien = s.participante.map(normalizar)
    # Las preguntas de la prensa no son parte de la sección. Cuando la transcripción
    # sí identifica a la presentadora, los turnos del Presidente son comentarios suyos
    # y tampoco cuentan; cuando no la identifica, su texto viene como del Presidente.
    fuera = quien.str.startswith("PREGUNTA")
    if vil.any():
        fuera |= quien.str.startswith("PRESIDENTE")
    return s[~fuera]


def turnos_seccion():
    m = pd.read_parquet(RAIZ / "datos" / "mananeras.parquet",
                        columns=["fecha", "participante", "texto", "palabras"])
    emis = pd.read_csv(RAIZ / "datos" / "emisiones_quien_es_quien.csv")
    filas = []
    for f in emis.fecha:
        s = seccion(m[m.fecha == f])
        filas.append(s.assign(emision=f, turno=range(1, len(s) + 1)))
    t = pd.concat(filas, ignore_index=True)
    return t[["emision", "turno", "participante", "palabras", "texto"]]


def intervenciones():
    t = pd.read_csv(RAIZ / "datos" / "turnos_secciones.csv")
    t = t[(t.rol == "diputado") & t.seccion.isin(LIBRES) & t.partido.isin(PARTIDOS)].copy()
    t["sesion"] = t.fecha + t.sufijo.fillna("").map(lambda s: f"-{s}" if s else "")
    t["id"] = [f"d{i:05d}" for i in range(len(t))]
    t["corta"] = t.palabras < MIN_PALABRAS
    return t[["id", "sesion", "seccion", "orador", "partido", "palabras", "corta", "texto"]]


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    s = turnos_seccion()
    s.to_csv(SALIDA / "seccion_turnos.csv", index=False)
    por = s.groupby("emision").palabras.sum()
    emis = pd.read_csv(RAIZ / "datos" / "emisiones_quien_es_quien.csv")
    vacias = sorted(set(emis.fecha) - set(por.index))
    print(f"Sección: {len(por)} de {len(emis)} emisiones con texto; {len(s)} turnos")
    print(f"  palabras por emisión: mediana {por.median():.0f}, mínimo {por.min()}, máximo {por.max()}")
    print(f"  emisiones sin texto de la sección: {vacias}")

    d = intervenciones()
    d.to_csv(SALIDA / "intervenciones.csv", index=False)
    print(f"Intervenciones libres: {len(d)} ({(~d.corta).sum()} van al modelo, "
          f"{d.corta.sum()} de trámite); {d.palabras.sum():,} palabras")


if __name__ == "__main__":
    main()
