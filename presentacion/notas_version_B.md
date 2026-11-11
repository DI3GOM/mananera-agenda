# Notas del orador, versión B

Lo que se dice en cada diapositiva de `version_B.pdf`.

## 1. ¿La mañanera fija la agenda de la oposición?

Somos el Equipo 1. Queremos saber si la sección de la mañanera que desmentía notas cambiaba de qué hablaban los diputados.

## 2. Cuando la sección desmiente una nota sobre un tema de política pública, ¿los diputados hablan más de ese tema en las dos sesiones siguientes?

De 2021 a 2024, cada miércoles la mañanera desmentía notas de medios y políticos. Preguntamos si, cuando esa sección toca un tema de política pública, los diputados hablan más de ese tema en las dos sesiones siguientes. Lo medimos para la oposición y para Morena por separado, y luego los comparamos. Importa porque la oposición es la que vigila: si el gobierno decide de qué se habla, también decide qué se vigila.

## 3. Dos teorías tiran en direcciones opuestas

Nos apoyamos en dos textos. Lovett, Bevan y Baumgartner encuentran que un presidente popular de Estados Unidos mueve las audiencias de los comités del Congreso con los temas de su informe; de ahí, que la oposición podría responder. Ellos no comparan partidos dentro de una cámara, y miden comités, no el Pleno: tomamos la idea, no la medida. Petrocik dice que en campaña cada partido enfatiza los temas en que tiene fama; llevarlo a la tribuna es extensión nuestra, y sugiere que la oposición preferiría sus temas. En el método, Olden y Møen justifican restar los dos bloques. Los temas vienen del Comparative Agendas Project, y de Simmons y coautores la disciplina de fijar el análisis antes de ver datos.

## 4. Cuatro escenarios, escritos antes de ver datos

Antes de ver datos escribimos qué significaría cada resultado. Si los dos bloques suben parecido, la mañanera mueve a toda la Cámara. Si Morena sube más, responde más el partido del Presidente. Si la oposición no sube, es compatible con que prefiera sus propios temas, como sugiere Petrocik. Y si ninguno sube, la sección no mueve la agenda de nadie, al menos no en un tamaño que podamos detectar.

## 5. Dos fuentes de texto, unidas por fecha

De la mañanera tenemos las 64 emisiones de la sección, con 317 desmentidos. De la Cámara, las versiones estenográficas del Pleno: 2,316 intervenciones en las partes donde el grupo elige de qué hablar, en 154 sesiones, dos antes y dos después de cada emisión. Y aquí está el tema de los ceros que nos pidió revisar: en 74 de esas 154 sesiones nadie habló en las secciones libres, porque fueron de dictámenes o comparecencias. Si un partido no habló, no hay porcentaje y la fila sale; si habló de otra cosa, vale cero.

## 6. Un modelo de lenguaje pone un tema a cada texto

Para saber de qué trata cada texto usamos agentes de Claude Opus 5.5 con un libro de códigos: los 21 temas del Comparative Agendas Project y una categoría para lo que no es política pública. Cada texto recibe un solo tema: “es falso que falten medicamentos” va a salud. Probamos el libro en dos pilotos con textos fuera de la muestra y lo congelamos. Al clasificar dos veces una parte, 92 de 100 intervenciones salieron iguales. Ser consistente no es acertar; para eso validamos a mano.

## 7. Por qué sirvió: la medida es buena y no favorece a ningún bloque

Codificamos a mano 160 textos al azar: 100 intervenciones, mitad de cada bloque, y 60 desmentidos. Dos personas por texto, sin ver partido, fecha ni lo que dijo el modelo. Nuestro acuerdo fue de 0.87, arriba de la meta de 0.80. Donde coincidimos, el modelo dice lo mismo en 95% de las intervenciones de oposición, 100% de Morena y 94% de la sección: sin una diferencia relevante entre bloques. Por eso sirvió: si el modelo acertara más con un bloque, la comparación estaría sesgada. Y nos dice algo para después: si no encontramos efecto, no es por mala medición.

## 8. Doble diferencia: el tema tocado contra los que nadie tocó

El ejemplo: un miércoles la sección toca salud. La oposición pasa de dedicarle 4% de su discurso a 6%. Los temas que nadie tocó no cambian. El efecto es de 2 puntos, que sobre 4% es 50% más. Un tema cuenta como tocado si la emisión anterior no lo tocó, para no medir una historia que ya venía. Hacemos lo mismo con Morena y restamos: si una noticia mueve a los dos bloques por igual, en la resta se cancela.

## 9. La lineal cae sobre el efecto real; el Poisson lo exagera

El profesor preguntó: ¿Poisson o lineal? Lo decidimos con una simulación antes de ver datos reales. Tomamos los discursos reales, pusimos temas al azar y metimos un efecto conocido. El círculo blanco es el efecto que pusimos; el punto verde, lo que estima la lineal, y cae encima. El punto naranja es el Poisson: con un efecto de 63% estima 90%, y con uno de 127% estima 221%. Los dos detectan el efecto casi igual de seguido, pero el Poisson exagera el tamaño, porque con cuatro sesiones por ventana y muchos ceros no logra quitar el nivel normal de cada grupo. Por eso la lineal es la principal y el Poisson va de robustez.

## 10. No detectamos que la sección mueva la agenda de ningún bloque

Este es el resultado. Después de la sección, la oposición dedica al tema tocado 1.4 puntos menos de su discurso, y Morena 0.3 más. Ninguno es distinto de cero, y la diferencia entre bloques tampoco. Antes de correrlo congelamos el plan en GitHub, y la especificación principal la corrimos una sola vez. Las seis variantes que fijamos, el Poisson y la permutación de fechas dicen lo mismo; están en el respaldo. En el estudio de eventos no hay evidencia de tendencias previas. Y 58 de las 64 emisiones aportan datos: en las otras seis las sesiones fueron solo de dictámenes.

## 11. Buena medición, poco poder: descartamos un efecto grande, no uno moderado

¿Son buenos los resultados? En dos partes. La medición y el diseño funcionaron: la medida es confiable y el placebo da cero, así que el nulo no viene de medir mal. Pero la prueba tiene poco poder. Podemos descartar un efecto grande: la oposición no sube más de unos 5 puntos, cerca de 66% sobre su base. No podemos descartar uno moderado: ya en la simulación detectábamos un efecto de 25% solo una de cada cuatro veces, y los datos reales salieron más ruidosos. Volviendo a los escenarios: el resultado es compatible con que la oposición prefiera sus temas y con que la sección no mueva a nadie, y no podemos separarlos.

## 12. Hacia el trabajo final del 7 de diciembre

Tres pasos para el trabajo final. Uno: la heterogeneidad que prometimos, por partido, por blanco del desmentido, antes y después de septiembre de 2023 y por sesión, una a la vez y marcada como exploratoria. Dos: medir el ángulo, porque un partido puede hablar del tema del rival para rebatirlo. Tres: más texto por ventana, para tener poder contra efectos moderados. Y una pregunta abierta, que creemos es lo que el profesor quiso decir con “cada partido se cree sus propios temas”: ¿responde la oposición cuando la sección toca uno de sus temas? Gracias.

## 13. Ninguna variante cambia la conclusión

Diapositiva de respaldo, para preguntas. Todas las variantes estaban fijadas en el plan congelado. Efectos en puntos porcentuales salvo el Poisson. Ninguna es significativa; el p más bajo, 0.22, es la diferencia sin pesos. En la sesión −2 no hay evidencia de tendencias previas.
