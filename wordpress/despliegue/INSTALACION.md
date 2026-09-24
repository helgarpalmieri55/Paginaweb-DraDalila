# Poner el sitio en línea

Todo lo que hay que hacer, en orden. Dominio en Cloudflare, hosting en
Hostinger, tema y contenido desde este repositorio.

> **Importante, por el orden:** la importación descarga las imágenes desde
> `helgarpalmieri55.github.io`. Hay que **importar antes de apagar GitHub
> Pages**, no después.

---

## 1 · WordPress en Hostinger

1. En el panel de Hostinger, **Sitios web → Añadir sitio web → WordPress**.
2. Dominio: `dalilapenaranda.com`. Idioma: **Español (Colombia)**.
3. Cuando pida el tema de arranque, cualquiera sirve: lo vamos a reemplazar.
4. Anota el usuario y la contraseña del administrador.

## 2 · El dominio, desde Cloudflare

En Hostinger, en **Sitios web → Panel → Dominio**, aparecen la dirección IP del
servidor y los servidores de nombres.

En Cloudflare, en el dominio `dalilapenaranda.com` → **DNS → Registros**:

| Tipo | Nombre | Contenido | Proxy |
|---|---|---|---|
| A | `@` | la IP que da Hostinger | Proxy activado |
| A | `www` | la misma IP | Proxy activado |

Después, en Cloudflare → **SSL/TLS → Overview**, poner el modo en
**Full (strict)**.

> Este es el error que más se comete: si se deja en **Flexible**, el sitio entra
> en un bucle de redirecciones y no carga. Hay que esperar a que Hostinger
> termine de emitir su certificado —lo hace solo, en unos minutos— y recién ahí
> poner Full (strict).

## 3 · El tema, desplegado desde GitHub

Hostinger despliega desde GitHub la rama **`tema-wordpress`**, que contiene solo
el tema en su raíz. La arma sola la GitHub Action `rama-del-tema.yml` cada vez
que cambia algo del tema en `main`, después de revisar que el PHP compile y que
el JavaScript y el JSON estén bien.

En Hostinger, **Sitios web → Panel → Avanzado → Git**, el despliegue automático
queda así:

| Campo | Valor |
|---|---|
| Repositorio | `helgarpalmieri55/Paginaweb-DraDalila` |
| Rama | `tema-wordpress` |
| Carpeta | `wp-content/themes/dalila` |
| Despliegue automático | activado |

> **Nunca** apuntar el despliegue a la raíz del sitio ni a otra rama: se copiaría
> el repositorio entero —mockups, propuesta comercial, notas internas— en la web
> pública.

Después, en el escritorio de WordPress: **Apariencia → Temas → activar
«Dra. Dalila Peñaranda»**.

El posicionamiento —datos estructurados y etiquetas sociales— viene dentro del
tema, en `inc/posicionamiento.php`. No hay plugin aparte que instalar.

## 4 · El contenido

1. **Ajustes → Enlaces permanentes → Nombre de la entrada.** Esto primero, o
   las direcciones quedan mal.
2. **Herramientas → Importar → WordPress**, instalar el importador si lo pide.
3. Subir `wordpress/importacion/contenido.xml`.
4. Asignar todas las entradas al usuario de la doctora.
5. **Marcar «Descargar e importar los archivos adjuntos».** Sin esa casilla las
   imágenes no viajan.
6. **Desmarcar «Cambiar todas las URL importadas…».** Viene marcada y convierte
   los enlaces a una sección de la misma página (`#politicas`) en enlaces a la
   portada (`/#politicas`).
7. Esperar. Son 49 imágenes y puede tardar unos minutos.

Al terminar deben quedar 25 entradas, 10 páginas y 4 categorías.

## 5 · Dejar cada cosa en su lugar

**Ajustes → Lectura:**
- Tu página de inicio muestra: **Una página estática**
- Página de inicio: **Inicio**
- Página de entradas: **Blog**

**Apariencia → Editor → Plantillas:** revisar que la portada, el blog y el
artículo se vean bien.

**Ajustes → Datos del consultorio:** confirmar el teléfono, el correo, la
dirección, las tarifas y los enlaces de Hotmart.

**Apariencia → Editor → Estilos → Logo:** subir `assets/img/logo.webp` y el
icono del sitio.

## 6 · Que no quede lento

Hostinger trae **LiteSpeed Cache**. Activarlo y, en su asistente, dejar
encendidos el caché de páginas, la compresión y la carga diferida de imágenes.
Es lo que compensa que WordPress arme cada página con PHP.

## 7 · Apagar el sitio viejo

**Solo cuando el sitio nuevo esté andando y revisado.**

En el repositorio: **Settings → Pages → Source: None**.

---

## Lo que el community manager necesita saber

- **Escribe artículos** en Entradas → Añadir nueva, con su categoría y su imagen
  destacada.
- **Arma páginas** con el botón **+** → pestaña **Patrones** → *Secciones del
  sitio*.
- **Cambia los datos del consultorio** en Ajustes → Datos del consultorio, y se
  actualizan en todo el sitio de una vez.
- **No edita archivos del tema** desde WordPress: eso se pierde en el siguiente
  despliegue. Los textos, las imágenes y las páginas sí son suyos y no se tocan
  desde el repositorio.
