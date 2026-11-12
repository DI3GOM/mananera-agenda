# Notas del orador, versión C

Lo que se dice en cada diapositiva de `version_C.pdf`.

## 1. ¿La mañanera fija la agenda de la oposición?

Somos el Equipo 1. Queremos saber si la sección de la mañanera que desmentía notas cambiaba de qué hablaban los diputados.

## 2. Cuando la sección desmiente una nota sobre un tema de política pública, ¿los diputados hablan más de ese tema en las dos sesiones siguientes?

De 2021 a 2024, cada miércoles la mañanera desmentía notas de medios y políticos. Preguntamos si, cuando esa sección toca un tema de política pública, los diputados hablan más de ese tema en las dos sesiones siguientes. Lo medimos para la oposición y para Morena, y luego comparamos. Importa porque la oposición vigila: si el gobierno decide de qué se habla, también decide qué se vigila.

## 3. Dos teorías, dos expectativas para la oposición

Nos apoyamos en dos teorías que dan expectativas distintas. Lovett, Bevan y Baumgartner encuentran que los temas del informe anual de un presidente popular suben después en las audiencias de comités del Congreso, por unos tres meses; de ahí, que la oposición podría responder. Ellos miden comités, no el Pleno, y no comparan partidos dentro de una cámara: eso agregamos. Petrocik dice que cada partido tiene fama de manejar mejor ciertos temas y que sus candidatos los enfatizan en campañas presidenciales; llevado a la tribuna, que es extensión nuestra, la oposición preferiría los suyos. Ojo: Petrocik también dice que, cuando el tema del rival es inevitable, se habla de él desde el ángulo propio. Para el método, Olden y Møen muestran que si dos diferencias en diferencias comparten el mismo sesgo, al restarlas se cancela: por eso comparamos los dos bloques. Y nos inspiramos en el Comparative Agendas Project para los temas, en Simmons y coautores, que muestran que decidir después de ver los datos infla los falsos positivos, y en Goldsmith-Pinkham, para quien la IA acelera el trabajo pero el juicio sigue siendo lo que decide.

## 4. Dos fuentes de texto, unidas por fecha

Usamos dos fuentes de texto. De la mañanera, la sección “Quién es quién en las mentiras”: cada semana presentaba notas de prensa como falsas. Tomamos 317 notas de 76 secciones: las 64 de la muestra y 12 vecinas, que necesitamos para saber qué temas se tocaron la semana antes y la semana después. Cada nota es un ítem y recibe un tema. De la Cámara, las versiones estenográficas del Pleno: 2,316 discursos de diputados en las partes de la sesión donde cada grupo elige de qué hablar, como iniciativas, proposiciones y agenda política, en 154 sesiones. Para cada emisión tomamos las dos sesiones anteriores y las dos posteriores. La sesión de la tarde del mismo miércoles no cuenta, porque su orden del día se cerró antes de la mañanera.

## 5. Para comparar, las notas de la sección y los discursos necesitan la misma lista de temas

Para saber si un diputado habló del tema que tocó la sección, los dos textos tienen que estar en la misma lista de temas. Usamos los 21 temas del Comparative Agendas Project y una categoría para lo que no es política pública; cada texto recibe un solo tema. Por ejemplo, “es falso que falten medicamentos” va a Salud, y una iniciativa sobre abasto de medicinas también va a Salud: así sabemos qué parte del discurso de cada partido trata del tema tocado. Antes de clasificar la muestra probamos el libro de códigos en dos pilotos con textos de fuera y lo congelamos. Después Claude Opus 5.5 lo aplicó a las 317 notas y los 2,316 discursos. Al repetir una parte en otro lote, 92 de 100 salieron iguales. Pero ser consistente no es acertar; para eso está la validación a mano.

## 6. Revisamos 160 textos a mano: el modelo acierta igual con los dos bloques

Para saber si el modelo acierta, los tres, Tania, Paola y Diego, codificamos a mano 160 textos al azar: 100 discursos, mitad de la oposición y mitad de Morena, y 60 notas de la sección. Cada texto lo codificaron dos de los tres, en parejas que rotaban, así que cada quien hizo unos 107, sin ver partido, fecha ni lo que dijo el modelo. Primera pregunta: ¿coincidimos entre nosotros? En 141 de 160 pusimos el mismo tema. El alfa de Krippendorff descuenta el acuerdo que daría el azar; nos dio 0.87, arriba de la meta de 0.80 que fijamos antes. Si hubiera quedado abajo de 0.67, habríamos tenido que juntar temas. Segunda pregunta: de esos 141, el modelo clasificó 135; los otros 6 son discursos de sesiones que no entran al análisis. ¿El modelo pone el mismo tema que nosotros? En la oposición acierta 40 de 42, en Morena 39 de 39 y en las notas de la sección 51 de 54. Por eso sirvió: si el modelo se equivocara más con un bloque, la comparación entre bloques mediría su error y no la conducta de los diputados.

