"""Codificación a mano en Excel (alternativa a la página web).

  armar   Escribe un Excel por codificador en datos/validacion/excel/ con solo sus
          unidades (asignacion.csv): A Tania, B Paola, C Diego. No dice partido, fecha
          ni lo que contestó el modelo. Tema y blanco se eligen de una lista; el libro
          de códigos va en la segunda pestaña.
  leer    Lee los Excel llenos y pasa tema, blanco y notas a las hojas
          hoja_codificador_A/B/C.csv. Después: 08_validacion.py alfa.

Uso: python 14_hojas_excel.py armar
     python 14_hojas_excel.py leer <codificacion_A.xlsx> [<codificacion_B.xlsx> ...]
"""
import re
import sys
from pathlib import Path

import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

RAIZ = Path(__file__).resolve().parents[1]
VAL = RAIZ / "datos" / "validacion"
SALIDA = VAL / "excel"
NOMBRES = {"A": "Tania", "B": "Paola", "C": "Diego"}
TEMAS = [(1, "Economía"), (2, "Derechos civiles"), (3, "Salud"), (4, "Agricultura"), (5, "Trabajo"),
         (6, "Educación"), (7, "Medio ambiente"), (8, "Energía"), (9, "Migración"), (10, "Transporte"),
         (12, "Justicia y seguridad"), (13, "Bienestar social"), (14, "Vivienda"),
         (15, "Comercio interno y finanzas"), (16, "Defensa"), (17, "Tecnología y comunicaciones"),
         (18, "Comercio exterior"), (19, "Asuntos internacionales"), (20, "Gobierno"),
         (21, "Territorio y recursos públicos"), (23, "Cultura"), (0, "Sin tema de política")]
BLANCOS = ["medio", "oposicion", "otro"]
TIPO = {"diputado": "Intervención de diputado", "seccion": "Ítem de la sección"}


def armar():
    asig = pd.read_csv(VAL / "asignacion.csv")
    libro = (RAIZ / "analisis" / "libro_de_codigos.md").read_text(encoding="utf-8")
    SALIDA.mkdir(exist_ok=True)
    gris = PatternFill("solid", fgColor="DDDDDD")
    for h, nombre in NOMBRES.items():
        t = pd.read_csv(VAL / f"hoja_codificador_{h}.csv")
        t = t[t.unidad.isin(asig[asig.codificadores.str.contains(h)].unidad)]
        wb = Workbook()
        ws = wb.active
        ws.title = "Codificar"
        ws.append(["unidad", "tipo", "texto", "tema", "blanco", "notas"])
        for r in t.itertuples():
            ws.append([r.unidad, TIPO[r.tipo], r.texto, None, None, None])
        for c in ws[1]:
            c.font = Font(bold=True)
        for col, ancho in zip("ABCDEF", [8, 14, 110, 30, 14, 30]):
            ws.column_dimensions[col].width = ancho
        for fila in ws.iter_rows(min_row=2):
            for c in fila:
                c.alignment = Alignment(wrap_text=True, vertical="top")
            if fila[1].value == TIPO["diputado"]:
                fila[4].fill = gris  # el blanco solo se llena en los ítems de la sección
        ws.freeze_panes = "D2"
        n = ws.max_row
        # Listas para elegir
        lst = wb.create_sheet("listas")
        for i, (num, nom) in enumerate(TEMAS, 1):
            lst.cell(i, 1, f"{num} {nom}")
        for i, b in enumerate(BLANCOS, 1):
            lst.cell(i, 2, b)
        lst.sheet_state = "hidden"
        dv_t = DataValidation(type="list", formula1=f"=listas!$A$1:$A${len(TEMAS)}", allow_blank=True,
                              showErrorMessage=True, error="Elige un tema de la lista.")
        dv_b = DataValidation(type="list", formula1=f"=listas!$B$1:$B${len(BLANCOS)}", allow_blank=True,
                              showErrorMessage=True, error="Elige medio, oposicion u otro.")
        ws.add_data_validation(dv_t)
        ws.add_data_validation(dv_b)
        dv_t.add(f"D2:D{n}")
        dv_b.add(f"E2:E{n}")
        # Libro de códigos
        lb = wb.create_sheet("Libro de códigos", 1)
        lb.column_dimensions["A"].width = 140
        for i, linea in enumerate(libro.splitlines(), 1):
            c = lb.cell(i, 1, linea)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        f = SALIDA / f"codificacion_{h}_{nombre}.xlsx"
        wb.save(f)
        print(f"{f.relative_to(RAIZ)}: {len(t)} unidades ({(t.tipo == 'seccion').sum()} ítems de la sección)")


def leer(archivos):
    asig = pd.read_csv(VAL / "asignacion.csv")
    for a in archivos:
        h = re.search(r"codificacion_([ABC])", Path(a).name)
        if not h:
            sys.exit(f"{a}: el nombre debe empezar con codificacion_A, _B o _C.")
        h = h.group(1)
        x = pd.read_excel(a, sheet_name="Codificar", dtype=str)
        x["tema"] = x.tema.str.extract(r"^\s*(\d+)")[0].astype("Int64")
        r = x.set_index("unidad")
        hoja = VAL / f"hoja_codificador_{h}.csv"
        t = pd.read_csv(hoja)
        t["tema"] = t.unidad.map(r.tema).astype("Int64")
        t["blanco"] = t.unidad.map(r.blanco)
        t["notas"] = t.unidad.map(r.notas)
        t.to_csv(hoja, index=False)
        mias = t.unidad.isin(asig[asig.codificadores.str.contains(h)].unidad)
        falta = (mias & t.tema.isna()).sum() + (mias & (t.tipo == "seccion") & t.blanco.isna()).sum()
        print(f"Hoja {h}: {t.tema.notna().sum()} de {mias.sum()} asignadas con tema; {falta} campos por llenar.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "armar":
        armar()
    elif len(sys.argv) > 2 and sys.argv[1] == "leer":
        leer(sys.argv[2:])
    else:
        sys.exit(__doc__)
