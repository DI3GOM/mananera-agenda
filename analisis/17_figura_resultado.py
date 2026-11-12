"""La figura de resultados para la presentación, en formato afirmación y evidencia.
 
Lee la última salida de 11_estimar.py principal (analisis/resultados/principal_*.csv) y guarda
presentacion/figura_resultado.png. No estima nada: todos los números salen del CSV.
 
Uso: python analisis/15_figura_resultado.py
"""
from pathlib import Path
 
import matplotlib.pyplot as plt
import pandas as pd
 
RAIZ = Path(__file__).resolve().parents[1]
OPOS, MORENA, DIF = "#2a78d6", "#eb6834", "#1f1f1e"
TEXTO, TEXTO_2, GRIS, REJILLA = "#1f1f1e", "#52514e", "#8a8984", "#e4e3df"
 
 
def pp(x):
    """Número con signo y signo de menos tipográfico: −1.4, +0.3."""
    return f"{x:+.1f}".replace("-", "−")
 
 
def main():
    res = RAIZ / "analisis" / "resultados"
    p = pd.read_csv(sorted(res.glob("principal_*.csv"))[-1]).set_index("bloque")
    o, m, d = p.loc["oposicion"], p.loc["morena"], p.loc["diferencia"]
 
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                         "axes.edgecolor": GRIS, "xtick.color": TEXTO_2, "ytick.color": TEXTO_2})
    fig, ax = plt.subplots(figsize=(11, 6.8))
    filas = [("Oposición\n(PAN, PRI, PRD y MC)", o, OPOS), ("Morena", m, MORENA),
             ("Diferencia\n(oposición − Morena)", d, DIF)]
    for i, (nombre, f, color) in enumerate(filas):
        y = len(filas) - 1 - i
        # Intervalo de 95%: la línea, con sus extremos marcados y rotulados.
        ax.plot([f.ic_bajo, f.ic_alto], [y, y], color=color, lw=4, solid_capstyle="butt", zorder=2)
        for x in (f.ic_bajo, f.ic_alto):
            ax.plot([x, x], [y - 0.09, y + 0.09], color=color, lw=2.5, zorder=2)
            ax.text(x, y - 0.17, pp(x), ha="center", va="top", fontsize=10.5, color=TEXTO_2)
        # Estimación: el punto, con su valor encima.
        ax.plot(f.coef, y, "o", color=color, ms=13, mec="white", mew=2, zorder=3)
        ax.text(f.coef, y + 0.15, f"{pp(f.coef)} pp", ha="center", va="bottom", fontsize=13,
                fontweight="bold", color=TEXTO, zorder=4,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))
        ax.text(1.01, y, f"p = {f.p:.2f}", transform=ax.get_yaxis_transform(), va="center",
                fontsize=11.5, color=TEXTO_2)
 
    # Rótulo que dice qué es la línea, sobre la primera fila.
    ax.annotate("Intervalo de confianza de 95%", xy=(o.ic_bajo + 0.6, len(filas) - 1 + 0.03),
                xytext=(o.ic_bajo - 0.2, len(filas) - 0.42), fontsize=11, color=OPOS, ha="left",
                arrowprops=dict(arrowstyle="-", color=OPOS, lw=1))
    ax.axvline(0, color=TEXTO_2, lw=1.4, zorder=1)
    ax.text(0.15, len(filas) - 0.38, "0 = sin efecto", ha="left", va="center", fontsize=10.5, color=TEXTO_2)
 
    ax.set_yticks(range(len(filas)), [n for n, _, _ in reversed(filas)], fontsize=12.5)
    ax.tick_params(axis="y", length=0)
    for lado in ["top", "right", "left"]:
        ax.spines[lado].set_visible(False)
    ax.set_ylim(-0.75, len(filas) - 0.3)
    ax.set_xlim(-10, 8)
    ax.xaxis.grid(True, color=REJILLA, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Cambio en el % del discurso dedicado al tema tocado en las dos sesiones siguientes "
                  "(puntos porcentuales, pp)", color=TEXTO_2, labelpad=10)
 
    # Afirmación y evidencia: el título dice el hallazgo con sus números.
    fig.suptitle(f"La mañanera no movió la agenda: la oposición cambió {pp(o.coef)} pp y Morena {pp(m.coef)} pp,\n"
                 "y ninguno de los dos cambios se distingue de cero", x=0.012, y=0.975, ha="left",
                 fontsize=16, fontweight="bold", color=TEXTO, linespacing=1.3)
    fig.text(0.012, 0.85,
             "Cambio en el discurso sobre el tema tocado tras la emisión.",
             fontsize=12, color=TEXTO_2, va="top", linespacing=1.45)
    fig.text(0.012, 0.012,
             "Doble diferencia por bloque, mínimos cuadrados ponderados por las palabras del partido en la sesión, "
             "errores agrupados por emisión y sesión.\n"
             f"N = {int(o.n):,} observaciones partido × tema × sesión, {int(o.emisiones)} emisiones de "
             "“Quién es quién en las mentiras”, 7 temas más el resto. Una sola corrida del plan congelado.\n"
             "Fuentes: NOSTRODATA y versiones estenográficas de la Cámara de Diputados, LXV Legislatura (2021–2024).",
             fontsize=9, color=TEXTO_2, va="bottom", linespacing=1.45)
    fig.subplots_adjust(left=0.19, right=0.86, top=0.75, bottom=0.25)
    salida = RAIZ / "presentacion" / "figura_resultado.png"
    fig.savefig(salida, dpi=200, facecolor="white")
    print(salida)
 
 
if __name__ == "__main__":
    main()
 