## 7. Cada semana, la sección le da un papel a cada tema

Primero, qué comparamos. Analizamos 7 temas, elegidos con una regla fijada antes de ver resultados: los que la sección tocó en 8 emisiones o más y que ocupan al menos 1% de lo que hablan los diputados. Cada semana, la sección le da un papel a cada tema. Si este miércoles tocó Salud y el anterior no, Salud es tratado: es una novedad que podría mover a los diputados. Si un tema no lo tocaron ni el miércoles anterior, ni este, ni el siguiente, es control: nos dice cuánto se mueven los temas por su cuenta. Los que ya venían de antes o vienen después quedan fuera, para no mezclar efectos. Tocar siempre se refiere a la sección; lo que dicen los diputados es lo que medimos.

## 8. La cuenta: cuánto cambió el tema tocado, menos cuánto cambiaron los controles

Segundo, la cuenta. Para la oposición, en una semana: Salud, el tema tocado, pasa de 4% de su discurso en las dos sesiones de antes a 6% en las dos de después, +2. Los controles, en promedio, no cambian. El efecto es +2 menos 0: dos puntos. La regresión hace esta cuenta en todas las semanas a la vez, por separado para la oposición y para Morena, y luego resta los dos bloques. ¿Por qué restar los controles? Porque las sesiones cambian mucho: en 74 de 154 nadie habló en secciones libres. Sin restar, una sesión con más debate parecería efecto de la mañanera. Tiene un costo: el tiempo de una sesión es limitado, así que si Salud sube, otro tema baja, y eso infla un poco el efecto, según una cuenta aproximada, entre 15 y 27%; nunca lo esconde. Y los ceros que nos pidieron revisar: si un partido no habló, la fila sale; si habló de otra cosa, el tema vale cero y se queda.

## 9. Después de la mañanera, ningún bloque habla más del tema tocado

El resultado, sesión por sesión. Cada punto dice cuánto cambió el porcentaje del discurso dedicado al tema que tocó la mañanera, comparado con la última sesión antes, que vale cero, y con los temas de control. En azul la oposición, en naranja Morena. Antes de la mañanera, los puntos no se separan del cero: no había una tendencia previa. Después, tampoco: los dos bloques se quedan cerca de cero, y todas las barras cruzan el cero. Promediando las dos sesiones de después, la oposición dedica 1.4 puntos menos al tema tocado y Morena 0.3 más; ninguno es distinto de cero, y la diferencia entre bloques tampoco. Lo que sí descartamos es una subida de más de 5 puntos. Congelamos el plan antes, lo corrimos una vez, y las variantes, el Poisson y la permutación dicen lo mismo.

## 10. Tema por tema casi todo es ruido; Salud es la excepción que vale revisar

Ahora, el mismo análisis tema por tema. Esto es exploratorio: lo decidimos después de ver los resultados, lo corrimos una vez y mostramos los siete temas. En casi todos, los puntos brincan y las barras son enormes: con 8 a 17 emisiones por tema no hay información para decir nada. La excepción es Salud: en las dos sesiones de después, la oposición y Morena dedican más de su discurso a salud. Pero hay tres razones para no creérnoslo todavía: son solo 9 emisiones, con tan pocas los errores estándar son poco confiables, y con tantos coeficientes alguno sale distinto de cero por azar. Lo tomamos como una pista para revisar en el trabajo final, no como un hallazgo.

## 11. Buena medición, poco poder: ni siquiera descartamos el +50% que buscábamos

¿Son buenos los resultados? La medición y el diseño funcionaron: la medida es confiable, la tubería da cero con fechas barajadas y las siete variantes coinciden. Pero la prueba tuvo poco poder. El intervalo de la oposición llega hasta 66% sobre su base, así que ni siquiera podemos descartar el efecto de 50% para el que diseñamos la prueba; un efecto de 25% ya en la simulación se detectaba una de cada cuatro veces, y los datos reales salieron más ruidosos. Lo que sí descartamos es un efecto grande. Y queda abierto por qué: es compatible con que la oposición prefiera sus temas y con que la sección no mueva a nadie.

## 12. Hacia el trabajo final del 7 de diciembre

Para el trabajo final: la heterogeneidad que prometimos, una dimensión a la vez y marcada como exploratoria; medir el ángulo y no solo el tema, porque un partido puede hablar del tema del rival para rebatirlo; y, como idea, más texto por ventana para tener poder contra efectos moderados. Cerramos con una pregunta abierta, que creemos es lo que el profesor quiso decir con “cada partido se cree sus propios temas”: ¿responde la oposición cuando la sección toca uno de sus temas? Gracias.

## 13. Ninguna variante cambia la conclusión

Respaldo para preguntas. Todas estas variantes, la permutación y el estudio de eventos estaban en el plan congelado. Efectos en puntos porcentuales salvo el Poisson. Ninguna es significativa; el p más bajo es 0.22, en la diferencia sin pesos. La sesión −2 no muestra evidencia de tendencias previas.
