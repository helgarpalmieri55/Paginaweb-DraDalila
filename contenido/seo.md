# Posicionamiento del sitio de la Dra. Dalila Peñaranda

Objetivo: que cuando una familia de Barranquilla busque una pediatra, aparezca ella.
Este documento explica qué encontramos, qué ya quedó aplicado en el sitio y qué falta
—que es, sobre todo, lo que no depende del código.

Fecha del análisis: 17 de septiembre de 2026.

---

## 1 · Qué pasa hoy cuando alguien busca «pediatra en Barranquilla»

Miramos la búsqueda real. Los primeros lugares no los ocupan pediatras: los ocupan
**directorios médicos** con años de antigüedad y miles de páginas —Doctoralia,
Top Doctors, DoctorAkí, medicosdoc, probienestar— y **IPS con varias sedes**, entre
ellas Pedinorte, que atiende pediatría en el mismo High Park donde está el consultorio
de la doctora.

Eso significa dos cosas, y conviene decirlas sin adornos:

1. **Un sitio nuevo no le gana a un directorio en esa búsqueda exacta**, ni este mes
   ni el próximo. Esas páginas llevan años acumulando enlaces y reseñas.
2. **La pelea real se da en otro lado**: en el mapa de Google, en los perfiles de
   directorio que ella ya tiene, y en las búsquedas más específicas donde el
   contenido de la doctora sí es mejor que el de cualquier directorio.

Por encima de los resultados normales, Google muestra un **bloque de mapa con tres
consultorios**. Ese bloque no se gana con la página web: se gana con la ficha de
Google, la cercanía de quien busca y las reseñas. Es, de lejos, lo que más tráfico
se lleva en una búsqueda como esta.

---

## 2 · El hallazgo más importante: sus datos viejos siguen circulando

La doctora **ya tiene perfiles publicados** que no controlamos y que aparecen antes
que el sitio:

- **Doctoralia** — `doctoralia.co/dalila-maria-penaranda-saurith/pediatra/barranquilla`
- **medicosdoc** — `medicosdoc.com/perfil-medico/4574/dalila-penaranda-saurith/pediatra-barranquilla`

El perfil de Doctoralia muestra una dirección **distinta a la actual**: Calle 85 No
50-37, consultorio 807, Torre Mar Center. La guía nutricional traía otra dirección
vieja, también en la Calle 85. Hoy el consultorio está en la Calle 1C # 30-40, High
Park Medical Center, consultorio 129.

Que el nombre, la dirección y el teléfono aparezcan distintos en cada sitio es una de
las cosas que más daño hace en búsqueda local: Google no sabe cuál creer y reparte la
confianza. **Unificar esos tres datos en todas partes es la tarea número uno**, y no
cuesta dinero, solo entrar a cada perfil y corregirlo.

Otra cosa que conviene saber: su nombre completo es **Dalila María Peñaranda Saurith**,
y así aparece en los directorios y en el registro médico. En el sitio siempre decimos
«Dra. Dalila Peñaranda». Vale la pena que el nombre completo aparezca al menos una vez
en la página «Sobre mí», para que Google entienda que la del sitio, la de Doctoralia y
la del registro son la misma persona.

---

## 3 · Lo que quedó aplicado en el sitio

### SEO técnico

- **`sitemap.xml`** con las 35 páginas, cada una con su fecha y su prioridad.
- **`robots.txt`** que declara el sitemap. *(Ojo: mientras el sitio viva en una
  subcarpeta de `github.io`, los buscadores no lo leen —ver el punto 5.)*
- **Canónicas absolutas** en las 35 páginas, para que no se indexen versiones
  duplicadas de la misma URL.
- **`meta robots`** con `max-image-preview:large`, que permite a Google mostrar la
  foto grande en el resultado en lugar de una miniatura.
- **Fechas reales** de publicación y de última modificación en cada artículo,
  visibles para el lector y legibles para el buscador.

### Datos estructurados (JSON-LD)

Cada página lleva ahora un bloque que le describe el negocio a Google en su propio
idioma:

- **`Physician` + `MedicalBusiness`**: nombre, dirección completa, teléfono, correo,
  especialidades (pediatría y nutrición), zona que atiende, los seis servicios y el
  Instagram.
- **`Person`**: la doctora, su cargo y los temas que domina, enlazada al consultorio.
- **`BreadcrumbList`**: la ruta de migas, que Google muestra en lugar de la URL cruda.
- **`BlogPosting`** en los 25 artículos, con autora, fecha y medio.
- **`FAQPage`** en la home, en citas y en cursos.

