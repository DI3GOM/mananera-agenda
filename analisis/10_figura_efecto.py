"""Figura ilustrativa del efecto, con datos sintéticos.

Panel A: el ejemplo de la metodología (salud pasa de 4% a 6% y los temas de control no cambian).
Panel B: lo que estimó la lineal pesada en la simulación ya corrida
(resultados_simulacion_rediseno_7temas.csv). No procesa datos nuevos ni mira resultados reales.

Uso: python 10_figura_efecto.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "analisis" / "figura_efecto_sintetico.png"

OPOS, MORENA = "#2a78d6", "#eb6834"
TEXTO, TEXTO_2, GRIS, REJILLA = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"

plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": GRIS, "axes.labelcolor": TEXTO_2,
    "xtick.color": TEXTO_2, "ytick.color": TEXTO_2, "axes.spines.top": False,
    "axes.spines.right": False, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "legend.frameon": False,
})


def real():
    """Figura con datos reales: lee la última salida de 11_estimar.py principal y robustez."""
    res = RAIZ / "analisis" / "resultados"
    p = pd.read_csv(sorted(res.glob("principal_*.csv"))[-1])
    r = pd.read_csv(sorted(res.glob("robustez_*.csv"))[-1])
    filas = [("Principal: lineal ponderada", p)]
    for esp, nombre in [("lineal sin pesos", "Sin pesos"), ("66 emisiones", "66 emisiones"),
                        ("controles sin excluir", "Controles con e+1"), ("150 palabras", "Turnos de 150+ palabras"),
                        ("5 temas", "5 temas"), ("10 temas", "10 temas")]:
        g = r[r.especificacion.str.contains(esp, regex=False) & r.modelo.str.startswith("lineal")]
        if len(g):
            filas.append((nombre, g))
    ev = r[r.modelo == "eventos"]

    fig, (a, b) = plt.subplots(2, 1, figsize=(6.5, 7.4), height_ratios=[1.5, 1])
    for i, (nombre, g) in enumerate(filas):
        y0 = len(filas) - 1 - i
        for blq, color, dy in [("oposicion", OPOS, 0.17), ("morena", MORENA, -0.17)]:
            f = g[g.bloque == blq].iloc[0]
            a.plot([f.ic_bajo, f.ic_alto], [y0 + dy] * 2, color=color, lw=2.4 if i == 0 else 1.6,
                   solid_capstyle="round")
            a.plot(f.coef, y0 + dy, "o", color=color, ms=7 if i == 0 else 5.5, mec="white", mew=1.2)
        d = g[g.bloque == "diferencia"].iloc[0]
        a.text(1.02, y0, f"{d.p:.2f}", transform=a.get_yaxis_transform(), va="center", color=TEXTO, fontsize=8)
    a.text(1.02, len(filas) - 0.45, "p dif.", transform=a.get_yaxis_transform(), va="bottom",
           color=TEXTO_2, fontsize=8)
    a.axvline(0, color=GRIS, lw=1)
    a.axhspan(len(filas) - 1.5, len(filas) - 0.5, color="#f3f2ee", zorder=-1)
    a.set_yticks(range(len(filas)), [n for n, _ in reversed(filas)])
    a.tick_params(axis="y", length=0)
    a.spines["left"].set_visible(False)
    a.xaxis.grid(True, color=REJILLA, lw=0.8)
    a.set_axisbelow(True)
    a.set_xlabel("Cambio en el % del discurso dedicado al tema tocado (puntos porcentuales)")
    a.set_title("A. Efecto en las dos sesiones siguientes, con IC de 95%", pad=24)
    a.legend(handles=[plt.Line2D([], [], color=OPOS, lw=2, marker="o", mec="white", label="Oposición"),
                      plt.Line2D([], [], color=MORENA, lw=2, marker="o", mec="white", label="Morena")],
             loc="lower left", ncol=2, fontsize=8, bbox_to_anchor=(0, 0.99), borderaxespad=0)

    for blq, color, dx in [("oposicion", OPOS, -0.06), ("morena", MORENA, 0.06)]:
        g = ev[ev.bloque.str.startswith(blq)].copy()
        g["k"] = g.bloque.str.extract(r"k=(-?\d+)")[0].astype(int)
        g = pd.concat([g, pd.DataFrame({"k": [-1], "coef": [0.0], "ic_bajo": [0.0], "ic_alto": [0.0]})]).sort_values("k")
        x = g.k.map({-2: 0, -1: 1, 1: 2, 2: 3}) + dx
        b.vlines(x, g.ic_bajo, g.ic_alto, color=color, lw=1.6)
        b.plot(x, g.coef, "o-", color=color, ms=5.5, mec="white", mew=1.2, lw=1)
    b.axhline(0, color=GRIS, lw=1)
    b.axvline(1.5, color=GRIS, lw=1, ls=":")
    b.set_xticks([0, 1, 2, 3], ["−2", "−1 (ref.)", "+1", "+2"])
    b.yaxis.grid(True, color=REJILLA, lw=0.8)
    b.set_axisbelow(True)
    b.set_xlabel("Sesión respecto a la emisión")
    b.set_ylabel("Puntos porcentuales")
    b.set_title("B. Sesión por sesión (estudio de eventos)")

    f0 = p[p.bloque == "oposicion"].iloc[0]
    fig.suptitle("No detectamos que la oposición ni Morena hablen más del tema que tocó la sección", x=0.01, ha="left",
                 fontsize=11, fontweight="bold")
    fig.text(0.01, 0.005,
             f"Doble diferencia por bloque, mínimos cuadrados ponderados por las palabras del partido en la sesión, efectos fijos\n"
             f"partido×tema×emisión y partido×sesión×emisión, errores agrupados por emisión y sesión. N = {int(f0.n):,} filas, "
             f"{int(f0.emisiones)} emisiones con datos,\n7 temas más el resto. «p dif.»: prueba de oposición − Morena. "
             "Fuentes: NOSTRODATA y versiones estenográficas de la Cámara\nde Diputados, LXV Legislatura (2021–2024). "
             "Plan congelado antes de estimar (etiqueta plan-congelado).",
             fontsize=7, color=TEXTO_2, va="bottom")
    fig.tight_layout(rect=(0, 0.075, 0.95, 0.97), h_pad=2.5)
    salida = RAIZ / "analisis" / "figura_efecto_real.png"
    fig.savefig(salida, dpi=200, facecolor="white")
    print(salida)


if __name__ == "__main__" and len(__import__("sys").argv) > 1 and __import__("sys").argv[1] == "real":
    real()
    raise SystemExit

fig, (a, b) = plt.subplots(2, 1, figsize=(6.5, 7.2), height_ratios=[1, 1.15])

# Panel A: una ventana, la oposición y el tema salud.
x = [0, 1, 2, 3]
a.plot(x, [8, 8, 8, 8], color=GRIS, lw=2, marker="o", ms=6, label="Temas de control (promedio)")
a.plot([1, 2, 3], [4, 4, 4], color=OPOS, lw=1.5, ls="--", label="Salud sin la mañanera (como el control)")
a.plot(x, [4, 4, 6, 6], color=OPOS, lw=2, marker="o", ms=6, label="Salud, tema tocado")
a.axvline(1.5, color=GRIS, lw=1, ls=":")
a.text(1.5, 9.6, "Miércoles: la sección toca salud", ha="center", va="top", color=TEXTO_2,
       bbox={"fc": "white", "ec": "none", "pad": 1})
a.annotate("", xy=(3.18, 6), xytext=(3.18, 4), arrowprops={"arrowstyle": "<->", "color": TEXTO, "lw": 1})
a.text(3.26, 5, "Efecto:\n2 puntos\n(+50% sobre 4%)", va="center", color=TEXTO)
a.set_xticks(x, ["−2", "−1", "+1", "+2"])
a.set_xlim(-0.3, 3.9)
a.set_ylim(0, 10)
a.set_yticks([0, 2, 4, 6, 8, 10], ["0%", "2%", "4%", "6%", "8%", "10%"])
a.yaxis.grid(True, color=REJILLA, lw=0.8)
a.set_axisbelow(True)
a.set_xlabel("Sesión respecto a la emisión")
a.set_ylabel("% del discurso de la oposición")
a.set_title("A. Cómo se mide: el ejemplo del texto")
a.legend(loc="lower left", fontsize=8)

# Panel B: mediana y 90% central de las estimaciones simuladas.
r = pd.read_csv(RAIZ / "analisis" / "resultados_simulacion_rediseno_7temas.csv")
escenarios = [("solo_oposicion", 0.0, "Sin efecto"),
              ("solo_oposicion", 0.25, "Solo la oposición, +25%"),
              ("solo_oposicion", 0.5, "Solo la oposición, +50%"),
              ("ambos", 0.5, "Los dos bloques, +50%")]
for fila, (esc, tau, nombre) in enumerate(escenarios):
    g = r[(r.escenario == esc) & (r.tau == tau)]
    y0 = len(escenarios) - 1 - fila
    for blq, color, dy, reacciona in [("o", OPOS, 0.17, tau > 0),
                                      ("m", MORENA, -0.17, esc == "ambos")]:
        est = g[f"lineal_pesos_{blq}_est"]
        y = y0 + dy
        b.plot([est.quantile(0.05), est.quantile(0.95)], [y, y], color=color, lw=2,
               solid_capstyle="round")
        b.plot(est.median(), y, "o", color=color, ms=7, mec="white", mew=1.5)
        verdadero = g.verdadero_lineal.mean() if reacciona else 0
        b.plot(verdadero, y, marker="|", color=TEXTO, ms=11, mew=1.5)
        b.text(1.03, y, f"{(g[f'lineal_pesos_{blq}_p'] < 0.05).mean():.0%}",
               transform=b.get_yaxis_transform(), va="center", color=TEXTO)
b.text(1.03, len(escenarios) - 0.45, "Detecta", transform=b.get_yaxis_transform(),
       va="bottom", color=TEXTO_2, fontsize=8)
b.axvline(0, color=GRIS, lw=1)
b.set_yticks(range(len(escenarios)), [e[2] for e in reversed(escenarios)])
b.tick_params(axis="y", length=0)
b.set_ylim(-0.6, len(escenarios) - 0.4)
b.set_xlim(-0.5, 1.5)
b.set_xticks([-0.5, 0, 0.5, 1, 1.5], ["−50%", "0", "+50%", "+100%", "+150%"])
b.xaxis.grid(True, color=REJILLA, lw=0.8)
b.set_axisbelow(True)
b.spines["left"].set_visible(False)
b.set_xlabel("Efecto estimado, sobre el nivel previo del tema")
b.set_title("B. Qué tan bien lo recupera la regresión", pad=24)
b.legend(handles=[
    plt.Line2D([], [], color=OPOS, lw=2, marker="o", mec="white", label="Oposición"),
    plt.Line2D([], [], color=MORENA, lw=2, marker="o", mec="white", label="Morena"),
    plt.Line2D([], [], color=TEXTO, ls="none", marker="|", ms=11, mew=1.5, label="Efecto verdadero"),
], loc="lower left", fontsize=8, ncol=3, bbox_to_anchor=(0, 0.99), borderaxespad=0)

fig.text(0.01, 0.005,
         "Datos sintéticos, no son resultados del proyecto. En B hay 100 simulaciones por escenario: el punto es la mediana,\n"
         "la línea cubre 9 de cada 10 simulaciones y «Detecta» es el porcentaje con p < 0.05. Temas inventados asignados\n"
         "al azar a los discursos reales, 7 temas más el resto (analisis/05_simulacion_rediseno.py).",
         fontsize=7, color=TEXTO_2, va="bottom")
fig.tight_layout(rect=(0, 0.06, 0.95, 1), h_pad=2.5)
fig.savefig(SALIDA, dpi=200, facecolor="white")
print(SALIDA)
