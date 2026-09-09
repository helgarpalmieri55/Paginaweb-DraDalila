# Página web · Dra. Dalila Peñaranda — Pediatría y Nutrición Infantil

Repositorio del sitio informativo de la Dra. Dalila Peñaranda (Barranquilla, Colombia). Contiene las propuestas de diseño de la fase de maquetas (`mockups/`) y el sitio en desarrollo (`docs/`).

## Sitio web (GitHub Pages)

El sitio real vive en la carpeta **`docs/`**, construido a partir del diseño aprobado (`DraDalilaInicio`): HTML semántico, `css/site.css`, `js/site.js` y assets optimizados con fuentes auto-hospedadas (Baloo 2 + Nunito). No usa frameworks ni dependencias.

**Publicar en GitHub Pages:** en el repositorio ir a *Settings → Pages → Build and deployment*, elegir **Deploy from a branch**, seleccionar la rama (esta rama de trabajo o `main` una vez integrada) y la carpeta **`/docs`**, y guardar. En uno o dos minutos la página queda en `https://<usuario>.github.io/<repositorio>/`.

**Datos que se editan en un solo lugar:** al inicio de `docs/js/site.js` está el objeto `CONFIG` con el número de WhatsApp (visible y del enlace `wa.me`), correo, dirección, precios de las consultas, redes sociales y dos interruptores (`mostrarPrecios`, `mostrarPepe`). El resto del contenido pendiente de la doctora (textos, cursos reales, testimonios reales, artículos del blog) se reemplaza directamente en `docs/index.html`; los textos de ejemplo están marcados como tales en la página.

**Animaciones incluidas:** aparición suave de cada bloque al hacer scroll (con retardos escalonados), olas que se mecen, foto del hero que flota, burbujas, botón de WhatsApp con latido, tarjetas que se elevan al pasar el cursor, menú móvil, enlace activo en la barra y preguntas frecuentes con apertura animada. Todo respeta `prefers-reduced-motion`.

**Previsualizar en local:** `cd docs && python3 -m http.server 8000` y abrir `http://localhost:8000` (las fuentes no cargan si se abre el archivo directamente con `file://`).

## Maquetas de diseño

Las propuestas de la fase de diseño están en `mockups/` (ver `mockups/README.md` y `mockups/index.html`).
