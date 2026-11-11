# Plan para la versión final: qué falta, qué probar y qué validar

Nov 5, 2026 · @tania

*Versión congelada del 10 de noviembre de 2026: el plan de Tania con las 13 correcciones aprobadas por Diego el 7 de noviembre (`notas/10-correcciones-al-plan-final.md`), la decisión 14 y los cambios declarados en la sección “Cambios después de las correcciones”, al final. Se congela con la etiqueta git `plan-congelado` antes de estimar el efecto con datos reales.*

## Para qué es este plan

La meta es presentar el 12 de noviembre el proyecto como si fuera la versión final, con datos reales y una sola figura con el hallazgo. El feedback de ese día es el insumo para el trabajo del 7 de diciembre.

Para llegar ahí sin hacer p-hacking hay una regla que ordena todo lo demás: primero fijamos por escrito cada decisión del análisis y después vemos el resultado. Nunca al revés. Hoy todavía no hemos visto ningún resultado real, porque la clasificación de los textos no se ha corrido. Eso es una ventaja: todavía estamos a tiempo de congelar el plan.

Qué falta, en una línea: congelar el plan, clasificar los textos, validar la clasificación a mano, correr una sola vez la especificación principal, reportar todas las de robustez que fijamos de antemano y escribir. El calendario está en la sección 6.

Un punto de partida honesto, con la simulación del diseño actual (05, 7 temas, 100 corridas por escenario): si la oposición sube +50%, lo detectamos en 68% de las corridas, pero la diferencia contra Morena solo sale significativa en 42%. Con +25% bajan a 27% y 17%. Con efecto cero, los falsos positivos quedan en 4% a 6%, que es lo esperado. Esto quiere decir dos cosas: si el resultado sale cerca de cero, lo correcto es decir que no hay un efecto grande, no que no hay efecto. Y la diferencia entre bloques es la prueba más difícil de pasar, así que no podemos prometerla en la presentación.

## Qué dicen las lecturas y qué tomamos

### Simmons, Nelson y Simonsohn (2011): las decisiones flexibles inflan los falsos positivos

Qué dicen. Cada investigador toma muchas decisiones pequeñas que parecen razonables: qué variable de resultado usar, cuándo dejar de juntar datos, qué controles poner, qué observaciones quitar. Las llaman “grados de libertad del investigador”. Si esas decisiones se toman después de ver los datos, la probabilidad de encontrar algo “significativo” que no existe sube mucho por encima del 5%. En sus simulaciones, combinar cuatro de esas flexibilidades lleva los falsos positivos a 61%. Lo ilustran con un experimento real en el que escuchar una canción de los Beatles “hace” a la gente un año y medio más joven.

Su solución es transparencia, no prohibición. Piden a los autores fijar la regla para dejar de juntar datos antes de empezar, reportar todas las variables medidas y todas las condiciones, y si se quitan observaciones o se agrega un control, mostrar también el resultado sin quitarlas o sin el control. A quienes revisan les piden exigir que el resultado no dependa de decisiones arbitrarias.

Qué tomamos. Nuestro proyecto no es un experimento, pero tiene los mismos grados de libertad: cuántos temas, qué ventana, qué sesiones, qué secciones, qué turnos, qué modelo, qué errores estándar y, algo nuevo, qué instrucciones le damos al modelo de lenguaje que clasifica. La sección 3 lista cada uno y cómo lo fijamos. En la presentación, este paper sirve para explicar por qué congelamos el plan antes de ver resultados.

### Nikolov (2021): cómo escribir y presentar un trabajo empírico

Qué dice. Lo más importante es la claridad, escribir para alguien que no estudió economía. El hallazgo principal va al principio, justo después de la pregunta, como en una nota de periódico y no como en una novela de misterio. La contribución se dice con precisión: qué agrega el trabajo frente a lo que ya existe. La estrategia de identificación explica por qué una comparación simple estaría sesgada y qué supuestos se necesitan. En resultados, cada párrafo abre con su punto, interpreta el coeficiente en sus unidades y redondea según el error estándar. Cada tabla y figura debe entenderse sola, con título claro, ejes con nombre, leyenda y fuente, y legible en blanco y negro. Recomienda no hacer juicios normativos y dejar que el análisis hable.

Qué tomamos. La estructura del trabajo final y de la presentación: pregunta, hallazgo, contribución, en las primeras líneas. Un párrafo que explique por qué comparar simplemente antes y después estaría sesgado: la mañanera y los diputados reaccionan a las mismas noticias. Notas al pie completas en cada figura. Nuestra figura ya usa forma y color para distinguir los bloques, así que se lee en blanco y negro.

