# Guía de citas: qué decimos de cada texto y dónde lo dice

1 de noviembre de 2026. Sirve para revisar que cada cita de `metodologia_v3.Rmd` diga lo que dice la fuente. Para cada afirmación damos la página y la parte del texto donde está, y lo que dice la fuente en nuestras palabras. Para comprobarlo, abran el texto en esa página y lean el pasaje. No copiamos los pasajes completos porque los artículos tienen derechos de autor; si quieren tener la frase textual a la mano, cópienla del PDF en la columna "Dónde".

La v3 cita tres textos: Petrocik (1996), Lovett, Bevan y Baumgartner (2015) y Olden y Møen (2022).

**Regla:** solo atribuimos a un texto lo que leímos en él. "Correcto" quiere decir que lo leímos en el texto completo. "Correcto en el resumen" quiere decir que lo leímos en el resumen publicado del artículo, pero todavía no en el cuerpo. Antes de entregar, todo debe quedar en "Correcto".

## Cómo conseguir cada texto

| Texto | Acceso | Qué leímos para esta guía |
|---|---|---|
| Lovett, Bevan y Baumgartner (2015), *Policy Studies Journal* 43 (1): 22–43 | De pago en Wiley. Hay versión de los autores en el repositorio de la Universidad de Edimburgo, que pide verificación de "no soy un robot" | El texto completo de la versión publicada (con la paginación de la revista) |
| Olden y Møen (2022), *Econometrics Journal* 25 (3): 531–553 | Acceso abierto en Oxford Academic (https://doi.org/10.1093/ectj/utac010); el sitio bloquea a los programas, pero se abre en un navegador normal | El resumen oficial, por OpenAlex |
| Petrocik (1996), *American Journal of Political Science* 40 (3): 825–850 | De pago (JSTOR). Con la cuenta de la universidad | El resumen oficial, por OpenAlex. **Falta leer el texto completo** |

## Lovett, Bevan y Baumgartner (2015)

**Qué estudian.** Si los temas que el presidente de Estados Unidos menciona en su informe anual (State of the Union) aumentan después las audiencias de los comités del Congreso sobre esos temas, de 1953 a 2005, por separado para la Cámara de Representantes y el Senado.

| Lo que decimos en la v3 | Dónde lo dice | Qué dice, en nuestras palabras | Estado |
|---|---|---|---|
| Los temas del informe anual aumentan después las audiencias de los comités (Qué esperamos) | p. 22, resumen; p. 23, primer párrafo | Los presidentes populares logran que el Congreso dedique atención a los temas que más destacaron en su informe | Correcto |
| Solo si el presidente es popular (Qué esperamos) | p. 22, última frase del resumen; pp. 34–35, primer hallazgo del análisis | Los presidentes impopulares no influyen. En la Cámara de Representantes, el efecto aparece con aprobación de al menos 60% | Correcto |
| Sobre todo en los primeros meses (Qué esperamos) | p. 23, segundo párrafo; p. 36, H3 | Su mejor estimación es que el efecto del informe dura unos tres meses; el modelo de tres meses es siempre el que mejor funciona | Correcto |
| En la Cámara de Representantes dura más si la controla su partido (Qué esperamos) | p. 23, primer párrafo; p. 36, discusión de H1; p. 39, conclusión | En la Cámara, el efecto es más fuerte y más duradero cuando la controla el partido del presidente. A corto plazo, el efecto existe con gobierno unificado o dividido; solo con gobierno unificado sigue el resto del año. En la conclusión lo llaman "some support" para la hipótesis de gobierno dividido. En el Senado los resultados son mixtos | Correcto. Solo vale para la Cámara de Representantes; no lo extiendan al Congreso en general |
| Un presidente popular, en los meses siguientes a su informe, mueve incluso a una cámara del partido rival (Qué aprenderemos) | p. 22, introducción; p. 39, conclusión | El efecto de la popularidad puede ser tan fuerte que mueve a los legisladores del partido rival. La conclusión cierra diciendo que importa un presidente popular en el Congreso, "even one controlled by the rival party" | Correcto, con el matiz de tiempo: con gobierno dividido el efecto se acaba al empezar el verano (p. 35) |
| No comparan partidos dentro de una misma cámara (Qué esperamos y Qué aprenderemos) | Diseño del estudio, pp. 29–30 | Su variable es el cambio en el número de audiencias por tema en cada cámara. No separan a los legisladores por partido | Correcto. Es una afirmación sobre lo que el estudio **no** hace |

**Cómo lo usamos.** Para dos expectativas: que la oposición podría responder a un presidente popular, y que Morena podría responder más. La segunda es lectura nuestra, porque ellos comparan cámaras controladas por un partido u otro, no partidos dentro de una cámara.

**Ojo con lo que no dice:**
- Mide **audiencias de comités**, que deciden los presidentes de comisión. Nosotros medimos **discursos en el Pleno** de cada partido. Si el profesor pregunta, la respuesta es que tomamos la idea, no la medida.
- El estímulo es un discurso al año. La mañanera es semanal y desmiente notas; es un estímulo distinto.
- No digan que encuentran que el partido del presidente "responde más". Encuentran que una cámara controlada por su partido le hace caso más tiempo.

## Olden y Møen (2022)

**Qué estudian.** Cómo se identifica el estimador de triple diferencia, que muchos artículos usan sin derivar sus supuestos.

| Lo que decimos en la v3 | Dónde lo dice | Qué dice, en nuestras palabras | Estado |
|---|---|---|---|
| Si dos diferencias en diferencias tienen el mismo sesgo, al restarlas se cancela (Estrategia de identificación) | p. 531, resumen | La triple diferencia se puede calcular como la resta de dos diferencias en diferencias. No necesita dos supuestos de tendencias paralelas: la resta de dos estimadores sesgados es insesgada si el sesgo es igual en ambos, y para eso basta un supuesto de tendencias paralelas | Correcto en el resumen. Falta leer el texto completo |

**Cómo lo usamos.** Para defender la resta β_O − β_M: aunque una noticia sesgue el efecto de cada bloque, la resta no queda sesgada si la noticia mueve igual a los dos.

**Pendiente:** solo leímos el resumen. Hay que leer el texto completo (la sección donde derivan el supuesto de identificación) y pasar la fila a "Correcto".

**Ojo:** el resultado es sobre la resta. El efecto de cada bloque por separado sí queda expuesto a ese sesgo, y la v3 lo dice bien ("Eso afectaría el efecto de cada bloque, pero no su resta").

## Petrocik (1996)

**Qué estudia.** Una teoría del voto basada en la "propiedad" de los temas, aplicada a las elecciones presidenciales de Estados Unidos de 1960 a 1992, con un caso de estudio de 1980.

| Lo que decimos en la v3 | Dónde lo dice | Qué dice, en nuestras palabras | Estado |
|---|---|---|---|
| Cada partido tiene fama de manejar mejor ciertos temas (Qué esperamos) | p. 825, resumen ("Hypotheses") | Los votantes apoyan al candidato cuyo partido tiene, por su desempeño, fama de manejar mejor el problema que les preocupa | Correcto en el resumen. Falta leer el texto completo |
| Sus candidatos enfatizan esos temas en campaña (Qué esperamos) | p. 825, resumen ("Theory" y "Results") | Espera que los candidatos enfaticen los temas en los que llevan ventaja y su rival es peor visto, y encuentra que cada candidato tiene un patrón propio de temas en campaña | Correcto en el resumen. Falta leer el texto completo |
| Estudia campañas presidenciales en Estados Unidos (Qué esperamos) | Título y p. 825, resumen ("Method") | Analiza noticias de campaña, los problemas que mencionan los votantes y el voto en elecciones presidenciales de 1960 a 1992 | Correcto en el resumen. Falta leer el texto completo |
| Si β_O es cercano a cero, la oposición se queda en sus temas, como en la extensión de Petrocik (Qué aprenderemos) | Es una extensión nuestra | La v3 lo presenta como extensión, que es honesto | Correcto como extensión, siempre que la idea de Petrocik que extendemos se confirme en el texto completo |

**Cómo lo usamos.** Para la expectativa de que la oposición prefiere sus propios temas a los de la mañanera.

**Ojo:**
- Es una teoría de **campañas y voto**, no de legisladores. La v3 ya lo aclara ("Es una extensión nuestra").
- La teoría dice que los candidatos enfatizan **sus** temas y evitan los del rival. Eso implica algo más fino que "la oposición no responde": que responda cuando la mañanera toca un tema propio de la oposición (por ejemplo, seguridad para el PAN) y no cuando toca uno de Morena (por ejemplo, programas sociales). Puede ser lo que quiso decir el profesor con "cada partido se cree sus propios temas".
- **Pendiente:** solo leímos el resumen. Hay que leer el texto completo para confirmar cómo define la propiedad de los temas y pasar las filas a "Correcto". Si alguna no se confirma, se quita de la v3.

## Fuentes de datos y normas (no son citas de argumento)

| Fuente | Para qué la usamos | Dónde verificar |
|---|---|---|
| Reglamento de la Cámara de Diputados, arts. 60 y 65 | La sesión del mismo miércoles no cuenta como posterior: los grupos registran sus asuntos a más tardar a las 13:00 del día anterior (art. 65.1) y la Gaceta publica el orden del día a más tardar a las 22:00 del día anterior (art. 60.1) | `papers/Camara-de-Diputados-Reglamento-ultima-reforma-DOF-2025-05-07.pdf` |
| NOSTRODATA | Transcripciones de las mañaneras | Repositorio en GitHub; los datos están en `datos/mananeras.parquet` |
| Comparative Agendas Project | Los temas | Master Codebook en comparativeagendas.net; nuestra versión está en `analisis/libro_de_codigos.md` |
