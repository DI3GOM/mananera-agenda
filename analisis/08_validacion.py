"""Validación del clasificador.

  muestra   Arma las hojas para codificar a mano: intervenciones de diputados (mitad
            oposición, mitad Morena) e ítems de la sección. Las hojas no dicen ni el
            partido ni la fecha ni lo que contestó el modelo. Cada codificador llena la
            suya sin ver la del otro, con el libro de códigos (libro_de_codigos.md).
            Los ítems de la sección salen de temas_seccion.csv, así que primero hay que
            correr 07_clasificar.py seccion.
  alfa      Con las dos hojas llenas: el alfa de Krippendorff entre nosotros (en total y
            por tema), los temas que más confundimos y qué tanto acierta el modelo en
            los casos en que coincidimos, por separado para la oposición y para Morena.

  asignar   Reparte la muestra entre tres codificadores (A Tania, B Paola, C Diego):
            cada unidad la codifican dos, así que cada quien hace unas dos terceras
            partes. Los grupos se arman por estratos (oposición, Morena, sección).
            Escribe datos/validacion/asignacion.csv y la hoja C.

  reducir   Se queda con un subconjunto estratificado de la muestra ya asignada (por
            defecto 100 intervenciones, 50 y 50, y 60 ítems) sin cambiar las parejas.

Uso: python 08_validacion.py muestra [n_intervenciones] [n_items]
     python 08_validacion.py asignar
     python 08_validacion.py reducir [n_intervenciones] [n_items]
     python 08_validacion.py alfa
"""
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
CLAS = RAIZ / "datos" / "clasificar"
VAL = RAIZ / "datos" / "validacion"
SEMILLA = 20261031
MIN_PALABRAS = 30