### Goldsmith-Pinkham (2026): investigar en tiempos de IA

Qué dice. La investigación es una cadena de etapas que se repiten: idea, diseño, datos, análisis, robustez, escritura, revisión y difusión. La IA acorta el tiempo de cada etapa pero no reemplaza el proceso. Le preocupa que la IA “sobrecargue” el p-hacking y cuenta su propia incomodidad cuando Claude Code se pone a contar cuántas regresiones salen significativas. Piensa que la replicación y los datos abiertos, que la IA también abarata, pueden compensarlo. Lo que se vuelve más valioso es el juicio: saber qué preguntas importan, qué hace creíble un diseño y conocer el contexto lo suficiente para saber dónde mienten los datos.

Qué tomamos. Coincide con lo que pidió el profesor: entender desde cero el porqué de cada decisión. Usamos IA para el código y la clasificación, pero las decisiones de diseño las tomamos y defendemos nosotros. Las reglas concretas están en la sección 7. Nuestro repositorio, con código, instrucciones y respuestas guardadas, es el paquete de replicación.

## Dónde podríamos hacer p-hacking sin querer

Cada fila es una decisión que, tomada después de ver resultados, podría fabricar un hallazgo. La regla: la columna “principal” se fija antes de ver datos reales y no se cambia. La columna “también reportamos” se presenta completa, salga como salga. Siguiendo a Simmons y coautores, si quitamos algo o agregamos algo, mostramos también el resultado sin ese cambio.

| Decisión | Principal (fijo) | También reportamos | Pendiente |
| --- | --- | --- | --- |
| Hipótesis principal | β de la oposición distinto de 0, a dos colas y con 5%, como dice la v3. La diferencia oposición − Morena es la segunda prueba | β de Morena | Escribir cuál es la principal |
| Emisiones | 64, sin la sesión de la tarde del mismo miércoles | 66, contando esa sesión | Cambiar el default de 02 a 64 |
| Ventana | 2 sesiones antes y 2 después, en el mismo periodo ordinario | Nada más. El estudio de eventos ya muestra cada sesión | Escribir la ecuación del estudio de eventos, con la sesión −1 como referencia (abajo de la tabla) |
| Número de temas | 7 más el resto. Si menos de 7 cumplen la regla, los que la cumplan (mínimo 5) | 5 y 10 más el resto | Confirmar 7 |
| Qué temas | Regla de la v3: de los temas que la sección tocó en al menos 8 emisiones, que distinguimos bien (si dos se confunden, se juntan) y de los que los diputados hablan, los 7 más frecuentes en la sección. Que los diputados hablen de él se mide con sus palabras en todo el periodo, sin ver ventanas ni emisiones | Ninguna otra lista | Escribir la regla |
| Tratados y controles | Tratado: tocado por esta emisión y no por la anterior. Control: no tocado por la anterior, esta ni la siguiente, más el resto. “La anterior” y “la siguiente” son las emisiones de la semana anterior y la siguiente, aunque caigan fuera de las 64 | Controles sin la condición de “ni la siguiente” | Ninguno |
| Texto de los diputados | Todas las palabras de las secciones libres | Solo turnos de 150 palabras o más (nueva, no está en la v3) | Alinear los scripts con la metodología |
| Variable de resultado | % de las palabras del partido en la sesión | Nada más | Ninguno |
| Modelo | Lineal ponderada por palabras del partido en la sesión | Poisson y lineal sin pesos | Ninguno |
| Errores estándar | Agrupados por emisión y por sesión | Permutación de las fechas de emisión | Escribir el script de permutación |
| Clasificador | Una versión congelada del libro de códigos y de las instrucciones, probada solo con textos fuera de la muestra | Una segunda corrida de una parte de los textos, para medir estabilidad | Congelar y guardar el hash del libro de códigos y de las instrucciones (hoy 07 solo guarda el del libro) |
| Validación | Alfa de Krippendorff de al menos 0.80 entre los dos codificadores | Acierto del modelo por bloque | Entre 0.67 y 0.80 se reporta como tentativo. Debajo de 0.67 juntamos una sola vez los temas que más confundimos y recalculamos |
| Exclusiones | Se quitan emisiones sin tema nuevo o sin discurso, con una regla fija | Cuántas y cuáles se quitan | Ninguno |
| Heterogeneidad | Ninguna en el análisis principal | Las cuatro de la v3, una a la vez y marcadas como exploratorias: por partido de oposición, por blanco del ítem (oposición o medio), antes y después de septiembre de 2023, y primera contra segunda sesión | Ninguno |

