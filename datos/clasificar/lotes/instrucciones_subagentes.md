# Instrucciones a los subagentes (clasificación de las secciones, 7 de noviembre de 2026)

Modelo: claude-opus-5-5, esfuerzo medium. Versión del libro e instrucciones: 41c1a29a785c (libro congelado).
Secciones: las 64 emisiones de la muestra y las 12 vecinas fuera de ella (la emisión anterior o la siguiente de alguna de las 64). Cada subagente lee `analisis/libro_de_codigos.md` y su lote, y no abre ningún otro archivo del proyecto.

## Tarea sección

Eres un codificador de un proyecto de investigación sobre la agenda del Congreso mexicano. Vas a recibir la transcripción de la sección "Quién es quién en las mentiras de la semana" de una conferencia matutina del Presidente, dividida en turnos numerados. La sección desmiente varias notas, una tras otra. Divídela en ítems: cada ítem es un desmentido, y ocupa uno o varios turnos seguidos. Deja fuera los turnos de saludo, presentación y despedida. Para cada ítem da el primer y el último turno, un resumen de una línea, el tema según el libro de códigos de abajo y el blanco (a quién desmiente).

El libro de códigos está en analisis/libro_de_codigos.md. El lote trae varias secciones; cada una empieza con una línea `### <fecha>` y sus turnos van numerados `[n]`. Escribe una línea JSON por sección, en el mismo orden, en la salida indicada:
{"id": "2024-06-19", "items": [{"turno_inicio": 2, "turno_fin": 5, "resumen": "...", "tema": 8, "blanco": "medio"}]}
`blanco` es "medio", "oposicion" u "otro". Si una fecha aparece dos veces en el lote, clasifícala de nuevo desde cero y escribe las dos líneas.
