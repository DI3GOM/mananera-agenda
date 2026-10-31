# Por qué tomamos cada decisión de la metodología

Equipo 1 · Guía interna, en palabras simples. Explica cada decisión de la metodología, por qué citamos cada texto y qué cambió en el camino. Complementa a `07-como-funciona-la-metodologia.md`, que explica cómo funciona el diseño paso a paso.

## En cinco líneas

1. Preguntamos si, cuando "Quién es quién en las mentiras" toca un tema, la oposición habla más de ese tema en la Cámara que Morena.
2. Cada emisión es un mini-experimento: comparamos antes y después, temas tocados y no tocados, y oposición contra Morena.
3. Un modelo de lenguaje asigna el tema de cada texto, y nosotros revisamos a mano que lo haga bien.
4. Primero elegimos un modelo de Poisson. La simulación muestra que, con nuestros datos, exagera el efecto. Una regresión lineal pesada casi no tiene ese problema. La decisión final depende de la última simulación.
5. Para decidir si el efecto es real usamos una prueba de permutación: repetimos el análisis con temas falsos y vemos si el resultado real destaca.

---

## 1. La pregunta y por qué comparamos contra Morena

**Decisión.** Medimos cuánto *más* responde la oposición que Morena, no cuánto responde la oposición sola.

**Por qué.** López Obrador era de Morena, así que lo esperable es que su bancada repita lo que dice la mañanera. Eso no nos dice nada nuevo. Lo interesante es si la oposición, que no tiene ningún interés en amplificar al Presidente, también termina hablando de sus temas.

Hay una segunda razón práctica. Si un día hay una noticia grande sobre salud, todos los partidos hablan de salud. Al comparar contra Morena, esa noticia afecta a los dos bloques y se cancela.

**Lo que esto implica.** Nuestro número (β) mide una *diferencia* entre bloques. Si los dos reaccionan igual, β sale cero aunque los dos hayan reaccionado. Por eso también vemos cada bloque por separado, aunque esa parte es solo descriptiva.

## 2. Qué esperamos encontrar, y por qué citamos esos tres textos

Citamos tres textos porque apuntan a respuestas opuestas. Así queda claro que el resultado no es obvio, que era una de las preguntas del profesor.

| Texto | Qué dice, en simple | Por qué lo usamos |
|---|---|---|
| **Petrocik (1996)** | Cada partido tiene fama de manejar mejor ciertos temas y, en campaña, habla de esos y evita los del rival. Lo estudia en elecciones presidenciales de EE.UU. | Sugiere que la oposición **no** seguiría la agenda de la mañanera: se quedaría en sus propios temas. Ojo: él estudia campañas, no congresos; aplicarlo a la tribuna es una extensión nuestra. |
| **Green-Pedersen y Mortensen (2010)** | En el parlamento danés, el gobierno está obligado a responder a los temas del momento, pero la oposición tiene libertad para empujar los temas que le convienen. | Lleva la idea de Petrocik al parlamento. También apunta a que la oposición **no** seguiría la agenda del Ejecutivo. |
| **Lovett, Bevan y Baumgartner (2015)** | En EE.UU., los temas que el presidente menciona en su informe anual aumentan después la atención del Congreso, pero solo si el presidente es popular y solo por poco tiempo. | Apunta a lo contrario: un presidente popular **sí** puede mover la atención del Congreso. También justifica mirar solo las dos sesiones siguientes: si el efecto existe, dura poco. |

Ninguno compara a la oposición contra el partido del presidente. Esa comparación es lo que aporta nuestro proyecto.

## 3. Qué periodo y qué sesiones usamos