Ecuación del estudio de eventos (fila “Ventana”):

$$Y_{ptse} = \sum_{k \in \{-2,\,+1,\,+2\}} \left( \beta_O^{k}\, \text{Opos}_p \times \text{Toc}_{te} \times D^{k}_{se} + \beta_M^{k}\, \text{Morena}_p \times \text{Toc}_{te} \times D^{k}_{se} \right) + \alpha_{pte} + \gamma_{pse} + \varepsilon_{ptse}$$

$D^{k}_{se}$ vale 1 si la sesión $s$ es la número $k$ de la ventana de la emisión $e$. La sesión −1 es la referencia, así que cada $\beta^{k}$ se lee contra la sesión justo anterior a la emisión. Mismos pesos, efectos fijos y errores que la especificación principal. $\beta^{-2}$ es la prueba de tendencias previas: si se aleja de cero, se reporta. $\beta^{+1}$ y $\beta^{+2}$ muestran si el efecto dura una o dos sesiones. Es una prueba de apoyo: la hipótesis principal sigue siendo el $\beta$ de la especificación principal.

Todo lo que no está en esta tabla y se nos ocurra después de ver resultados va en una sección aparte llamada “Análisis exploratorio”, con esa etiqueta en el texto y en las láminas.

## Checklist por etapa

Las etapas van en orden, con una excepción: la 3 y la 4 pueden avanzar mientras corre la 2, porque ninguna muestra el efecto. La 5 no empieza hasta cerrar de la 1 a la 4.

### 1. Congelar el plan (antes de ver cualquier dato real)

- [ ] Escribir el plan de análisis en una o dos páginas: la tabla de la sección 3, la ecuación de la metodología v3 y la figura que vamos a mostrar.
- [ ] Subir el trabajo del clasificador que sigue sin commit (06, 07, libro de códigos, piloto_1), para que la etiqueta lo incluya.
- [ ] Subirlo al repositorio con un commit y una etiqueta de git (por ejemplo plan-congelado). La etiqueta subida a GitHub es la prueba de que se escribió antes de ver resultados (la fecha de un commit local se puede cambiar).
- [ ] Que cada integrante pueda explicar sin notas por qué tomamos cada decisión. El documento 09-por-que-cada-decision.md es la base.
- [ ] Preguntar al profesor qué quiso decir con “cada partido se cree sus propios temas”.

### 2. Medir: clasificar los textos

- [ ] Probar el clasificador solo con textos fuera de la muestra (la opción --piloto de 07). El libro de códigos solo se ajusta en esta etapa.
- [ ] Congelar el libro de códigos y las instrucciones, y guardar su versión.
- [ ] Clasificar la sección de las 64 emisiones y las intervenciones de los diputados.
- [ ] Clasificar dos veces una parte de los textos (la opción --repetir) para medir qué tan estable es.
- [ ] Guardar todas las instrucciones y respuestas del modelo en el repositorio.

### 3. Validar la medición

- [ ] Rehacer la muestra de 08. La actual es de antes de unir los turnos: solo 2 de sus 150 textos coinciden con la versión vigente. Tampoco tiene ítems de la sección, porque esos existen hasta que el modelo corta la sección. Codifican dos personas que no operan el clasificador.
- [ ] Codificar a mano la muestra de 08 (150 intervenciones y 80 ítems), cada quien por su lado y sin ver la respuesta del modelo.
- [ ] Calcular el alfa de Krippendorff y el acierto del modelo por bloque. Si el modelo acierta distinto con la oposición que con Morena, eso sesga la comparación y hay que decirlo.
- [ ] Revisar dónde pueden mentir los datos: transcripciones que le atribuyen al Presidente lo que dice la presentadora, sesiones mal fechadas y diputados que cambiaron de partido durante la legislatura.

### 4. Probar la tubería sin ver el efecto

- [ ] Escribir 11_estimar.py: arma Y_ptse a partir de las clasificaciones y estima la especificación principal, las de robustez y el estudio de eventos. Probarlo con los datos simulados de 05: tiene que recuperar el efecto que pusimos.
- [ ] Correr todo el análisis con fechas de emisión inventadas (placebo). Debe dar un efecto cercano a cero. Si no, hay un error en el código y se corrige aquí, antes de ver el resultado real.
- [ ] Sacar los descriptivos: temas tratados por emisión, palabras por bloque y sesión, y los dos tipos de ceros.

