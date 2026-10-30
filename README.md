# ¿La mañanera fija la agenda de la oposición?

Equipo 1 (Diego Méndez, Tania Hernández, Paola Carmona) · Tópicos de Políticas Públicas II, otoño 2026.

Medimos si, cuando "Quién es quién en las mentiras" trata un tema, la oposición (PAN, PRI, PRD y MC) habla más de ese tema en la Cámara de Diputados que Morena en las sesiones siguientes. LXV Legislatura, 2021–2024.

## Qué hay aquí

| Carpeta | Contenido |
|---|---|
| `analisis/` | Los scripts, numerados en el orden en que se corren |
| `datos/` | Datos crudos: versiones estenográficas, mañaneras, calendario y emisiones |
| `papers/` | Los artículos que citamos (solo para el equipo; no compartir fuera del repo) |

### Datos

| Archivo | Qué es |
|---|---|
| `datos/estenograficas/` | Versiones estenográficas del Pleno (LXIV a LXVI), una por sesión, bajadas de la Gaceta Parlamentaria |
| `datos/calendario_sesiones.csv` | Todas las sesiones con su tipo (ordinaria, solemne, Permanente, Congreso General) y su archivo |
| `datos/emisiones_quien_es_quien.csv` | Fechas de cada emisión de la sección y cómo se detectó |
| `datos/mananeras.parquet` | Transcripciones de las mañaneras, del repositorio NOSTRODATA |
| `datos/fichas_diputados.csv` | Partido de cada diputado, por legislatura |
| `datos/comisiones_panel.csv` | Comisiones de cada diputado |

## Cómo empezar

Se necesita Python 3.11 o más reciente.

```bash
git clone https://github.com/DI3GOM/mananera-agenda.git
cd mananera-agenda
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cómo correr el análisis

Los scripts van en orden. Cada uno lee lo que dejó el anterior en `datos/`.

```bash
python analisis/01_turnos_por_seccion.py
python analisis/02_ventanas_y_volumen.py
python analisis/03_simulacion_poder.py 100
```

| Script | Qué hace | Tarda |
|---|---|---|
| `01_turnos_por_seccion.py` | Divide cada versión estenográfica de la LXV en turnos de palabra, con el partido del orador y la sección de la sesión (iniciativas, dictámenes, etc.). Crea `datos/turnos_secciones.csv` | ~5 s |
| `02_ventanas_y_volumen.py` | Arma las ventanas de cada emisión (2 sesiones antes y 2 después) y mide cuánto texto hay en las secciones libres. Crea `datos/ventanas.csv` y `datos/discursos_libres.csv` | ~5 s |
| `03_simulacion_poder.py` | Simulación de poder con temas asignados al azar: si hubiera un efecto, ¿lo detectaríamos? Acepta una variante: `colapsado`, `fe_simple` o `fe_periodo` | ~2 min por cada 100 simulaciones |

Los resultados de las simulaciones que ya corrimos están en `analisis/resultados_simulacion_poder*.csv`.

## Reglas del equipo

- **No mirar resultados antes de congelar el diseño.** Mientras no fijemos el clasificador, los temas y la ecuación, nadie compara las emisiones de la muestra con lo que dijo la oposición. Si necesitan un ejemplo, tómenlo de una emisión que no entra en la muestra.
- **Decisión pendiente:** `02_ventanas_y_volumen.py` todavía arma las ventanas contando la sesión del mismo miércoles como posterior (66 emisiones). El borrador de la metodología propone no contarla (64 emisiones). Cuando lo decidamos, se cambia `mismo_dia_es_post` en ese script.
- **Los archivos generados no se suben.** `turnos_secciones.csv`, `ventanas.csv` y `discursos_libres.csv` se recrean con los scripts.

## Cómo trabajar con git (lo básico)

Antes de empezar, bajen lo que subieron las demás:

```bash
git pull
```

Para guardar y compartir sus cambios:

```bash
git add analisis/mi_script.py
git commit -m "Describe en una frase qué cambiaste"
git push
```

Si van a cambiar algo grande, mejor en una rama propia y luego abren un pull request en GitHub:

```bash
git checkout -b nombre-de-la-rama
```