def muestra(n_interv=150, n_items=80):
    rng = np.random.default_rng(SEMILLA)
    d = pd.read_csv(CLAS / "intervenciones.csv")
    d = d[d.palabras >= MIN_PALABRAS]
    d["bloque"] = np.where(d.partido == "MORENA", "morena", "oposicion")
    partes = [g.sample(n_interv // 2, random_state=SEMILLA) for _, g in d.groupby("bloque")]
    di = pd.concat(partes)
    unidades = pd.DataFrame({"id": di.id, "tipo": "diputado", "texto": di.texto, "bloque": di.bloque})

    if (CLAS / "temas_seccion.csv").exists():
        it = pd.read_csv(CLAS / "temas_seccion.csv").sample(n_items, random_state=SEMILLA)
        s = pd.read_csv(CLAS / "seccion_turnos.csv")
        textos = [" ".join(s[(s.emision == r.emision) & s.turno.between(r.turno_inicio, r.turno_fin)].texto)
                  for r in it.itertuples()]
        unidades = pd.concat([unidades, pd.DataFrame({
            "id": [f"s{r.emision}_{r.item}" for r in it.itertuples()], "tipo": "seccion",
            "texto": textos, "bloque": "seccion"})])
    else:
        print("Todavía no hay temas_seccion.csv: la hoja solo trae intervenciones.")

    unidades = unidades.iloc[rng.permutation(len(unidades))].reset_index(drop=True)
    unidades["unidad"] = [f"u{i:03d}" for i in range(1, len(unidades) + 1)]
    VAL.mkdir(parents=True, exist_ok=True)
    for c in "AB":
        hoja = VAL / f"hoja_codificador_{c}.csv"
        if hoja.exists() and pd.read_csv(hoja).tema.notna().any():
            sys.exit(f"{hoja.name} ya tiene códigos; no se sobrescribe. Muévela antes de rehacer la muestra.")
    unidades[["unidad", "id", "tipo", "bloque"]].to_csv(VAL / "clave.csv", index=False)
    hoja = unidades[["unidad", "tipo", "texto"]].assign(tema="", blanco="", notas="")
    for c in ["A", "B"]:
        hoja.to_csv(VAL / f"hoja_codificador_{c}.csv", index=False)
    print(f"{len(unidades)} unidades en datos/validacion/hoja_codificador_A.csv y _B.csv "
          f"({(unidades.tipo == 'diputado').sum()} intervenciones, {(unidades.tipo == 'seccion').sum()} ítems). "
          "La columna 'blanco' solo se llena en los ítems de la sección.")


PARES = ["AB", "BC", "AC"]


def asignar():
    clave = pd.read_csv(VAL / "clave.csv")
    rng = np.random.default_rng(SEMILLA)
    clave["orden"] = rng.permutation(len(clave))
    clave = clave.sort_values(["bloque", "orden"])
    # Dentro de cada estrato se reparte en rueda, así los tres grupos llevan la misma mezcla.
    clave["grupo"] = clave.groupby("bloque").cumcount() % 3 + 1
    clave["codificadores"] = clave.grupo.map(lambda g: PARES[g - 1])
    clave = clave.sort_values("unidad")
    clave[["unidad", "grupo", "codificadores"]].to_csv(VAL / "asignacion.csv", index=False)
    c = VAL / "hoja_codificador_C.csv"
    if not c.exists():
        pd.read_csv(VAL / "hoja_codificador_A.csv").assign(tema="", blanco="", notas="").to_csv(c, index=False)
    for h in "ABC":
        n = clave.codificadores.str.contains(h).sum()
        print(f"Hoja {h}: {n} unidades")
    print(pd.crosstab(clave.bloque, clave.codificadores))


def reducir(n_interv=100, n_items=60):
    """Subconjunto estratificado de la muestra ya asignada (decisión del 8 de noviembre).

    Conserva las unidades, sus id y su pareja de codificadores, así que lo que alguien ya
    haya codificado de las que se quedan sigue valiendo. Dentro de cada bloque se toma lo
    mismo de cada pareja (AB, AC, BC)."""
    clave = pd.read_csv(VAL / "clave.csv")
    asig = pd.read_csv(VAL / "asignacion.csv")
    x = clave.merge(asig, on="unidad")
    meta = {"oposicion": n_interv // 2, "morena": n_interv - n_interv // 2, "seccion": n_items}
    partes = []
    for bl, g in x.groupby("bloque"):
        grupos = sorted(g.grupo.unique())
        cuota = [meta[bl] // 3 + (i < meta[bl] % 3) for i in range(3)]
        for gr, n in zip(grupos, cuota):
            partes.append(g[g.grupo == gr].sample(n, random_state=SEMILLA))
    queda = pd.concat(partes).unidad
    clave[clave.unidad.isin(queda)].to_csv(VAL / "clave.csv", index=False)
    asig[asig.unidad.isin(queda)].to_csv(VAL / "asignacion.csv", index=False)
    for h in "ABC":
        f = VAL / f"hoja_codificador_{h}.csv"
        if f.exists():
            t = pd.read_csv(f)
            t[t.unidad.isin(queda)].to_csv(f, index=False)
    x = x[x.unidad.isin(queda)]
    print(f"Quedan {len(x)} unidades.")
    print(pd.crosstab(x.bloque, x.codificadores))
    for h in "ABC":
        print(f"Hoja {h}: {x.codificadores.str.contains(h).sum()} unidades")


def alfa_nominal(a, b):
    """Alfa de Krippendorff para dos codificadores, datos nominales, sin faltantes."""
    valores = np.concatenate([a, b])
    if len(set(valores)) < 2:
        return np.nan
    n = len(valores)
    observado = np.mean(a != b)
    _, cuenta = np.unique(valores, return_counts=True)
    esperado = (n ** 2 - (cuenta ** 2).sum()) / (n * (n - 1))
    return 1 - observado / esperado


def alfa():
    clave = pd.read_csv(VAL / "clave.csv")
    x = clave.copy()
    hojas = [c for c in "ABC" if (VAL / f"hoja_codificador_{c}.csv").exists()]
    for c in hojas:
        h = pd.read_csv(VAL / f"hoja_codificador_{c}.csv", dtype={"tema": "Int64"})
        x = x.merge(h[["unidad", "tema", "blanco"]].rename(columns={"tema": f"t_{c}", "blanco": f"b_{c}"}), on="unidad")
    # Cada unidad la codifican dos personas (asignacion.csv): se toman los dos códigos que tenga.
    def dos(fila, campo):
        v = [fila[f"{campo}_{c}"] for c in hojas if pd.notna(fila[f"{campo}_{c}"])]
        return (v + [pd.NA, pd.NA])[:2]
    x["tema_a"], x["tema_b"] = zip(*[dos(r, "t") for _, r in x.iterrows()])
    x["blanco_a"], x["blanco_b"] = zip(*[dos(r, "b") for _, r in x.iterrows()])
    faltan = x.tema_a.isna() | x.tema_b.isna()
    if faltan.any():
        print(f"Aviso: {faltan.sum()} unidades sin tema en alguna hoja; se dejan fuera.")
    x = x[~faltan]
    a, b = x.tema_a.to_numpy(int), x.tema_b.to_numpy(int)
    print(f"Alfa entre codificadores (tema): {alfa_nominal(a, b):.2f} en {len(x)} unidades "
          "(meta 0.80; 0.67 a 0.80 es tentativo)")
    for tipo, g in x.groupby("tipo"):
        print(f"  {tipo}: {alfa_nominal(g.tema_a.to_numpy(int), g.tema_b.to_numpy(int)):.2f} ({len(g)})")
    sec = x[x.tipo == "seccion"].dropna(subset=["blanco_a", "blanco_b"])
    if len(sec):
        print(f"Alfa del blanco (ítems de la sección): {alfa_nominal(sec.blanco_a.to_numpy(), sec.blanco_b.to_numpy()):.2f}")

    print("\nAlfa por tema (ese tema contra todos los demás):")
    for t in sorted(set(a) | set(b)):
        print(f"  {t:>2}: {alfa_nominal(a == t, b == t):.2f}  (usado {np.sum(a == t) + np.sum(b == t)} veces)")
    pares = x[x.tema_a != x.tema_b].apply(lambda r: tuple(sorted((r.tema_a, r.tema_b))), axis=1)
    if len(pares):
        print("\nPares de temas que más confundimos:", pares.value_counts().head(8).to_dict())

    # El modelo contra los casos en que los dos coincidimos.
    acuerdo = x[x.tema_a == x.tema_b].copy()
    modelo = {}
    if (CLAS / "temas_intervenciones.csv").exists():
        modelo.update(pd.read_csv(CLAS / "temas_intervenciones.csv").set_index("id").tema.dropna().astype(int))
    if (CLAS / "temas_seccion.csv").exists():
        s = pd.read_csv(CLAS / "temas_seccion.csv")
        modelo.update(dict(zip("s" + s.emision + "_" + s.item.astype(str), s.tema)))
    acuerdo["modelo"] = acuerdo.id.map(modelo)
    acuerdo = acuerdo.dropna(subset=["modelo"])
    if acuerdo.empty:
        print("\nTodavía no hay respuestas del modelo para comparar.")
        return
    acuerdo["acierta"] = acuerdo.modelo.astype(int) == acuerdo.tema_a.astype(int)
    print(f"\nAcierto del modelo donde coincidimos ({len(acuerdo)} unidades): {acuerdo.acierta.mean():.0%}")
    for bl, g in acuerdo.groupby("bloque"):
        print(f"  {bl}: {g.acierta.mean():.0%} ({len(g)})")
    por_tema = acuerdo.groupby(acuerdo.tema_a.astype(int)).acierta.agg(["mean", "size"])
    print("Acierto por tema:", {t: f"{m:.0%} de {n}" for t, (m, n) in por_tema.iterrows()})


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "alfa":
        alfa()
    elif len(sys.argv) > 1 and sys.argv[1] == "asignar":
        asignar()
    elif len(sys.argv) > 1 and sys.argv[1] == "reducir":
        reducir(*[int(v) for v in sys.argv[2:4]])
    else:
        muestra(*[int(v) for v in sys.argv[2:4]])
