# Página web · Dra. Dalila Peñaranda — Pediatría y Nutrición Infantil

Repositorio del sitio informativo de la Dra. Dalila Peñaranda (Barranquilla, Colombia). Contiene las propuestas de diseño de la fase de maquetas (`mockups/`) y el sitio en desarrollo (`docs/`).

## Sitio web (GitHub Pages)

El sitio real vive en la carpeta **`docs/`**, construido a partir del diseño aprobado (`DraDalilaInicio`): HTML semántico, `css/site.css`, `js/site.js` y assets optimizados con fuentes auto-hospedadas (Baloo 2 + Nunito). No usa frameworks ni dependencias.

### Páginas

| Archivo | Página |
|---|---|
| `index.html` | Inicio |
| `sobre-mi.html` | Sobre mí — historia, formación y principios de consulta |
| `servicios.html` | Servicios — seis bloques con ancla propia (`#nutricion-infantil`, `#crecimiento-desarrollo`, …) |
| `consultorio.html` | El consultorio — recorrido fotográfico, cómo llegar, horario y qué traer |
| `cursos.html` | Cursos en video — temarios, precios y compra en Hotmart |
| `blog.html` | Blog — destacado, filtro por categoría y rejilla de artículos |
| `blog-articulo.html` | Plantilla de artículo (así se verá cada entrada) |
| `citas.html` | Citas y tarifas — modalidades, pasos, convenios y condiciones |
| `contacto.html` | Contacto — formulario con consentimiento, datos directos y horario |
| `aviso-medico.html` · `privacidad.html` | Textos legales (borradores para revisión) |

La barra y el pie son idénticos en todas las páginas: si se cambia un enlace hay que cambiarlo en los once archivos (`grep -l` ayuda). La página activa se marca con `aria-current="page"` en su enlace del menú.

**Publicar en GitHub Pages:** en el repositorio ir a *Settings → Pages → Build and deployment*, elegir **Deploy from a branch**, seleccionar la rama (esta rama de trabajo o `main` una vez integrada) y la carpeta **`/docs`**, y guardar. En uno o dos minutos la página queda en `https://<usuario>.github.io/<repositorio>/`.

**Datos que se editan en un solo lugar:** al inicio de `docs/js/site.js` está el objeto `CONFIG` con el número de WhatsApp (visible y del enlace `wa.me`), correo, dirección, precios de las consultas, redes sociales, los enlaces de compra de Hotmart y dos interruptores (`mostrarPrecios`, `mostrarPepe`). Mientras `hotmart` esté vacío, los botones de los cursos escriben por WhatsApp en lugar de llevar a un enlace roto. El resto del contenido pendiente de la doctora (textos, cursos reales, testimonios reales, artículos del blog) se reemplaza directamente en el HTML de cada página; los textos de ejemplo están marcados como tales, y el pie lleva una nota de «versión de trabajo» que se borra al publicar.

**Formulario de contacto:** valida en el navegador, exige el consentimiento de la Ley 1581 de 2012 y, como todavía no hay servidor, arma el mensaje y lo abre en WhatsApp. Cuando exista backend (o WordPress), solo hay que reemplazar el bloque `form.addEventListener('submit', …)` de `docs/js/site.js`.

**Animaciones incluidas:** aparición suave de cada bloque al hacer scroll (con retardos escalonados y entrada lateral en los bloques de servicios y cursos), foto del hero que flota, línea de tiempo de la formación que se dibuja al aparecer, botón de WhatsApp con latido, tarjetas que se elevan al pasar el cursor, menú móvil, filtro del blog y preguntas frecuentes con apertura animada. Todo respeta `prefers-reduced-motion`.

**Franjas de mar:** ya no son una imagen única ni se repiten a mano en cada página. Se escriben así:

```html
<div class="franja franja--crema" data-escena="2"></div>
```

y `docs/js/franjas.js` las puebla: el oleaje se dibuja en SVG (cinco capas que derivan a distinta velocidad, generadas con una función de onda) y cada animalito es un elemento independiente recortado de `assets/img/mar/`. La tortuga rema, la ballena nada, el pez avanza a impulsos, las estrellas se balancean, los corales se mecen desde la base y las burbujas suben; cada uno con su propia duración y desfase, así que nunca se mueven en bloque. `data-escena` (0–5) elige el reparto y `franja--crema` / `franja--agua` el color del que viene; el color al que va se deduce solo, o se fuerza con `data-hasta="crema|agua"`. Para retocar un reparto se edita la receta correspondiente en `ESCENAS` (`nombre  izquierda%  ancho  altura%  duración  retraso`, y `:x` para ocultarlo en móvil).

**Previsualizar en local:** `cd docs && python3 -m http.server 8000` y abrir `http://localhost:8000` (las fuentes no cargan si se abre el archivo directamente con `file://`).

## Maquetas de diseño

Las propuestas de la fase de diseño están en `mockups/` (ver `mockups/README.md` y `mockups/index.html`).
