# Libro de códigos de temas

Lo usan el modelo de lenguaje (el script `07_clasificar.py` lee este archivo y lo pone en sus instrucciones) y nosotros al codificar a mano. Si se cambia algo aquí, cambia para los dos: hay que volver a clasificar y volver a validar.

Los temas son los 21 temas principales del Comparative Agendas Project (Bevan 2019), con su número original, más el 0 para lo que no es política pública. Las notas para México son nuestras.

## Regla general

Se asigna **un solo tema**: el de la política pública de la que trata el texto. Si toca varios, se elige el que ocupa más espacio o el que es el centro del argumento. Si el texto no trata de ninguna política pública, va en 0.

## Temas

- **1 Economía**: crecimiento, inflación, tipo de cambio, desempleo en general, presupuesto federal y gasto público en general, impuestos, deuda pública, política monetaria y Banco de México.
- **2 Derechos civiles**: discriminación, igualdad de género, derechos de las mujeres y de la comunidad LGBT, pueblos indígenas como asunto de derechos, libertad de expresión y de prensa, privacidad, derechos humanos en general.
- **3 Salud**: sistema de salud, IMSS, ISSSTE e IMSS-Bienestar, abasto de medicamentos y vacunas, COVID-19 como asunto de salud, enfermedades, salud mental, adicciones como asunto de salud.
- **4 Agricultura**: campo, producción agrícola y ganadera, pesca, precios de garantía, Segalmex como programa agrícola, apoyos a productores, glifosato y maíz transgénico.
- **5 Trabajo**: empleo, salario mínimo, derechos laborales, sindicatos, outsourcing, pensiones y Afores como asunto laboral, seguridad en el trabajo.
- **6 Educación**: escuelas, maestros, SEP, libros de texto, universidades, becas educativas, reforma educativa.
- **7 Medio ambiente**: contaminación, cambio climático, agua como recurso natural, deforestación, áreas naturales, residuos, protección animal.
- **8 Energía**: petróleo, Pemex, electricidad, CFE, reforma eléctrica, gasolina y gas, litio, refinerías (Dos Bocas), energías renovables.
- **9 Migración**: migrantes, refugiados, frontera como asunto migratorio, deportaciones, remesas como asunto migratorio.
- **10 Transporte**: carreteras, aeropuertos (AIFA), trenes (Tren Maya, Tren Interoceánico), transporte público, Metro, aviación.
- **12 Justicia y seguridad**: delincuencia, violencia, homicidios, feminicidios como delito, narcotráfico, Guardia Nacional y policías como seguridad pública, cárceles, Fiscalía, jueces y sistema de justicia penal, desaparecidos, Ayotzinapa.
- **13 Bienestar social**: programas sociales (pensión para adultos mayores, Jóvenes Construyendo el Futuro, Sembrando Vida), pobreza, apoyos a personas con discapacidad, guarderías y cuidados.
- **14 Vivienda**: vivienda, Infonavit, desarrollo urbano, créditos de vivienda.
- **15 Comercio interno y finanzas**: bancos, empresas, competencia, protección al consumidor, turismo, pequeñas empresas, desastres naturales y protección civil, propiedad intelectual.
- **16 Defensa**: Fuerzas Armadas como institución militar (Sedena, Marina), militarización, presupuesto militar, espionaje militar (por ejemplo, Pegasus).
- **17 Tecnología y comunicaciones**: telecomunicaciones, internet, medios públicos como infraestructura, ciencia, Conacyt, espacio.
- **18 Comercio exterior**: T-MEC, aranceles, exportaciones e importaciones, inversión extranjera, disputas comerciales.
- **19 Asuntos internacionales**: relación con Estados Unidos y otros países, política exterior, embajadas, asilo diplomático, organismos internacionales.
- **20 Gobierno**: funcionamiento del gobierno y del Congreso, corrupción en el gobierno, elecciones e INE, reforma electoral, órganos autónomos, transparencia, servidores públicos, austeridad, relación entre poderes, Poder Judicial como poder (no como justicia penal), partidos políticos como instituciones.
- **21 Territorio y recursos públicos**: tierras federales, ejidos, concesiones de agua y minería, parques nacionales, asuntos territoriales de los estados.
- **23 Cultura**: arte, patrimonio, deporte, fiestas y conmemoraciones culturales.
- **0 Sin tema de política**: trámite parlamentario ("con su venia", saludos, agradecimientos), ataques o defensas personales sin una política detrás, rumores sobre la vida personal de alguien, desmentidos sobre la salud o la imagen del Presidente, críticas a un medio que no tratan de ninguna política.

## Casos difíciles

- **Programas sociales**: van en 13, salvo que sean claramente de un sector (becas escolares en 6, apoyos al campo en 4).
- **Violencia contra las mujeres**: si trata de delitos (feminicidios, denuncias), 12; si trata de igualdad o derechos, 2.
- **Guardia Nacional**: si trata de seguridad pública, 12; si trata de que pase a la Sedena o del papel del Ejército, 16.
- **Corrupción**: en el gobierno, 20; en una empresa privada, 15; si es un delito que investiga la Fiscalía, 12.
- **Desmentidos de la mañanera**: el tema es la política de la que trata la nota desmentida, no el hecho de que sea una mentira. "Es falso que falten medicamentos" va en 3. "Es falso que el Presidente esté enfermo" va en 0.

## Blanco del ítem (solo para la sección de la mañanera)

A quién desmiente el ítem:

- **medio**: un medio de comunicación, un periodista, un columnista o una cuenta de redes que no es de un político.
- **oposicion**: un político, partido u organización de oposición (PAN, PRI, PRD, MC, o personajes identificados con la oposición).
- **otro**: cualquier otro caso, o si no se sabe.
