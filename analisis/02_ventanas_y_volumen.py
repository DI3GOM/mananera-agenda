"""Arma las ventanas de cada emisión (2 sesiones antes, 2 después, mismo periodo
ordinario) y mide cuánto texto hay en las secciones libres de esas ventanas.

No usa temas: solo dice si hay suficiente material para estimar el modelo.
Salidas: datos/ventanas.csv y un resumen en pantalla.
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
LIBRES = {"iniciativas", "proposiciones", "agenda_politica", "intervenciones"}
OPOSICION = {"PAN", "PRI", "PRD", "MC"}


def periodo(fecha):
    """Periodos ordinarios: 1 sep a 15 dic y 1 feb a 30 abr."""
    if fecha.month >= 9:
        return f"{fecha.year}-otoño"
    if 2 <= fecha.month <= 4:
        return f"{fecha.year}-primavera"
    return None


def sesiones_lxv():
    cal = pd.read_csv(f"{RAIZ}/datos/calendario_sesiones.csv")
    cal = cal[(cal.legislatura == 65) & (cal.tipo == "ordinaria")].copy()
    cal["fecha"] = pd.to_datetime(cal.fecha)
    cal["sufijo"] = cal.sufijo.fillna("")
    cal["periodo"] = cal.fecha.map(periodo)
    cal["sesion"] = cal.fecha.dt.strftime("%Y-%m-%d") + cal.sufijo.map(lambda s: f"-{s}" if s else "")
    return cal.sort_values(["fecha", "sufijo"]).reset_index(drop=True)


def ventanas(cal, mismo_dia_es_post=True):
    emis = pd.read_csv(f"{RAIZ}/datos/emisiones_quien_es_quien.csv", parse_dates=["fecha"])
    filas = []
    for f in emis.fecha:
        per = periodo(f)
        if per is None:
            continue
        s = cal[cal.periodo == per]
        if s.empty or not (s.fecha.min() <= f <= s.fecha.max()):
            continue
        antes = s[s.fecha < f].tail(2)
        despues = s[s.fecha >= f] if mismo_dia_es_post else s[s.fecha > f]
        despues = despues.head(2)
        if len(antes) < 2 or len(despues) < 2:
            continue
        e = f.strftime("%Y-%m-%d")
        for k, ses in zip([-2, -1], antes.sesion):
            filas.append({"emision": e, "k": k, "sesion": ses})
        for k, ses in zip([1, 2], despues.sesion):
            filas.append({"emision": e, "k": k, "sesion": ses})
    return pd.DataFrame(filas)


def main():
    cal = sesiones_lxv()
    v = ventanas(cal)
    v0 = ventanas(cal, mismo_dia_es_post=False)
    print(f"Emisiones con ventana completa: {v.emision.nunique()} (si la sesión del mismo día no cuenta: {v0.emision.nunique()})")
    print(f"Sesiones distintas usadas: {v.sesion.nunique()}; lugares en ventanas: {len(v)}")
    reps = v.groupby("sesion").size()
    print("Ventanas en que aparece cada sesión:", reps.value_counts().sort_index().to_dict())
    v.to_csv(f"{RAIZ}/datos/ventanas.csv", index=False)

    t = pd.read_csv(f"{RAIZ}/datos/turnos_secciones.csv")
    t = t[t.rol == "diputado"].copy()
    t["sesion"] = t.fecha + t.sufijo.fillna("").map(lambda s: f"-{s}" if s else "")
    t["bloque"] = t.partido.map(lambda p: "oposicion" if p in OPOSICION else ("morena" if p == "MORENA" else "otro"))
    t["libre"] = t.seccion.isin(LIBRES)
    # Un "discurso" es un turno largo: una iniciativa o una intervención completa.
    t["discurso"] = t.palabras >= 150

    lib = t[t.libre]
    por_sesion = (lib.groupby(["sesion", "bloque"])
                  .agg(palabras=("palabras", "sum"), discursos=("discurso", "sum"))
                  .unstack("bloque", fill_value=0))
    por_sesion.columns = [f"{a}_{b}" for a, b in por_sesion.columns]
    vv = v.merge(por_sesion, left_on="sesion", right_index=True, how="left").fillna(0)

    tot = t.groupby(t.fecha.str[:4]).palabras.sum()
    libres = lib.groupby(lib.fecha.str[:4]).palabras.sum()
    print("\nParte de las palabras de diputados que cae en secciones libres, por año:")
    print((libres / tot).round(3).to_string())
    print("\nPalabras por sección (todas las sesiones LXV):")
    print((t.groupby("seccion").palabras.sum() / t.palabras.sum()).round(3).sort_values(ascending=False).to_string())
    print(f"\nPalabras 'desde la curul': {t[t.desde_curul].palabras.sum() / t.palabras.sum():.1%}")

    post = vv[vv.k > 0]
    pre = vv[vv.k < 0]
    for nombre, d in [("posteriores (k=+1,+2)", post), ("previas (k=-2,-1)", pre)]:
        op = d["palabras_oposicion"]
        mo = d["palabras_morena"]
        print(f"\nSesiones {nombre}: {len(d)} lugares")
        print(f"  sin palabras libres de la oposición: {(op == 0).mean():.0%}; de Morena: {(mo == 0).mean():.0%}")
        print(f"  mediana de palabras libres oposición: {op.median():.0f}; Morena: {mo.median():.0f}")
        print(f"  discursos libres largos de la oposición (suma): {d['discursos_oposicion'].sum():.0f}; Morena: {d['discursos_morena'].sum():.0f}")

    por_emision = post.groupby("emision")[["palabras_oposicion"]].sum()
    vacias = (por_emision.iloc[:, 0] == 0)
    print(f"\nEmisiones sin ninguna palabra libre de la oposición en sus dos sesiones posteriores: {vacias.sum()} de {len(por_emision)}")
    por_anio = post.assign(anio=post.emision.str[:4]).groupby("anio")["discursos_oposicion"].sum()
    print("Discursos libres largos de la oposición en sesiones posteriores, por año de emisión:", por_anio.to_dict())

    # Para la simulación de poder.
    lib.to_csv(f"{RAIZ}/datos/discursos_libres.csv", index=False,
               columns=["sesion", "fecha", "seccion", "orador", "partido", "bloque", "palabras", "discurso"])


if __name__ == "__main__":
    main()
