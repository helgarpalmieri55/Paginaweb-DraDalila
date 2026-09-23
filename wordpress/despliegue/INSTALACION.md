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

## 3 · El tema

Tiene dos caminos. El segundo es el que queda funcionando para siempre.

### La primera vez, a mano

1. Comprimir la carpeta `wordpress/themes/dalila` en un `dalila.zip`.
2. En el escritorio: **Apariencia → Temas → Añadir nuevo → Subir tema**.
3. Activar **Dra. Dalila Peñaranda**.

### De ahí en adelante, solo

Cada push a `main` que toque el tema lo sube solo. Para que funcione hay que
crear cuatro secretos en GitHub, en **Settings → Secrets and variables →
Actions → New repository secret**:

| Secreto | De dónde sale |
|---|---|
| `HOSTINGER_HOST` | Hostinger → **Archivos → Cuentas FTP**, campo «Servidor FTP» |
| `HOSTINGER_USER` | la misma pantalla, campo «Usuario FTP», empieza por `u` |
| `HOSTINGER_SSH_KEY` | la clave privada del par que se genera abajo |
| `HOSTINGER_RUTA` | `/home/uXXXXXXXX/domains/dalilapenaranda.com/public_html/wp-content/themes/dalila` |

**Generar el par de claves**, en tu computador:

```bash
ssh-keygen -t ed25519 -C "github-dalila" -f ~/.ssh/dalila-hostinger -N ""
```

- El contenido de `~/.ssh/dalila-hostinger.pub` se pega en Hostinger, en
  **Avanzado → Acceso SSH → Claves SSH**.
- El contenido de `~/.ssh/dalila-hostinger` —el archivo sin `.pub`, completo,
  con sus líneas `BEGIN` y `END`— se pega en el secreto `HOSTINGER_SSH_KEY`.

La conexión va por el puerto **65002**, que es el que usa Hostinger.

## 4 · El contenido

1. **Ajustes → Enlaces permanentes → Nombre de la entrada.** Esto primero, o
   las direcciones quedan mal.
2. **Herramientas → Importar → WordPress**, instalar el importador si lo pide.
3. Subir `wordpress/importacion/contenido.xml`.
4. Asignar todas las entradas al usuario de la doctora.
5. **Marcar «Descargar e importar los archivos adjuntos».** Sin esa casilla las
   imágenes no viajan.
6. Esperar. Son 49 imágenes y puede tardar unos minutos.

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