Lo que **no** pusimos, a propósito: horarios de atención, títulos universitarios,
registro médico y reseñas. Ninguno está confirmado todavía, y un dato inventado en
los datos estructurados es peor que no ponerlo —Google penaliza el marcado que no
corresponde con la realidad.

### AEO · que ChatGPT, Perplexity y los resúmenes de Google la citen

Los motores de respuesta no «rankean»: leen y citan. Para que citen bien hace falta
que el texto responda la pregunta de una, con quién lo dice y desde dónde:

- **Preguntas frecuentes en la home**, de cuatro pasaron a ocho, y ahora incluyen las
  que la gente realmente escribe: dónde queda el consultorio, si atiende con prepagada
  o póliza, en qué se diferencia el control pediátrico de la consulta de nutrición, y
  si atiende urgencias (no, y se explica a dónde ir).
- **Firma de autora al pie de cada artículo**, con foto, credencial y enlaces. Para
  contenido de salud, saber quién firma es lo que más pesa.
- **Firma con fecha y enlace** en la entradilla de los 25 artículos.
- Los artículos ya venían bien escritos para esto: dicen la conclusión en las primeras
  líneas en lugar de guardarla para el final.

### GEO · que los modelos generativos tengan de dónde leer

- **`llms.txt`**: un resumen en texto plano del consultorio, los servicios, los datos
  de contacto y los 25 artículos con su descripción. Es una convención joven y ningún
  motor promete leerla, pero el archivo pesa 9 KB y no estorba.
- Los datos de contacto y los precios **están en el HTML**, no solo inyectados por
  JavaScript. La mayoría de los rastreadores de los modelos no ejecutan JavaScript;
  si el teléfono solo apareciera al ejecutarlo, sería invisible para ellos.

### Compartir por WhatsApp

Se compuso una **tarjeta social de 1200×630** (`assets/img/og-portada.jpg`) con el
logo, el titular y el retrato de la doctora. Antes se compartía una foto vertical que
WhatsApp recortaba mal. Se generó también la tarjeta de Twitter y las etiquetas
`og:` completas —antes la imagen iba en ruta relativa, que las redes no resuelven, así
que muchas veces no se veía ninguna.

Todo esto lo regenera `herramientas/seo.py`. Se puede volver a ejecutar cuantas veces
haga falta y no toca los títulos ni las descripciones escritos a mano.

---

## 4 · Lo que no depende del sitio, y pesa más

Ordenado por lo que más mueve la aguja:

### 4.1 · Ficha de Google del consultorio — **lo más importante de esta lista**

Es gratis y es lo que decide quién sale en el mapa. Hay que crearla o reclamarla en
`business.google.com` con:

- Nombre: *Dra. Dalila Peñaranda — Pediatría y Nutrición Infantil*
- Categoría principal: **Pediatra**. Secundaria: **Nutricionista**.
- La dirección exacta del High Park, con el pin puesto a mano en la entrada correcta.
- El teléfono y el sitio web.
- **Horarios reales de atención** (siguen pendientes de que ella los confirme).
- Fotos del consultorio —ya las tenemos, las seis.
- Los servicios, que se pueden copiar de la página de servicios.

Sin esta ficha, no hay búsqueda local que funcione. Con ella verificada, la doctora
entra a competir en el bloque del mapa desde el primer mes.

### 4.2 · Reseñas de pacientes reales

El bloque del mapa ordena, en buena medida, por cantidad y frescura de reseñas. Diez
reseñas reales valen más que cualquier cosa que hagamos en el código.

Lo práctico: un mensaje corto por WhatsApp un día después de la consulta, con el
enlace directo para reseñar. Nada de incentivos —Google los penaliza.

Esto además destraba algo del sitio: hoy los tres testimonios de la home son de
relleno, con nombres inventados y cinco estrellas. **Hay que reemplazarlos por
testimonios reales o quitarlos.** Mientras sean inventados no podemos marcarlos como
reseñas en los datos estructurados, y si alguien lo nota, cuesta credibilidad.

### 4.3 · Corregir Doctoralia y medicosdoc

Entrar a los dos perfiles, actualizar dirección, teléfono y foto, y enlazar al sitio.
Dos beneficios: dejan de circular datos viejos, y los perfiles —que ya rankean bien—
mandan tráfico y señales de confianza al sitio.