| Decisión | Por qué |
|---|---|
| **Solo 2021–2024 (LXV Legislatura).** | La sección se transmitió de 2021 a 2024. Con Sheinbaum existe un segmento parecido, pero casi siempre es un video sin transcripción, así que no podemos saber de qué temas habla. |
| **Solo sesiones ordinarias del Pleno.** | En las sesiones solemnes, las del Congreso General y la Comisión Permanente no participan todos los diputados o no hay debate libre. |
| **Dos sesiones antes y dos después de cada emisión, dentro del mismo periodo ordinario.** | Lovett et al. muestran que el efecto, si existe, dura poco. Además, si la ventana cruza unas vacaciones legislativas, el "después" ocurriría meses más tarde. |
| **La sesión de la tarde del mismo miércoles no cuenta como "después".** | Su orden del día ya estaba cerrado antes de la mañanera: los grupos registran sus asuntos a más tardar a las 13:00 del día anterior (Reglamento, art. 65) y la Gaceta lo publica antes de las 22:00 de ese día (art. 60). Con esta regla entran 64 emisiones; contándola, serían 66. **Pendiente:** el script `02_ventanas_y_volumen.py` todavía usa 66. |

## 4. Qué palabras contamos

**Decisión.** Solo contamos las partes de la sesión donde el grupo decide de qué hablar: iniciativas, proposiciones con punto de acuerdo, agenda política e intervenciones sobre diversos temas. No contamos dictámenes, acuerdos, comparecencias ni efemérides.

**Por qué.** En un dictamen, el tema lo fija la comisión que lo aprobó; en una efeméride, el calendario. Si la oposición habla de salud en un dictamen de salud, no es porque la mañanera la haya movido. El Reglamento (art. 62) enumera esas partes de la sesión, así que la separación no es arbitraria.

**Por qué contamos palabras y no discursos.** Una mención de pasada y un discurso entero sobre el tema no pesan lo mismo; las palabras sí reflejan esa diferencia.

## 5. Cómo sabemos de qué tema habla cada texto

| Decisión | Por qué | Texto |
|---|---|---|
| **Usamos los 21 temas del Comparative Agendas Project (CAP).** | Es una lista estándar e internacional de temas de política pública (salud, seguridad, economía…), así que no la inventamos nosotros. Además, nos deja comparar con la misma lista lo que dice la mañanera y lo que dicen los diputados. | **Bevan (2019)** cuenta cómo se armó esa lista común a partir de las de muchos países. |
| **Un modelo de lenguaje asigna el tema, a temperatura cero.** | Son miles de párrafos; codificarlos a mano es imposible. La temperatura cero hace que el modelo dé siempre la misma respuesta al mismo texto. | **Gilardi, Alizadeh y Kubli (2023)**: ChatGPT clasificó tuits mejor que trabajadores en línea en la mayoría de las tareas, y fue más consistente que humanos entrenados. **Ojo:** en la tarea de temas, la más parecida a la nuestra, acertó alrededor de 60% y quedó *por debajo* de los trabajadores en línea. Por eso no lo damos por bueno sin revisarlo. |
| **Dos de nosotros codificamos a mano una muestra al azar, sin ver la fecha.** | Para medir qué tan bien clasifica el modelo. "Sin ver la fecha" evita que sepamos si el texto es de antes o después de una emisión, porque eso podría sesgarnos. | |
| **Medimos nuestro acuerdo con el alfa de Krippendorff; meta de 0.80.** | Si ni siquiera dos personas coinciden en el tema, no podemos pedirle al modelo que acierte. El alfa descuenta las veces que coincidiríamos por pura suerte. | **Krippendorff (2004)** pide 0.80 para conclusiones firmes y acepta 0.667 para conclusiones tentativas. Si no llegamos a 0.80, juntamos los temas que más se confunden. |
| **Revisamos los aciertos del modelo por separado para oposición y Morena.** | Si el modelo se equivoca igual con los dos bloques, el error se cancela al compararlos. Si se equivoca más con uno, podría inventar o esconder un efecto. | |

## 6. Cómo separamos el efecto de la mañanera de todo lo demás

**La idea: tres restas.** Si un miércoles la sección desmiente una nota sobre desabasto de medicamentos:

1. Vemos cuánto cambia lo que la oposición habla de salud, de las dos sesiones anteriores a las dos posteriores.
2. Le restamos lo que cambió en los temas que la sección no tocó. Así quitamos lo que cambió en toda la sesión; por ejemplo, que ese día la oposición habló más de todo.
3. Hacemos lo mismo para Morena y restamos. Así quitamos las noticias que hicieron hablar de salud a todos.

Lo que queda es cuánto más se movió la oposición hacia el tema tocado que Morena. Esto se llama **triple diferencia**.

| Decisión | Por qué | Texto |
|---|---|---|
| **Un tema es "tratado" si la emisión lo tocó y la anterior no.** | Si la emisión anterior ya lo había tocado, el "antes" ya estaría contaminado. | |
| **Un tema es "de control" si no lo tocaron la emisión anterior, esta, ni la siguiente.** | Para que el grupo de comparación no reciba ningún empujón de la mañanera. **Riesgo:** la siguiente emisión podría escoger temas que la oposición estaba discutiendo esa semana, y quitarlos haría ver un efecto más grande. Por eso repetimos el análisis sin la condición "ni la siguiente". | |
| **Cada emisión se compara solo con sus propias sesiones, y luego juntamos todas las ventanas ("apilado").** | Como hay una emisión cada semana, mezclar todas en una sola comparación puede producir resultados engañosos. Al alinear cada emisión con su propio antes y después, es como si todas ocurrieran al mismo tiempo. | **Cengiz et al. (2019)** lo hacen con 138 aumentos del salario mínimo en distintos estados y años. Solo usamos su método; su tema no tiene relación con el nuestro. |
| **Solo necesitamos un supuesto.** | Sin la emisión, la *diferencia* entre oposición y Morena habría cambiado igual en los temas tocados que en los de control. No necesitamos que Morena sea un grupo "limpio", solo que cualquier sesgo afecte igual a los dos bloques. | **Olden y Møen (2022)** demuestran formalmente que la triple diferencia necesita un solo supuesto, no dos. |
| **El supuesto es sobre porcentajes, no sobre cantidades.** | En el modelo de Poisson, "cambiar igual" quiere decir crecer en el mismo porcentaje. | **Wooldridge (2023)** explica cómo se adapta el supuesto a modelos como el de Poisson. |
| **Revisamos si el tema ya venía subiendo antes de la emisión (sesión −2 contra −1).** | La amenaza principal es que la mañanera desmienta notas que ya circulaban y que la oposición habría retomado de todos modos. Si fuera así, veríamos la subida *antes* de la emisión. | **Roth (2022)** advierte que esta prueba muchas veces no detecta el problema, y que confiar solo en ella puede empeorar las cosas. Por eso decimos que ayuda, pero no demuestra el supuesto. |

## 7. Qué modelo usamos, y cómo llegamos ahí

Esta es la parte que más ha cambiado. En orden:

### Paso 1: la primera idea fue una regresión lineal sobre porcentajes

El primer borrador medía qué **porcentaje** de las palabras de cada partido iba a cada tema, con una regresión lineal normal. Vimos tres problemas:

- **Los porcentajes de un partido suman 100.** Si sube un tema, otro tiene que bajar, aunque nadie haya decidido nada sobre ese otro tema.
- **Si un partido no habló en una sesión, el porcentaje no existe** (sería 0 entre 0).
- **Hay muchísimos ceros.** En casi todas las sesiones, un partido no dice nada de la mayoría de los temas.

### Paso 2: cambiamos a contar palabras con un modelo de Poisson

**Por qué Poisson.** Es el modelo hecho para conteos con muchos ceros. Contar palabras en vez de porcentajes quita el problema de que todo sume 100. Además, su resultado se lee directamente como un cambio en porcentaje.