### 5. Estimar una sola vez

- [ ] Correr la especificación principal una vez y guardar la salida con fecha.
- [ ] Revisar la sesión de 2 antes en el estudio de eventos. Si se aleja de 0, hay una tendencia previa y se reporta.

### 6. Robustez

- [ ] Correr todas las variantes de la columna “también reportamos” y ponerlas en una sola tabla, salgan como salgan.
- [ ] Calcular el valor p por permutación de fechas como confirmación de los errores estándar.

### 7. La figura

- [ ] Adaptar 10\_figura\_efecto.py para que lea la salida de 11\_estimar.py (hoy solo dibuja datos sintéticos) y correrlo con los datos reales.
- [ ] Escribir el título según lo que salga. Conviene tener listas de antemano tres versiones: la oposición reacciona y Morena no, ninguno reacciona, los dos reaccionan igual.
- [ ] Escribir la nota al calce completa, que pide el profesor: qué se compara, unidades, intervalos, N y fuente.
- [ ] Redondear según el error estándar, como sugiere Nikolov.

### 8. Escritura del trabajo final

- [ ] Introducción: gancho, pregunta, hallazgo y contribución en las primeras dos páginas como máximo.
- [ ] Datos: fuentes, periodo, unidad de observación, N y descriptivos.
- [ ] Diseño: por qué comparar antes y después estaría sesgado y qué supuesto necesitamos.
- [ ] Resultados: cada párrafo abre con su punto y da el efecto en sus unidades.
- [ ] Conclusión: qué aprendimos, limitaciones e implicaciones de política sin juicios de valor.
- [ ] Abstract al final, de 150 palabras como máximo.
- [ ] Al menos 15 fuentes de calidad en formato APSR o AER, cada una citada por lo que dice.

### 9. Presentación del 12 de noviembre

- [ ] Seis o siete láminas de contenido, con poco texto.
- [ ] Ensayar con cronómetro: son 12 minutos y el corte es estricto.
- [ ] Subirla a Canvas antes de que empiece la clase.

## Feedback del profesor: estado de cada punto

Cinco de los diez puntos ya están resueltos en el diseño. Lo que falta depende de los datos reales o de una pregunta al profesor.

| Comentario | Cómo lo atendemos | Estado |
| --- | --- | --- |
| El supuesto no corresponde con la regresión | En la v3 el supuesto se escribe al mismo nivel que el efecto fijo: partido × tema × emisión. Hay que cuidar que el trabajo final lo diga igual | Hecho |
| Cada partido se cree sus propios temas | No estamos seguros de qué quiso decir. Si se refiere a que cada partido habla más de ciertos temas, el efecto fijo partido × tema × emisión ya lo absorbe | Preguntar |
| El efecto va a ser igual en la oposición y en el presidente | Estimamos un efecto para la oposición, otro para Morena y la diferencia | Hecho |
| Hacerlo más sencillo y con otro supuesto identificador | Doble diferencia por bloque con pocos temas, en lugar de la triple diferencia | Hecho |
| Checar los ceros en la variable de resultado | Reportar dos tipos de ceros: partidos que no hablaron en la sesión y temas de los que no hablaron | Falta |
| Si la Y está en porcentaje | El efecto se lee en puntos porcentuales y se convierte a % sobre la base | Hecho |
| Poisson como robustez o como principal | Lineal como principal, porque en la simulación el Poisson exageró el efecto. Poisson como robustez | Hecho |
| Elegir un número pequeño de temas | Falta fijar el número (proponemos 7) y la regla para escogerlos | Falta |
| Figura: incertidumbre, afirmación y evidencia, etiquetas | Resuelto en la versión simulada. Falta rehacerla con datos reales | Falta |
| Entender e iterar desde cero el porqué de cada decisión | El documento 09 y este plan. Cada integrante debe poder defender cada fila de la sección 3 | Falta |

## Calendario

El margen es corto: si un paso se atrasa un día, el resultado real llega justo para el ensayo.

&#91;embedded content: calendario al 7 de diciembre · 9 pasos, 3 compuertas\]

Plan B, decidido desde hoy: si el lunes 9 el alfa sale bajo o la clasificación no terminó, no apuramos el resultado. El 12 presentamos el diseño, la validación y la figura simulada marcada como tal, y el resultado real se queda para el trabajo final.

