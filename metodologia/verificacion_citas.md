# Verificación de las citas de la metodología v3

31 de octubre de 2026. La v3 usa ahora el estilo de la v2: cinco textos, y cada cita dice qué idea tomamos. Abajo está lo que afirma la metodología sobre cada texto, lo que dice la fuente y cómo lo revisamos.

## Las cinco citas

| Texto | Lo que decimos | Lo que dice la fuente | Estado | Cómo lo revisamos |
|---|---|---|---|---|
| **Gilardi, Alizadeh y Kubli (2023)** | ChatGPT, sin ejemplos previos, clasificó tuits y noticias mejor que trabajadores en línea en la mayoría de sus tareas | "ChatGPT outperforms MTurk for most tasks" (p. 3) | Confirmado | PDF en `papers/` (versión de arXiv; su resumen es igual al de PNAS) |
| | Al asignar tuits a seis temas sobre moderación de contenido acertó alrededor de 60%, menos que esos trabajadores | Figura 1, panel A, "Topics": ChatGPT cerca de 62–64% y MTurk cerca de 73%. Los seis temas son de moderación de contenido (Sección 230, expulsión de Trump, etc.), no temas de política pública | Confirmado, con un matiz | Figura 1 del PDF. **Ojo:** el resumen del artículo menciona "topics" entre las tareas en que ChatGPT supera a los trabajadores, pero su propia figura muestra lo contrario en ese conjunto de datos. Nos quedamos con la figura |
| **Törnberg (2025)** | GPT-4 identificó el partido de políticos de 11 países a partir de un solo tuit, con más acierto que codificadores expertos y que clasificadores entrenados | El resumen publicado dice que identifica la afiliación política "based on a single X/Twitter message", con datos "from 11 different countries", y que GPT-4 supera a modelos supervisados y a codificadores humanos | Confirmado | Resumen publicado (OpenAlex y Semantic Scholar). Volumen 43 (6): 1181–1195; salió en línea en 2024 y en número impreso en 2025 |
| | (v2) "advierte que hay que validarlo en cada tarea" | Solo está en la versión preliminar de arXiv (2023), que habla de validar "on specific tasks"; no lo encontramos en el resumen publicado | No verificado en la versión que citamos | Por eso la v3 ya no se lo atribuye: lo dice como conclusión nuestra |
| **Lovett, Bevan y Baumgartner (2015)** | Los temas que el presidente de EE. UU. destaca en su informe anual aumentan después las audiencias de los comités del Congreso | Modelan las menciones del informe sobre el número de audiencias del Congreso por tema, de 1953 a 2005 | Confirmado | Texto completo (PDF de los autores) |
| | Solo si el presidente es popular | "Unpopular presidents, by contrast, are irrelevant" (resumen) | Confirmado | Texto completo |
| | Sobre todo en los primeros meses | En la conclusión: el efecto se concentra en los tres meses posteriores al informe y para el otoño puede haberse olvidado | Confirmado | Texto completo |
| | Un presidente popular mueve incluso a una cámara del partido rival; en la Cámara de Representantes el efecto dura más si la controla su partido | Encuentran "some support" para la hipótesis de gobierno unificado, solo en la Cámara de Representantes; en el Senado los resultados son mixtos; un presidente popular mueve también al Congreso del partido rival | Confirmado | Texto completo. **Corrección a la v2:** decía "con más probabilidad si su partido controla el Congreso", que exagera un poco: solo vale para la Cámara de Representantes y con apoyo parcial |
| **Olden y Møen (2022)** | Una triple diferencia es la resta de dos diferencias en diferencias; si las dos tienen el mismo sesgo, este se cancela y basta un supuesto de tendencias paralelas | Resumen: el estimador es "the difference between two difference-in-differences estimators" y no requiere dos supuestos de tendencias paralelas si el sesgo es el mismo en ambos | Confirmado | Página de la revista (resumen, leído a través de una herramienta que lo resume; no textual) |
| **Petrocik (1996)** | Cada partido tiene fama de manejar mejor ciertos temas y sus candidatos enfatizan esos temas en campaña; estudia campañas presidenciales en EE. UU. | Fuentes secundarias coinciden: la propiedad de temas es una reputación de manejo de políticas, y Petrocik la usa para explicar qué temas enfatizan los candidatos presidenciales | Confirmado solo con fuentes secundarias | JSTOR bloquea la descarga. **Pendiente:** que alguien con acceso de la universidad lea el resumen y la primera página |

Los datos bibliográficos (volumen, número y páginas) de los cinco coinciden con las fuentes.

## Otras afirmaciones con fuente

| Afirmación | Fuente | Estado |
|---|---|---|
| Los grupos registran sus asuntos a más tardar a las 13:00 del día anterior | Reglamento, art. 65.1.I | Confirmado (texto literal) |
| La Gaceta publica el orden del día a más tardar a las 22:00 del día anterior | Reglamento, art. 60.1 | Confirmado (texto literal) |
| El orden del día solo puede cambiarse si la Junta lo propone y el Pleno lo vota | Reglamento, art. 65.2 | Confirmado. **Agregado a la v3:** la v2 decía que el orden del día "se cerró", sin este matiz |
| Morena, con sus aliados, tenía mayoría en la Cámara de la LXV | Composición de la LXV (Morena, PT y PVEM suman más de 250 de 500) | Dato conocido; conviene citar la página de la Cámara si el profesor lo pide |

## Lo que quitamos

Ya no se citan Bevan (2019), Krippendorff (2004), Cengiz et al. (2019), Roth (2022), Santos Silva y Tenreyro (2006), Wooldridge (2023), Cameron, Gelbach y Miller (2011), MacKinnon y Webb (2020) ni Green-Pedersen y Mortensen (2010). Las decisiones de método que justificaban siguen en el texto, explicadas sin cita. La idea de Green-Pedersen y Mortensen, que en el parlamento la oposición tiene más libertad para quedarse en sus temas, se quitó junto con la cita. El CAP, el Reglamento, las estenográficas y NOSTRODATA pasaron a "Fuentes de datos y normas", como en la v2.