**Texto: Santos Silva y Tenreyro (2006).** Estudian el comercio entre países, donde también hay muchos ceros (países que no comercian entre sí). Muestran que la salida "fácil", sacar logaritmos y usar una regresión normal, no funciona con ceros (el logaritmo de cero no existe) y da resultados sesgados. Proponen usar Poisson, que maneja los ceros sin problema.

### Paso 3: la simulación mostró que el Poisson exageraba el efecto

Antes de ver cualquier dato real, hicimos una **simulación**: tomamos los discursos reales, les asignamos temas al azar, metimos un efecto de tamaño conocido (por ejemplo, +50%) y vimos si el modelo lo recuperaba.

El primer Poisson tenía un "nivel normal" (α) para cada partido-tema-*emisión*. El problema es que cada ventana tiene solo cuatro sesiones, casi todas en cero, y con tan poca información el modelo **estimaba el doble del efecto real**.

**Texto: Weidner y Zylkin (2021).** Explican este problema: con muchos niveles normales que estimar y pocos datos para cada uno, el Poisson da intervalos de confianza que no están centrados en el valor verdadero y errores estándar sesgados.

**Ajuste.** Calculamos α por *periodo ordinario* en vez de por emisión, porque así cada nivel normal se calcula con todo el semestre: unas 40 sesiones en lugar de 4. El sesgo bajó del doble a cerca de **+45%**, pero no desapareció.

### Paso 4: volvimos a probar la regresión lineal, ahora bien hecha

Con la simulación pudimos comparar los dos modelos con las mismas reglas. La versión lineal nueva usa los mismos niveles normales por periodo y pesa cada observación por cuántas palabras dijo el partido. Resultados con un efecto real de +50%:

| Modelo | ¿Encuentra efectos que no existen? (ideal: 5%) | ¿Detecta un efecto de +50%? | ¿Cuánto se equivoca en el tamaño? |
|---|---|---|---|
| Poisson, α por periodo (200 simulaciones) | 8% | 78% | Exagera ~44% |
| Lineal con pesos (500 simulaciones) | 7% | 78% | Se queda ~5% abajo |

**Por qué ahora sí funciona la lineal.** En una regresión lineal, los niveles normales se quitan exactamente, restando promedios, así que no importa que haya pocos datos por grupo. En el Poisson eso no se puede, y de ahí viene el sesgo. Los problemas del paso 1 resultaron ser menores en la práctica: el de "todo suma 100" ya está dentro de lo que la triple diferencia compara, y la simulación lo toma en cuenta al calcular el efecto verdadero.

**Decisión (30 de octubre).** Con 200 simulaciones, el Poisson rechaza de más casi igual que la lineal (8% contra 7%) y detecta lo mismo (78% con un efecto de +50%), pero exagera el tamaño del efecto en ~44%. Por eso la regresión lineal con pesos es el modelo principal y el Poisson queda como prueba de robustez. La metodología v2.0 (`metodologia/metodologia_v2.Rmd`) ya está escrita así.

## 8. Cómo decidimos si el efecto es real y no suerte

| Decisión | Por qué | Texto |
|---|---|---|
| **Errores agrupados por emisión y por sesión a la vez.** | Las observaciones de una misma emisión se parecen entre sí, y una misma sesión aparece en dos o tres ventanas. Si las tratáramos como independientes, creeríamos tener más información de la que hay y encontraríamos efectos falsos. | **Cameron, Gelbach y Miller (2011)** explican cómo corregir los errores cuando los datos se agrupan en dos dimensiones a la vez. |
| **La prueba principal es de permutación.** | Con esa corrección, la simulación encontró "efectos" inexistentes en 7% (lineal) y 8% (Poisson) de los casos, un poco más que el 5% ideal. La permutación sirve para confirmarlo sin depender de fórmulas, y no depende de fórmulas: 1,000 veces reasignamos los temas de cada emisión a otra emisión, volvemos a estimar y vemos si el resultado real es más extremo que casi todos los falsos. | **MacKinnon y Webb (2020)** recomiendan hacer la permutación con el estadístico t y no con el coeficiente, porque funciona mejor cuando los grupos son muy distintos entre sí. |
| **Decimos de antemano qué tamaño de efecto podemos detectar.** | Con la lineal pesada detectamos un efecto de +50% en 78% de los casos, pero uno de +25% solo en 30%. Si β sale cercano a cero, no podremos decir "no hay efecto", solo "no hay un efecto grande". | |