## Reglas para usar IA en el proyecto

La IA hace el trabajo pesado. Las decisiones las tomamos y defendemos nosotros. Estas reglas aplican también a Claude en estas sesiones.

1. Las decisiones de diseño salen del plan congelado, no de una conversación con la IA. Si la IA propone un cambio después de ver datos, va a “Análisis exploratorio”.
2. Nunca pedirle a la IA que pruebe especificaciones hasta encontrar una significativa, ni que cuente cuántas salen significativas. Es justo lo que preocupa a Goldsmith-Pinkham.
3. Llevar un registro de cada corrida con datos reales: fecha, especificación y resultado, incluidas las que no reportemos. Basta un archivo en el repositorio.
4. Para el clasificador, guardar el modelo y su versión, el libro de códigos, las instrucciones y todas las respuestas. Clasificar dos veces una parte para medir estabilidad, porque ya no se puede fijar la temperatura.
5. Una persona del equipo revisa cada script antes de correrlo con datos reales y lee al menos 20 clasificaciones del modelo con sus textos.
6. Cada cita del trabajo se verifica en el texto original. Nada de citar por lo que dice un resumen.
7. El trabajo final incluye un párrafo que diga para qué usamos IA: código, clasificación de temas y revisión de redacción.

## Cambios después de las correcciones (7 al 10 de noviembre, sin ver el efecto)

Ninguno de estos pasos muestra el efecto: nadie ha visto todavía datos por bloque antes y después de una emisión.

- **Temas** (7 de noviembre, `analisis/12_elegir_temas.py`): “los diputados hablan del tema” es al menos 1% de sus palabras en las sesiones de las ventanas, todas juntas. Quedan 20 Gobierno, 12 Justicia y seguridad, 10 Transporte, 8 Energía, 3 Salud, 1 Economía y 2 Derechos civiles. Con 5 temas, los primeros cinco; con 10, más 19, 15 y 7.
- **Libro de códigos**: las campañas de bots #NarcoPresidente van en 0 (aclaración del 7 de noviembre, aplicada a 8 ítems de la sección).
- **Muestra de validación** (8 de noviembre): se redujo de 230 a 160 unidades, 100 intervenciones (50 de oposición y 50 de Morena) y 60 ítems de la sección, como subconjunto estratificado de la muestra ya armada (`08_validacion.py reducir`). Se codificó en un Excel por persona (`14_hojas_excel.py`).
- **Quién codifica**: la corrección 11 decía que codifican dos personas que no operan el clasificador. Codificamos los tres (Tania A, Paola B, Diego C) y cada unidad la codifican dos. Diego opera el clasificador, aunque al codificar no veía las respuestas del modelo. Por eso reportamos el alfa por pareja además del total.
- **Resultado de la validación** (10 de noviembre): alfa de 0.87 en las 160 unidades (0.86 en intervenciones y 0.89 en ítems). Por pareja: Tania–Paola 0.78 (54), Tania–Diego 0.87 (52) y Paola–Diego 0.94 (54). Supera la meta de 0.80, así que no se junta ningún tema y los 7 temas quedan fijos. El modelo coincide en 96% de las 135 unidades donde los codificadores coinciden (Morena 100%, oposición 95%, sección 94%). El alfa del blanco del ítem es bajo (0.53), así que la heterogeneidad por blanco se reporta con esa advertencia.

## Fuentes

- Simmons, Joseph P., Leif D. Nelson y Uri Simonsohn. 2011. “False-Positive Psychology: Undisclosed Flexibility in Data Collection and Analysis Allows Presenting Anything as Significant.” Psychological Science 22 (11): 1359–1366. [doi](https://doi.org/10.1177/0956797611417632)
- Nikolov, Plamen. 2021. “Writing Tips for Economics Research Papers.” MPRA Paper No. 105088. [MPRA](https://mpra.ub.uni-muenchen.de/105088/)
- Goldsmith-Pinkham, Paul. 2026. “Research in the Time of AI.” A Causal Affair (Substack), 16 de marzo. [post](https://paulgp.substack.com/p/research-in-the-time-of-ai)
- Simpser, Alberto. 2026. “Descripción de entregas relacionadas con el proyecto a desarrollar.” Tópicos de Políticas Públicas II, ITAM.
- Simulaciones del equipo: analisis/resultados\_simulacion\_rediseno\_7temas.csv en el repositorio [mananera-agenda](https://github.com/DI3GOM/mananera-agenda).