### 4.4 · Los resultados de prensa

Al buscar su nombre completo aparecen primero notas de prensa de 2020 sobre un hecho
personal, no su consulta. No se borran ni se piden bajar: lo que funciona es que sus
propios perfiles —sitio, ficha de Google, Doctoralia, Instagram— sean tan sólidos que
ocupen los primeros lugares. La ficha de Google y el sitio con dominio propio son
justamente eso. Es una decisión de ella, no nuestra, y conviene consultarla antes de
mover nada.

---

## 5 · El dominio propio

Hoy el sitio vive en `helgarpalmieri55.github.io/Paginaweb-DraDalila/`. Eso trae tres
problemas concretos:

1. **El `robots.txt` no se lee.** Los buscadores lo buscan en la raíz del dominio
   (`helgarpalmieri55.github.io/robots.txt`), que no es nuestra. El archivo que
   generamos queda inerte hasta que haya dominio propio. El sitemap sí se puede
   entregar a mano en Search Console.
2. **No transmite confianza.** Una familia que compara pediatras no espera el nombre
   de usuario de una agencia en la barra de direcciones.
3. **No hay correo con dominio.** Hoy el contacto es una cuenta de Gmail; un
   `hola@dradalilapenaranda.com` pesa en la percepción y en la verificación de la
   ficha de Google.

Un `.com` cuesta del orden de 50.000 pesos al año y GitHub Pages lo soporta sin
cambiar nada del sitio: se agrega un archivo `CNAME`, se apuntan los DNS y se vuelve a
ejecutar `herramientas/seo.py` con la constante `BASE` cambiada. Es media hora de
trabajo. **Es la mejor relación esfuerzo/resultado de toda esta lista después de la
ficha de Google.**

---

## 6 · Dónde sí se puede ganar pronto

No en «pediatra en Barranquilla», sino en las búsquedas largas donde los directorios
no tienen nada que decir y los 25 artículos sí:

- «mi hijo dejó de comer al año»
- «por qué ronca mi hijo al dormir»
- «cuándo puede tomar agua un bebé»
- «cómo hacer lavado nasal a un bebé»
- «qué leche dar después del destete»
- «se puso morado al llorar»

Son búsquedas de mamás preocupadas a las once de la noche. Traen menos volumen, pero
llegan con la duda exacta que ella resuelve, y de ahí salen pacientes. Cada artículo
cierra invitando a agendar, así que el camino está hecho.

**Lo que falta para que esto rinda de verdad: que la doctora revise los 25 artículos.**
Son textos médicos con su nombre y su cara. Google evalúa el contenido de salud con
una vara más alta que cualquier otro, y un error clínico ahí cuesta más que diez
aciertos técnicos.

---

## 7 · Cómo medirlo

1. **Google Search Console** — verificar el sitio, entregar el sitemap a mano, y
   revisar cada mes qué búsquedas traen visitas. Es gratis y es la única fuente que
   dice la verdad.
2. **Estadísticas de la ficha de Google** — cuántos pidieron cómo llegar, cuántos
   llamaron. Ahí se ve el efecto real.
3. **Señal propia**: preguntar en la primera consulta «¿cómo me encontró?». Sigue
   siendo el dato más honesto de todos.

Qué esperar, con los pies en la tierra: el primer mes no pasa nada visible; entre el
segundo y el tercero empiezan a entrar los artículos por búsquedas largas; el mapa
depende de cuándo se cree la ficha y de cuántas reseñas se junten. «Pediatra en
Barranquilla» a secas es una meta de un año, y llega por acumulación, no por un truco.

---

## 8 · Resumen de lo que hay que pedirle a la doctora

| Qué | Para qué | Quién |
|---|---|---|
| Crear o reclamar la ficha de Google | Salir en el mapa | Ella, con nuestra ayuda |
| Horarios reales de atención | Completar la ficha y los datos estructurados | Ella |
| Pedir reseñas a pacientes | Subir en el mapa | Ella |
| Testimonios reales para la home | Quitar los de relleno | Ella |
| Corregir Doctoralia y medicosdoc | Unificar sus datos | Nosotros, con su clave |
| Revisar los 25 artículos | Publicarlos con respaldo clínico | Ella |
| Decidir el dominio propio | Confianza, correo, `robots.txt` | Cliente |
| Credenciales y registro médico | Completar «Sobre mí» y el marcado | Ella |
