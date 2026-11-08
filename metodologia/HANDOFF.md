# Handoff: de la clasificación al resultado

7 de noviembre de 2026. Para el agente que sigue con el trabajo. Antes de empezar: `git pull` (Tania también hace push) y usa `.venv/bin/python` (pyfixest 0.60).

## Contexto

- Equipo 1 (Diego Méndez, Tania Hernández, Paola Carmona), Tópicos de Políticas Públicas II, Prof. Simpser. Repo público: github.com/DI3GOM/mananera-agenda.
- Pregunta: cuando "Quién es quién en las mentiras" toca un tema de política pública, ¿la oposición (PAN, PRI, PRD, MC) y Morena hablan más de ese tema en las dos sesiones siguientes de la LXV?
- Fechas: presentación el **jueves 12 de noviembre** (12 minutos, como versión final, una figura); trabajo final el **7 de diciembre**. Plan B, decidido: si el lunes 9 no hay alfa o no hay plan congelado, se presenta el diseño, la validación y la figura simulada marcada como tal.
- Metodología entregada: `metodologia/metodologia_v3.Rmd` (y `.pdf`). Es el compromiso público; el plan de análisis debe decir lo mismo o declarar qué cambia.

## Reglas que no se rompen

- **No ver resultados antes de congelar.** Nadie ha visto todavía el efecto real (nada por bloque antes/después). `11_estimar.py principal`, `robustez` y `permutacion` exigen la etiqueta git `plan-congelado`, que todavía **no existe**. No la crees sin el OK de Diego.
- Todo lo que se decida después de ver resultados va en una sección "Análisis exploratorio".
- Cada corrida con datos reales queda en `analisis/registro_corridas.csv` (lo hace 11 solo).
- Nunca probar especificaciones hasta que una salga significativa, ni contar cuántas salen.
- Citas: no atribuir a un texto nada que no se haya leído en él (`metodologia/guia_citas.md`). No citar papers para justificar el LLM. No subir PDFs de JSTOR.
- Git: commit o push solo si Diego lo pide; sin líneas de atribución en los commits.
- Diego prefiere cambios mínimos y puntuales a los textos del equipo, no reescrituras. Responde en español.

## Diseño (no reabrirlo)

- Doble diferencia apilada por bloque en una regresión: Y_ptse = β_O·Opos×Toc×Post + β_M·Morena×Toc×Post + α_pte + γ_pse + ε. Lineal ponderada por las palabras del partido en la sesión; Y = 100·W_ptse/W_pse; errores agrupados por emisión y sesión. Principal: β_O ≠ 0 a dos colas, 5%; segunda prueba: β_O − β_M.
- 64 emisiones (sin la sesión de la tarde del mismo miércoles). Ventana: 2 sesiones antes y 2 después, mismo periodo ordinario.
- Tratado: tocado por e y no por e−1. Control: no tocado por e−1, e ni e+1. Resto por ventana. "La anterior" y "la siguiente" son las emisiones de la semana anterior y siguiente aunque caigan fuera de las 64.
- Robustez (fijada): Poisson, lineal sin pesos, 66 emisiones, controles sin excluir e+1, solo intervenciones de 150+ palabras, 5 y 10 temas, estudio de eventos (referencia: sesión −1; β en −2 = tendencias previas), permutación de fechas.
- Heterogeneidad (exploratoria, una a la vez): por partido de oposición, por blanco del ítem, antes/después de septiembre de 2023, primera vs. segunda sesión.

## Lo hecho al 7 de noviembre (todo en GitHub)

- **Clasificación** por subagentes de Claude Opus 5.5, esfuerzo medio, sin API (lotes con `07_clasificar.py --lotes`, salidas en `datos/clasificar/salidas/`, `--importar`). Libro de códigos `analisis/libro_de_codigos.md`, huella ffdd8fb29d15.
  - Dos pilotos fuera de muestra (`datos/clasificar/piloto_1`, `piloto_2`).
  - 76 secciones (64 + 12 vecinas): 317 ítems; 6 de 8 repetidas iguales.
  - 2,316 intervenciones de las sesiones de las ventanas: 92 de 100 repetidas iguales.
  - Aclaración posterior: campañas de bots #NarcoPresidente van en 0 (8 ítems, `datos/clasificar/recodificaciones.csv`).
  - `06` corta mejor el final de la sección (la del 2023-12-13 traía el informe de seguridad).
- **Temas** (`12_elegir_temas.py`): sección en ≥ 8 emisiones y ≥ 1% de las palabras de los diputados (todas juntas). 7 temas: 20 Gobierno, 12 Justicia, 10 Transporte, 8 Energía, 3 Salud, 1 Economía, 2 Derechos civiles. Listas de 5 y 10 en `temas_elegidos_5.csv` y `_10.csv`. Provisionales hasta el alfa por tema (si dos se confunden, se juntan en `TEMAS_JUNTOS`).
- **Tubería** `11_estimar.py`: prueba simulada (+50% → estima +57%, verdadero +62%), descriptivos, placebo con 200 corridas (media ≈ 0, 6% de rechazos, errores bien calibrados).
- **Validación a mano**: muestra de 230 unidades (150 intervenciones, 80 ítems) en `datos/validacion/`. Cada unidad la codifican dos de tres (A Tania, B Paola, C Diego; `asignacion.csv`, 153-154 por persona). Se codifica en la página https://claude.ai/artifact/Q2b6azTqbge7jEvdrnqzJ2 (cuenta de Diego; cada quien guarda en `codigos/<id>`; nadie ve las respuestas de los otros). Para pasarlas al análisis: bajar la colección `codigos` con ArtifactData (`list`, `out_dir`) y correr `13_bajar_codificacion.py <carpeta>`; luego `08_validacion.py alfa`. Solo la cuenta de Diego (dueño) puede leer esas respuestas.

## Lo que falta, en orden

1. **Decisión pendiente de Diego:** ¿reducir la validación a 100 intervenciones (50/50) y 60 ítems? Se propuso para ahorrar tiempo; solo vale si se decide antes de que alguien codifique. Si se aprueba: subconjunto estratificado de la muestra actual, rehacer `asignacion.csv` y la página.
2. Tania pasa las 13 correcciones a su plan (están en `notas/10-correcciones-al-plan-final.md`, solo en la Mac de Diego; pídeselas si no las tienes). El plan corregido se guarda en `metodologia/` y se pone la etiqueta `plan-congelado` (con el OK de Diego).
3. Codificación a mano → `08_validacion.py alfa`. Si el alfa sale entre 0.67 y 0.80 se reporta como tentativo; debajo de 0.67 se juntan una vez los temas que más se confunden. Revisar el acierto del modelo por bloque.
4. Fijar temas con el alfa por tema (`12_elegir_temas.py`) y volver a correr descriptivos.
5. `11_estimar.py principal` **una sola vez**, luego `robustez` y `permutacion`. Reportar todo, salga como salga.
6. Figura con datos reales: adaptar `10_figura_efecto.py` (hoy solo sintética) para leer la salida de 11. Tres títulos preparados: la oposición reacciona y Morena no; ninguno reacciona; los dos igual.
7. Pendiente con el profesor: qué quiso decir con "cada partido se cree sus propios temas" (hay un borrador de correo en `notas/10`).
