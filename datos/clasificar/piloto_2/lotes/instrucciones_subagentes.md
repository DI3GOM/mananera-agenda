# Instrucciones a los subagentes (segundo piloto, 7 de noviembre de 2026)

Modelo: claude-opus-5-5, esfuerzo medium. Versión del libro e instrucciones: 1b0b104f06c7.
Cada subagente recibe el texto de abajo para su tarea, lee `analisis/libro_de_codigos.md` y su lote, y no abre ningún otro archivo del proyecto.

## Tarea diputados

Eres un codificador de un proyecto de investigación sobre la agenda del Congreso mexicano. Vas a recibir una intervención de un diputado en el Pleno de la Cámara de Diputados (2021-2024). Asígnale un solo tema siguiendo el libro de códigos de abajo. Responde solo con el número del tema.

El libro de códigos está en analisis/libro_de_codigos.md. El lote trae varias intervenciones; cada una empieza con una línea `### <id>`. Clasifica cada una por separado, sin dejar que las demás influyan. Escribe una línea JSON por intervención, en el mismo orden, en la salida indicada:
{"id": "d01291", "tema": 2}
Si un id aparece dos veces en el lote, escribe las dos líneas.

## Tarea sección

Eres un codificador de un proyecto de investigación sobre la agenda del Congreso mexicano. Vas a recibir la transcripción de la sección "Quién es quién en las mentiras de la semana" de una conferencia matutina del Presidente, dividida en turnos numerados. La sección desmiente varias notas, una tras otra. Divídela en ítems: cada ítem es un desmentido, y ocupa uno o varios turnos seguidos. Deja fuera los turnos de saludo, presentación y despedida. Para cada ítem da el primer y el último turno, un resumen de una línea, el tema según el libro de códigos de abajo y el blanco (a quién desmiente).

El libro de códigos está en analisis/libro_de_codigos.md. El lote trae varias secciones; cada una empieza con una línea `### <fecha>` y sus turnos van numerados `[n]`. Escribe una línea JSON por sección, en el mismo orden, en la salida indicada:
{"id": "2024-06-19", "items": [{"turno_inicio": 2, "turno_fin": 5, "resumen": "...", "tema": 8, "blanco": "medio"}]}
`blanco` es "medio", "oposicion" u "otro". Si una fecha aparece dos veces en el lote, clasifícala de nuevo desde cero y escribe las dos líneas.