## 9. Cómo leeremos el resultado

| Resultado | Qué significa |
|---|---|
| β > 0 | La oposición responde a la mañanera más que Morena. |
| β < 0 | Morena retoma la agenda presidencial más que la oposición. |
| β ≈ 0 | Los dos bloques responden igual, o ninguno responde. Para distinguirlo, vemos cada bloque por separado (solo como evidencia descriptiva). |

## 10. Análisis por subgrupos

Repetimos el análisis por partido de oposición, por blanco del ítem (un medio o un político de oposición), antes y después del inicio del proceso electoral (septiembre de 2023) y por sesión (la primera o la segunda después de la emisión). Con 64 emisiones hay pocos datos por grupo, así que los presentamos como exploratorios, no como conclusiones.

## 11. Las referencias de un vistazo

| Texto | Para qué lo usamos | ¿Está en `papers/`? |
|---|---|---|
| Petrocik (1996) | Expectativa: la oposición no sigue al Ejecutivo | No (de pago) |
| Green-Pedersen y Mortensen (2010) | Expectativa: la oposición no sigue al Ejecutivo (en un parlamento) | No (de pago) |
| Lovett, Bevan y Baumgartner (2015) | Expectativa: un presidente popular sí mueve al Congreso; mirar solo dos sesiones | No (bajar a mano) |
| Olden y Møen (2022) | La triple diferencia necesita un solo supuesto | No (bajar a mano) |
| Wooldridge (2023) | El supuesto es sobre porcentajes en el Poisson | No (bajar a mano) |
| Cengiz et al. (2019) | Comparar cada emisión con sus propias sesiones (apilado) | Sí (versión de NBER) |
| Roth (2022) | La prueba de tendencias previas ayuda, pero no demuestra | Sí |
| Santos Silva y Tenreyro (2006) | Por qué Poisson con muchos ceros | Sí (versión de CEP) |
| Weidner y Zylkin (2021) | Por qué el Poisson se sesga con pocos datos por grupo | Sí (versión de arXiv) |
| Cameron, Gelbach y Miller (2011) | Errores agrupados en dos dimensiones | Sí (versión de NBER) |
| MacKinnon y Webb (2020) | Permutación con el estadístico t | Sí |
| Bevan (2019) | La lista de 21 temas del CAP | Sí (working paper) |
| Gilardi, Alizadeh y Kubli (2023) | Qué tan bien clasifica un modelo de lenguaje | Sí (versión de arXiv) |
| Krippendorff (2004) | La meta de acuerdo entre codificadores | Sí |
| Reglamento de la Cámara | Por qué la sesión del mismo día no cuenta; qué partes de la sesión son libres | Sí |
| NOSTRODATA (2024) | De donde salen las transcripciones de la mañanera | Datos en `datos/` |

Si el modelo principal cambia a la regresión lineal, Santos Silva y Tenreyro y Wooldridge pasan a justificar la prueba de robustez, no el modelo principal.

## 12. Lo que falta decidir

- [x] Modelo principal: lineal con pesos (decidido el 30 de octubre con 200 simulaciones del Poisson).
- [ ] Cambiar `mismo_dia_es_post` en `02_ventanas_y_volumen.py` para que dé 64 emisiones, como dice el texto.
- [ ] Confirmar la definición de tema de control (con o sin "ni la siguiente").
- [ ] Elegir el modelo de lenguaje: comparar uno comercial por API y uno abierto contra la muestra codificada a mano.
- [ ] Conseguir los cinco textos que faltan en `papers/` para revisar que los citamos bien.
