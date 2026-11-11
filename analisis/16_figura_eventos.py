"""Figuras del estudio de eventos con datos reales, para la presentación.

  figura_eventos_real.png      Todos los temas juntos: la salida de 11_estimar.py robustez
                               (especificación fijada en el plan).
  figura_eventos_por_tema.png  Un panel por tema: la salida de 15_eventos_por_tema.py
                               (EXPLORATORIO, decidido después de ver resultados).

No estima nada: solo lee los CSV de analisis/resultados.
Uso: python 16_figura_eventos.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "analisis" / "resultados"

OPOS, MORENA = "#1F6F8B", "#D9822B"
TEXTO, TEXTO_2, REJILLA, FONDO, SOMBRA = "#1F3D36", "#4B5A55", "#DDD5C6", "#F4EFE6", "#EAE2D3"
K = [-2, -1, 1, 2]
ETIQ = ["2 sesiones\nantes", "1 sesión\nantes", "1 sesión\ndespués", "2 sesiones\ndespués"]
X = np.arange(4)

plt.rcParams.update({
    "font.size": 13, "axes.edgecolor": TEXTO_2, "axes.labelcolor": TEXTO_2, "text.color": TEXTO,
    "xtick.color": TEXTO_2, "ytick.color": TEXTO_2, "axes.spines.top": False,
    "axes.spines.right": False, "legend.frameon": False, "figure.facecolor": FONDO,
    "axes.facecolor": FONDO, "savefig.facecolor": FONDO,
})


def serie(ev, bloque):
    """Coeficientes en k = -2, -1 (referencia, 0), +1, +2."""
    g = ev[ev.bloque.str.startswith(bloque)].copy()
    g["k"] = g.bloque.str.extract(r"k=(-?\d)").astype(int)
    g = g.set_index("k")
    c = [g.loc[k, "coef"] if k != -1 else 0 for k in K]
    lo = [g.loc[k, "ic_bajo"] if k != -1 else 0 for k in K]
    hi = [g.loc[k, "ic_alto"] if k != -1 else 0 for k in K]
    return np.array(c), np.array(lo), np.array(hi)


def panel(ax, ev, lim=None, grande=True):
    ax.axvspan(1.5, 3.6, color=SOMBRA, zorder=0)
    ax.axhline(0, color=TEXTO_2, lw=1.2, zorder=1)
    ax.grid(axis="y", color=REJILLA, lw=0.8, zorder=0)
    for bloque, color, marca, dx in [("oposicion", OPOS, "o", -0.1), ("morena", MORENA, "s", 0.1)]:
        c, lo, hi = serie(ev, bloque)
        x = X + dx
        if lim:
            lo_c, hi_c = np.clip(lo, *lim), np.clip(hi, *lim)
        else:
            lo_c, hi_c = lo, hi
        ax.vlines(x, lo_c, hi_c, color=color, lw=3 if grande else 2, zorder=2)
        if lim:
            for xi, l, h in zip(x, lo, hi):
                if l < lim[0]:
                    ax.plot(xi, lim[0], marker="v", color=color, ms=7, zorder=3)
                if h > lim[1]:
                    ax.plot(xi, lim[1], marker="^", color=color, ms=7, zorder=3)
        ax.plot(x, c, color=color, alpha=0.45, lw=1.5, zorder=2)
        ax.plot(x, c, marca, color=color, ms=11 if grande else 7, mec="white", mew=1.5, zorder=4,
                label="Oposición" if bloque == "oposicion" else "Morena")
    ax.set_xticks(X, ETIQ if grande else ["−2", "−1", "+1", "+2"])
    ax.set_xlim(-0.6, 3.6)
    if lim:
        ax.set_ylim(*lim)


def general():
    r = pd.read_csv(sorted(RES.glob("robustez_*.csv"))[-1])
    ev = r[r.modelo == "eventos"]
    fig, ax = plt.subplots(figsize=(11, 6.6), dpi=200)
    panel(ax, ev)
    ax.set_ylim(-11, 15)
    ax.text(0.5, 14.2, "Antes", ha="center", color=TEXTO_2, fontsize=15)
    ax.text(2.55, 14.2, "Después", ha="center", color=TEXTO, fontsize=15, weight="bold")
    ax.set_ylabel("Cambio en el % del discurso sobre el tema\n(puntos, contra los temas de control)")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, fontsize=14)
    ax.annotate("Referencia: la última sesión\nantes de la mañanera vale 0",
                xy=(1, 0), xytext=(0.95, -8.6), fontsize=12, color=TEXTO_2, ha="center",
                arrowprops=dict(arrowstyle="->", color=TEXTO_2))
    ax.text(3.55, -10.6, "Barras: intervalo de 95%. Si cruza el 0, no distinguimos el cambio de cero.",
            ha="right", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    fig.savefig(RAIZ / "analisis" / "figura_eventos_real.png")


def por_tema():
    r = pd.read_csv(sorted(RES.glob("eventos_por_tema_*.csv"))[-1])
    temas = list(dict.fromkeys(r.tema))
    n_emis = r.groupby("tema").emisiones.first()
    lim = (-30, 35)
    fig, axs = plt.subplots(2, 4, figsize=(16, 8), dpi=200, sharey=True)
    for ax, t in zip(axs.flat, temas):
        panel(ax, r[r.tema == t], lim=lim, grande=False)
        ax.set_title(f"{t}", fontsize=15, color=TEXTO, loc="left", weight="bold", pad=22)
        ax.text(0, 1.02, f"{n_emis[t]} emisiones con datos", transform=ax.transAxes, fontsize=11, color=TEXTO_2)
    leyenda = axs.flat[-1]
    leyenda.axis("off")
    h, l = axs.flat[0].get_legend_handles_labels()
    leyenda.legend(h, l, loc="upper left", fontsize=14)
    leyenda.text(0.02, 0.62, "Sesiones respecto a la mañanera:\n−2 y −1 antes, +1 y +2 después\n(zona sombreada).\n\n"
                 "Triángulo: el intervalo sigue\nmás allá de la escala.\n\nPocas emisiones por tema:\n"
                 "intervalos anchos y poco\nconfiables. Exploratorio.",
                 transform=leyenda.transAxes, va="top", fontsize=12, color=TEXTO_2)
    for ax in axs[:, 0]:
        ax.set_ylabel("Cambio (puntos)")
    fig.tight_layout()
    fig.savefig(RAIZ / "analisis" / "figura_eventos_por_tema.png")


if __name__ == "__main__":
    general()
    por_tema()
