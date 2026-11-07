# Instrucciones a los subagentes (clasificación de las intervenciones, 7 de noviembre de 2026)

Modelo: claude-opus-5-5, esfuerzo medium. Versión del libro e instrucciones: ffdd8fb29d15 (libro congelado más la aclaración de las campañas de bots).
Intervenciones: las de las sesiones que entran en alguna ventana (64 emisiones, o 66 si cuenta la sesión del mismo miércoles). Cada subagente lee `analisis/libro_de_codigos.md` y su lote, y no abre ningún otro archivo del proyecto. El lote no trae partido, orador ni fecha.

## Tarea diputados

Eres un codificador de un proyecto de investigación sobre la agenda del Congreso mexicano. Vas a recibir una intervención de un diputado en el Pleno de la Cámara de Diputados (2021-2024). Asígnale un solo tema siguiendo el libro de códigos de abajo. Responde solo con el número del tema.

El libro de códigos está en analisis/libro_de_codigos.md. El lote trae varias intervenciones; cada una empieza con una línea `### <id>`. Clasifica cada una por separado, sin dejar que las demás influyan. Escribe una línea JSON por intervención, en el mismo orden, en la salida indicada:
{"id": "d01291", "tema": 2}
