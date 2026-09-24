#!/usr/bin/env python3
"""
Convierte el sitio estático de docs/ en un archivo de importación de WordPress.

La regla es no cambiar nada: los textos, las imágenes y la estructura viajan tal
como están. Lo que era un párrafo queda como bloque de párrafo, para que el
community manager lo edite; lo que era una pieza propia con SVG —el aviso
médico, el botón de compartir, las tarjetas de «sigue leyendo»— queda como
bloque HTML, que es la única forma de que se vea idéntico.

    python3 herramientas/wordpress.py

Deja wordpress/importacion/contenido.xml, listo para
Herramientas → Importar → WordPress en el escritorio.

Las imágenes se traen desde el sitio actual, así que hay que importar ANTES de
bajar GitHub Pages.
"""

import html
import os
import sys
import re
import subprocess
import unicodedata
from datetime import datetime, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RAIZ, 'docs')
SALIDA = os.path.join(RAIZ, 'wordpress', 'importacion', 'contenido.xml')
# Los estilos que iban en línea, convertidos en clases (ver bloques.py).
HOJA_BLOQUES = os.path.join(RAIZ, 'wordpress', 'themes', 'dalila', 'assets', 'css', 'bloques.css')
# Las versiones del contenido que pudo tener dalilapenaranda.com: la que se
# importó y las que después se pasaron con la actualización del tema. Una
# página que sigue igual a cualquiera de ellas no se editó a mano y se puede
# actualizar. Cada vez que se publique una actualización, su commit se suma.
IMPORTADOS = ['ba1636b', '028508a', 'ef67d86']
MIGRACION = os.path.join(RAIZ, 'wordpress', 'themes', 'dalila', 'inc', 'migracion.php')
# Los resúmenes de las tarjetas del blog, para un sitio que ya se importó.
TARJETAS = os.path.join(RAIZ, 'wordpress', 'themes', 'dalila', 'inc', 'tarjetas.php')

# De dónde se descargan las imágenes durante la importación.
ORIGEN = 'https://helgarpalmieri55.github.io/Paginaweb-DraDalila/'
# El sitio nuevo.
DESTINO = 'https://dalilapenaranda.com/'

AUTOR = 'dalila'

# Donde quedan los PDF para descargar: dentro del tema.
DESCARGAS = DESTINO + 'wp-content/themes/dalila/assets/descargas/'

CATEGORIAS = {
    'nutricion':   ('nutricion', 'Nutrición'),
    'lactancia':   ('lactancia', 'Lactancia'),
    'salud':       ('salud', 'Salud'),
    'crecimiento': ('crecimiento', 'Crecimiento'),
}

# Las páginas, con el nombre que tendrán en la dirección.
PAGINAS = {
    'index.html':        ('inicio', 'Inicio'),
    'sobre-mi.html':     ('sobre-mi', 'Sobre mí'),
    'servicios.html':    ('servicios', 'Servicios'),
    'consultorio.html':  ('consultorio', 'El consultorio'),
    'cursos.html':       ('cursos', 'Cursos y talleres'),
    'blog.html':         ('blog', 'Blog'),
    'citas.html':        ('citas', 'Citas y tarifas'),
    'contacto.html':     ('contacto', 'Contacto'),
    'aviso-medico.html': ('aviso-medico', 'Aviso médico'),
    'privacidad.html':   ('privacidad', 'Política de privacidad'),
}


# ----------------------------------------------------------------- utilidades

def texto_plano(fragmento):
    fragmento = re.sub(r'<svg.*?</svg>', ' ', fragmento, flags=re.S)
    fragmento = re.sub(r'<br\s*/?>', ' ', fragmento)
    fragmento = re.sub(r'<[^>]+>', ' ', fragmento)
    return re.sub(r'\s+', ' ', html.unescape(fragmento)).strip()


def etiqueta(fuente, patron, grupo=1):
    m = re.search(patron, fuente, re.S)
    return m.group(grupo) if m else None


def apodo(texto):
    """El nombre corto que va en la dirección: sin tildes, ni signos, ni eñes."""
    texto = texto.lower().replace('ñ', 'n')
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    texto = re.sub(r'[^a-z0-9]+', '-', texto).strip('-')
    return re.sub(r'-{2,}', '-', texto)[:70].strip('-')


def fecha_de_alta(ruta):
    """El día que el archivo entró al repositorio."""
    salida = subprocess.run(
        ['git', 'log', '--diff-filter=A', '--format=%ad', '--date=iso-strict', '-1', '--', ruta],
        capture_output=True, text=True, cwd=RAIZ).stdout.strip()
    if not salida:
        return datetime.now(timezone.utc)
    return datetime.fromisoformat(salida)


def cdata(texto):
    return '<![CDATA[' + texto.replace(']]>', ']]]]><![CDATA[>') + ']]>'


# --------------------------------------------------- el mapa de direcciones

def construir_mapa():
    """De cada archivo del sitio viejo a su dirección en el sitio nuevo."""
    mapa = {}

    for archivo, (nombre, _) in PAGINAS.items():
        mapa[archivo] = '/' if archivo == 'index.html' else '/%s/' % nombre

    for archivo in sorted(os.listdir(DOCS)):
        if not archivo.startswith('blog-') or not archivo.endswith('.html'):
            continue
        fuente = open(os.path.join(DOCS, archivo), encoding='utf-8').read()
        titulo = texto_plano(etiqueta(fuente, r'<h1[^>]*>(.*?)</h1>') or archivo)
        mapa[archivo] = '/blog/%s/' % apodo(titulo)

    return mapa


def reescribir(fragmento, mapa):
    """Direcciones y rutas de imagen, del sitio viejo al nuevo."""
    for archivo, destino in mapa.items():
        fragmento = fragmento.replace('href="%s"' % archivo, 'href="%s"' % destino)
        fragmento = fragmento.replace('href="%s#' % archivo, 'href="%s#' % destino)
    # Las descargas viajan dentro del tema, porque el sitio viejo se va a bajar.
    fragmento = fragmento.replace('href="assets/descargas/', 'href="%s' % DESCARGAS)
    # Las imágenes apuntan al sitio actual: el importador las descarga y luego
    # reemplaza solo estas direcciones por las de la biblioteca de medios.
    fragmento = re.sub(r'(src|href)="(assets/[^"]+)"',
                       lambda m: '%s="%s%s"' % (m.group(1), ORIGEN, m.group(2)), fragmento)
    return fragmento


# ------------------------------------------------- de HTML a bloques

# Las etiquetas que se cierran solas.
SUELTAS = ('br', 'hr', 'img', 'input', 'source', 'meta', 'link')

ABRE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>', re.S)


def elementos(fragmento):
    """Los elementos de primer nivel de un trozo de HTML, en orden."""
    piezas, profundidad, inicio = [], 0, None

    for m in ABRE.finditer(fragmento):
        cierre, nombre, sola = m.group(1), m.group(2).lower(), m.group(3)

        if nombre in SUELTAS or sola:
            if profundidad == 0:
                piezas.append(fragmento[m.start():m.end()])
            continue

        if not cierre:
            if profundidad == 0:
                inicio = m.start()
            profundidad += 1
        else:
            profundidad -= 1
            if profundidad == 0 and inicio is not None:
                piezas.append(fragmento[inicio:m.end()])
                inicio = None

    return piezas


def interior(elemento):
    """Lo que hay dentro de la etiqueta más externa."""
    m = re.match(r'<[a-zA-Z][^>]*>(.*)</[a-zA-Z][a-zA-Z0-9]*>\s*$', elemento, re.S)
    return m.group(1).strip() if m else elemento


def clases(elemento):
    return (etiqueta(elemento, r'^<[^>]*\bclass="([^"]*)"') or '').split()


def bloque_html(elemento):
    return '<!-- wp:html -->\n%s\n<!-- /wp:html -->' % elemento.strip()


def a_bloques(fragmento):
    """
    Convierte el cuerpo de un artículo en bloques de WordPress.

    Lo que es texto corriente pasa a bloques de verdad, editables uno por uno.
    Lo que es una pieza propia del sitio —con SVG, con estilos en línea— se
    guarda como bloque HTML, que es la única manera de que se vea igual.
    """
    salida = []

    for el in elementos(fragmento):
        el = el.strip()
        if not el:
            continue

        nombre = (etiqueta(el, r'^<([a-zA-Z][a-zA-Z0-9]*)') or '').lower()
        cls = clases(el)
        tiene_estilo = 'style="' in el.split('>')[0]
        dentro = interior(el)

        # Párrafo corriente.
        if nombre == 'p' and not cls and not tiene_estilo:
            salida.append('<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->' % dentro)

        # Títulos.
        elif nombre in ('h2', 'h3', 'h4') and not tiene_estilo:
            nivel = int(nombre[1])
            extra = ' ' + ' '.join(cls) if cls else ''
            atributos = '{"level":%d%s}' % (
                nivel, ',"className":"%s"' % ' '.join(cls) if cls else '')
            salida.append(
                '<!-- wp:heading %s -->\n<%s class="wp-block-heading%s">%s</%s>\n<!-- /wp:heading -->'
                % (atributos, nombre, extra, dentro, nombre))

        # Listas.
        elif nombre in ('ul', 'ol') and not cls and not tiene_estilo:
            ordenada = ',"ordered":true' if nombre == 'ol' else ''
            items = []
            for li in elementos(dentro):
                items.append('<!-- wp:list-item -->\n<li>%s</li>\n<!-- /wp:list-item -->'
                             % interior(li))
            atributos = '{%s}' % ordenada.lstrip(',') if ordenada else ''
            salida.append('<!-- wp:list %s-->\n<%s class="wp-block-list">\n%s\n</%s>\n<!-- /wp:list -->'
                          % (atributos + ' ' if atributos else '', nombre, '\n'.join(items), nombre))

        # Cita destacada.
        elif nombre == 'blockquote' and not cls:
            salida.append('<!-- wp:quote -->\n<blockquote class="wp-block-quote">%s</blockquote>\n<!-- /wp:quote -->'
                          % dentro)

        # Figura con imagen y pie.
        elif nombre == 'figure' and '<img' in el:
            src = etiqueta(el, r'<img[^>]+src="([^"]+)"')
            alt = etiqueta(el, r'<img[^>]+alt="([^"]*)"') or ''
            pie = etiqueta(el, r'<figcaption[^>]*>(.*?)</figcaption>')
            # El bloque Imagen no guarda ancho ni alto en la etiqueta: si van,
            # el editor lo marca como bloque con contenido inesperado.
            salida.append(
                '<!-- wp:image {"sizeSlug":"large"} -->\n'
                '<figure class="wp-block-image size-large">'
                '<img src="%s" alt="%s"/>%s</figure>\n<!-- /wp:image -->'
                % (src, alt,
                   '<figcaption class="wp-element-caption">%s</figcaption>' % pie if pie else ''))

        # Separador.
        elif nombre == 'hr':
            salida.append('<!-- wp:separator -->\n<hr class="wp-block-separator has-alpha-channel-opacity"/>\n<!-- /wp:separator -->')

        # Todo lo demás se guarda tal cual: el aviso médico, el botón de
        # compartir, las tarjetas. Son piezas con SVG y estilos propios.
        else:
            salida.append(bloque_html(el))

    return '\n\n'.join(salida)


# ------------------------------------------------- el contenido de cada pieza

def cuerpo_del_articulo(fuente, mapa):
    """
    Todo lo que va dentro de la entrada: el texto, su franja de mar, los tres
    artículos que la doctora escogió para ese tema y su propio cierre.

    La firma de la autora no entra: esa sí es igual en los 25 y la pone la
    plantilla.
    """
    partes = []

    # 1 · El texto, en su sección de lectura.
    i = fuente.find('<div class="wrap prosa reveal">')
    j = fuente.find('</div>\n</section>', i)
    prosa = interior(fuente[i:j + len('</div>')])
    partes.append(
        '<!-- wp:group {"className":"seccion seccion--crema seccion--lectura","layout":{"type":"constrained"}} -->\n'
        '<div class="wp-block-group seccion seccion--crema seccion--lectura">\n'
        '<!-- wp:group {"className":"prosa","layout":{"type":"constrained"}} -->\n'
        '<div class="wp-block-group prosa">\n'
        + a_bloques(prosa) +
        '\n</div>\n<!-- /wp:group -->\n</div>\n<!-- /wp:group -->')

    # 2 · La franja de mar, con la escena que traía el artículo.
    escena = etiqueta(fuente[j:], r'<div class="franja franja--crema" data-escena="(\d+)"></div>') or '0'
    partes.append('<!-- wp:dalila/franja {"escena":%s,"desde":"crema","hasta":"agua","align":"full"} /-->' % escena)

    # 3 · «Sigue leyendo», con sus tres artículos escogidos a mano.
    k = fuente.find('Sigue leyendo')
    if k > 0:
        inicio = fuente.rfind('<section', 0, k)
        fin = fuente.find('</section>', k) + len('</section>')
        partes.append(CONVERSOR.convertir(fuente[inicio:fin]))

    # 4 · El cierre propio del artículo.
    m = re.search(r'<section class="cierre[^"]*">.*?</section>', fuente, re.S)
    if m:
        partes.append(CONVERSOR.convertir(m.group(0)))

    return reescribir('\n\n'.join(partes), mapa)


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bloques import Conversor  # noqa: E402

CONVERSOR = Conversor()


def cuerpo_de_la_pagina(fuente, mapa):
    """
    Una página entera, desde que abre <main> hasta que cierra, convertida en
    bloques: grupos con las clases del sitio, y títulos, párrafos y listas que
    se editan directo. Los dibujos y las piezas con datos propios quedan como
    bloque HTML (ver bloques.py).
    """
    i = fuente.find('<main')
    i = fuente.find('>', i) + 1
    j = fuente.rfind('</main>')
    if i < 1 or j < 0:
        # Las páginas legales no llevan <main>.
        i = fuente.find('<body>') + len('<body>')
        j = fuente.find('<footer class="pie">')

    cuerpo = '\n'.join(el for el in elementos(fuente[i:j])
                       if el.strip() and 'class="barra"' not in el[:80])

    return CONVERSOR.convertir(reescribir(cuerpo, mapa))


# ------------------------------------------------------------ el archivo WXR

CABECERA = """<?xml version="1.0" encoding="UTF-8"?>
<!--
  Contenido del sitio de la Dra. Dalila Peñaranda, listo para importar.
  Generado por herramientas/wordpress.py a partir de docs/.

  Se importa desde el escritorio en Herramientas → Importar → WordPress,
  marcando «Descargar e importar los archivos adjuntos».
-->
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
	<title>Dra. Dalila Peñaranda</title>
	<link>{destino}</link>
	<description>Pediatría y nutrición infantil en Barranquilla</description>
	<language>es-CO</language>
	<wp:wxr_version>1.2</wp:wxr_version>
	<wp:base_site_url>{destino}</wp:base_site_url>
	<wp:base_blog_url>{destino}</wp:base_blog_url>

	<wp:author>
		<wp:author_id>1</wp:author_id>
		<wp:author_login>{cdata_login}</wp:author_login>
		<wp:author_email>nutripedcm@gmail.com</wp:author_email>
		<wp:author_display_name>{cdata_nombre}</wp:author_display_name>
		<wp:author_first_name>{cdata_pila}</wp:author_first_name>
		<wp:author_last_name>{cdata_apellido}</wp:author_last_name>
	</wp:author>
"""


def bloque_categorias():
    filas = []
    for _, (nombre, titulo) in sorted(CATEGORIAS.items()):
        filas.append(
            '\t<wp:category>\n'
            '\t\t<wp:term_id>0</wp:term_id>\n'
            '\t\t<wp:category_nicename>%s</wp:category_nicename>\n'
            '\t\t<wp:category_parent></wp:category_parent>\n'
            '\t\t<wp:cat_name>%s</wp:cat_name>\n'
            '\t</wp:category>' % (nombre, cdata(titulo)))
    return '\n'.join(filas)


def item(titulo, nombre, contenido, resumen, fecha, post_id, tipo,
         estado='publish', categoria=None, orden=0, adjunto=None, miniatura=None, padre=0,
         tarjeta=None, fijo=False):
    fecha_wp = fecha.strftime('%Y-%m-%d %H:%M:%S')
    enlace = DESTINO + ('' if nombre == 'inicio' else nombre + '/')

    filas = [
        '\t<item>',
        '\t\t<title>%s</title>' % cdata(titulo),
        '\t\t<link>%s</link>' % enlace,
        '\t\t<pubDate>%s</pubDate>' % fecha.strftime('%a, %d %b %Y %H:%M:%S +0000'),
        '\t\t<dc:creator>%s</dc:creator>' % cdata(AUTOR),
        '\t\t<guid isPermaLink="false">%s?p=%d</guid>' % (DESTINO, post_id),
        '\t\t<description></description>',
        '\t\t<content:encoded>%s</content:encoded>' % cdata(contenido),
        '\t\t<excerpt:encoded>%s</excerpt:encoded>' % cdata(resumen),
        '\t\t<wp:post_id>%d</wp:post_id>' % post_id,
        '\t\t<wp:post_date>%s</wp:post_date>' % cdata(fecha_wp),
        '\t\t<wp:post_date_gmt>%s</wp:post_date_gmt>' % cdata(fecha_wp),
        '\t\t<wp:comment_status>%s</wp:comment_status>' % cdata('closed'),
        '\t\t<wp:ping_status>%s</wp:ping_status>' % cdata('closed'),
        '\t\t<wp:post_name>%s</wp:post_name>' % cdata(nombre),
        '\t\t<wp:status>%s</wp:status>' % cdata(estado),
        '\t\t<wp:post_parent>%d</wp:post_parent>' % padre,
        '\t\t<wp:menu_order>%d</wp:menu_order>' % orden,
        '\t\t<wp:post_type>%s</wp:post_type>' % cdata(tipo),
        '\t\t<wp:post_password></wp:post_password>',
        '\t\t<wp:is_sticky>%d</wp:is_sticky>' % (1 if fijo else 0),
    ]

    if categoria:
        nombre_cat, titulo_cat = CATEGORIAS[categoria]
        filas.append('\t\t<category domain="category" nicename="%s">%s</category>'
                     % (nombre_cat, cdata(titulo_cat)))

    if adjunto:
        filas.append('\t\t<wp:attachment_url>%s</wp:attachment_url>' % cdata(adjunto))

    if miniatura:
        filas.append(
            '\t\t<wp:postmeta>\n'
            '\t\t\t<wp:meta_key>%s</wp:meta_key>\n'
            '\t\t\t<wp:meta_value>%s</wp:meta_value>\n'
            '\t\t</wp:postmeta>' % (cdata('_thumbnail_id'), cdata(str(miniatura))))

    if tarjeta:
        filas.append(
            '\t\t<wp:postmeta>\n'
            '\t\t\t<wp:meta_key>%s</wp:meta_key>\n'
            '\t\t\t<wp:meta_value>%s</wp:meta_value>\n'
            '\t\t</wp:postmeta>' % (cdata('dalila_tarjeta'), cdata(tarjeta)))

    if tipo == 'page':
        filas.append(
            '\t\t<wp:postmeta>\n'
            '\t\t\t<wp:meta_key>%s</wp:meta_key>\n'
            '\t\t\t<wp:meta_value>%s</wp:meta_value>\n'
            '\t\t</wp:postmeta>' % (cdata('_wp_page_template'), cdata('default')))

    filas.append('\t</item>')
    return '\n'.join(filas)


def tarjetas():
    """El texto corto que cada artículo lleva en su tarjeta del blog, y cuál
    es el destacado. En el sitio es distinto de la entrada del artículo."""
    blog = open(os.path.join(DOCS, 'blog.html'), encoding='utf-8').read()
    textos = {}
    for m in re.finditer(r'<article class="articulo[^"]*"[^>]*>(?:(?!</article>).)*?<h3>.*?</h3>\s*<p>(.*?)</p>'
                         r'(?:(?!</article>).)*?href="([^"]+)"', blog, re.S):
        textos[m.group(2)] = texto_plano(m.group(1))

    destacado = None
    d = re.search(r'<article class="destacado.*?</article>', blog, re.S)
    if d:
        destacado = etiqueta(d.group(0), r'href="(blog-[^"]+)"')
        texto = etiqueta(d.group(0), r'</h2>\s*<p>(.*?)</p>')
        if destacado and texto:
            textos[destacado] = texto_plano(texto)

    return textos, destacado


def escribir_tarjetas(por_nombre, destacado):
    """Los mismos resúmenes en PHP, para pasarlos a un sitio ya importado."""
    filas = ['<?php',
             '/**',
             ' * Generado por herramientas/wordpress.py. No se edita a mano.',
             ' *',
             ' * Los resúmenes de las tarjetas del blog y el artículo destacado, tal como',
             ' * estaban en el sitio. inc/blog.php los copia una sola vez a cada entrada;',
             ' * después se editan desde el campo personalizado «dalila_tarjeta».',
             ' *',
             ' * @package dalila',
             ' */',
             '',
             "if ( ! defined( 'ABSPATH' ) ) {",
             '\texit;',
             '}',
             '',
             'return array(',
             "\t'destacado' => %s," % ("'%s'" % destacado if destacado else 'null'),
             "\t'tarjetas'  => array("]
    for nombre in sorted(por_nombre):
        texto = por_nombre[nombre].replace('\\', '\\\\').replace("'", "\\'")
        filas.append("\t\t'%s' => '%s'," % (nombre, texto))
    filas += ['\t),', ');', '']
    open(TARJETAS, 'w', encoding='utf-8').write('\n'.join(filas))


def normalizar(contenido):
    """El contenido sin las direcciones de las imágenes, que el importador
    cambia al subirlas. Es la misma cuenta que hace inc/actualizacion.php."""
    contenido = contenido.replace('\r\n', '\n')
    contenido = re.sub(r'https?://[^"\'\s)]+/([^/"\'\s)]+\.(?:webp|jpe?g|png|gif|svg|pdf))',
                       r'\1', contenido, flags=re.I)
    # WordPress le agrega «-1», «-scaled» o las medidas al nombre si ya existe.
    contenido = re.sub(r'(?:-\d+x\d+|-scaled|-\d+)+(\.(?:webp|jpe?g|png|gif|svg|pdf))\b',
                       r'\1', contenido, flags=re.I)
    return contenido.strip()


def contenidos_del_xml(texto):
    """(tipo, nombre) → contenido, de un archivo de importación."""
    salida = {}
    for item in re.findall(r'<item>(.*?)</item>', texto, re.S):
        tipo = etiqueta(item, r'<wp:post_type><!\[CDATA\[(.*?)\]\]>')
        if tipo not in ('post', 'page'):
            continue
        nombre = etiqueta(item, r'<wp:post_name><!\[CDATA\[(.*?)\]\]>')
        cuerpo = etiqueta(item, r'<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>') or ''
        salida[(tipo, nombre)] = cuerpo.replace(']]]]><![CDATA[>', ']]>')
    return salida


def escribir_migracion(nuevo_xml):
    """Para un sitio ya importado: el contenido nuevo de cada página y
    entrada, y la huella del que se importó, para no pisar lo que se editó."""
    import hashlib
    viejos = {}
    for version in IMPORTADOS:
        xml = subprocess.run(['git', 'show', '%s:wordpress/importacion/contenido.xml' % version],
                             capture_output=True, text=True, cwd=RAIZ).stdout
        for clave, contenido in contenidos_del_xml(xml).items():
            viejos.setdefault(clave, []).append(contenido)
    nuevos = contenidos_del_xml(nuevo_xml)

    def php(texto):
        return "'" + texto.replace('\\', '\\\\').replace("'", "\\'") + "'"

    filas = ['<?php',
             '/**',
             ' * Generado por herramientas/wordpress.py. No se edita a mano.',
             ' *',
             ' * El contenido de cada página y entrada convertido a bloques editables,',
             ' * para pasarlo a un sitio que ya se había importado. inc/actualizacion.php',
             ' * lo aplica una sola vez y solo donde nadie editó desde la importación.',
             ' *',
             ' * @package dalila',
             ' */',
             '',
             "if ( ! defined( 'ABSPATH' ) ) {",
             '\texit;',
             '}',
             '',
             'return array(']
    for (tipo, nombre), contenido in sorted(nuevos.items()):
        huellas = sorted({hashlib.md5(normalizar(a).encode()).hexdigest()
                          for a in viejos.get((tipo, nombre), [])
                          if normalizar(a) != normalizar(contenido)})
        if not huellas:
            continue
        filas += ['\tarray(',
                  "\t\t'tipo'      => '%s'," % tipo,
                  "\t\t'nombre'    => '%s'," % nombre,
                  "\t\t'antes'     => array( %s )," % ', '.join("'%s'" % h for h in huellas),
                  "\t\t'contenido' => %s," % php(contenido),
                  '\t),']
    filas += [');', '']
    open(MIGRACION, 'w', encoding='utf-8').write('\n'.join(filas))


def imagenes_del_sitio():
    """Todas las imágenes que el sitio usa de verdad, sin repetir."""
    usadas = []
    vistas = set()
    for archivo in sorted(os.listdir(DOCS)):
        if not archivo.endswith('.html'):
            continue
        fuente = open(os.path.join(DOCS, archivo), encoding='utf-8').read()
        for ruta in re.findall(r'<img[^>]+src="(assets/img/[^"]+)"', fuente):
            if ruta not in vistas and os.path.exists(os.path.join(DOCS, ruta)):
                vistas.add(ruta)
                usadas.append(ruta)
    return usadas


def generar():
    mapa = construir_mapa()
    fecha_base = datetime.now(timezone.utc)
    partes = [CABECERA.format(
        destino=DESTINO.rstrip('/'),
        cdata_login=cdata(AUTOR),
        cdata_nombre=cdata('Dra. Dalila Peñaranda'),
        cdata_pila=cdata('Dalila'),
        cdata_apellido=cdata('Peñaranda'),
    ), bloque_categorias()]

    # --- las imágenes, primero, para que las entradas puedan apuntarlas
    id_de = {}
    siguiente = 100
    for ruta in imagenes_del_sitio():
        id_de[ruta] = siguiente
        partes.append(item(
            titulo=os.path.basename(ruta).rsplit('.', 1)[0].replace('-', ' '),
            nombre=apodo(os.path.basename(ruta).rsplit('.', 1)[0]),
            contenido='', resumen='',
            fecha=fecha_base, post_id=siguiente, tipo='attachment', estado='inherit',
            adjunto=ORIGEN + ruta))
        siguiente += 1

    # --- los 25 artículos
    articulos = 0
    textos, destacado = tarjetas()
    por_nombre = {}
    nombre_destacado = None
    for archivo in sorted(os.listdir(DOCS)):
        if not archivo.startswith('blog-') or not archivo.endswith('.html'):
            continue
        fuente = open(os.path.join(DOCS, archivo), encoding='utf-8').read()

        titulo = texto_plano(etiqueta(fuente, r'<h1[^>]*>(.*?)</h1>'))
        resumen = texto_plano(etiqueta(fuente, r'<p class="cabecera__lead[^"]*"[^>]*>(.*?)</p>') or '')
        portada = etiqueta(fuente, r'<meta property="og:image" content="[^"]*?(assets/img/[^"]+)"')
        categoria = etiqueta(fuente, r'<span class="chip[^"]*">([a-zá-ú]+)</span>')

        # La categoría fiable es la que el blog le pone a su tarjeta. El artículo
        # destacado no tiene tarjeta, así que se toma la de su distintivo.
        blog = open(os.path.join(DOCS, 'blog.html'), encoding='utf-8').read()
        m = re.search(r'<article[^>]*data-cat="([^"]*)"[^>]*>(?:(?!</article>).)*?href="%s"' % re.escape(archivo),
                      blog, re.S)
        if m:
            categoria = m.group(1)
        else:
            d = re.search(r'<div class="destacado.*?href="%s"' % re.escape(archivo), blog, re.S)
            if d:
                chip = etiqueta(d.group(0), r'<span class="chip[^"]*">([^<]+)</span>')
                categoria = apodo(chip) if chip else categoria
        if categoria not in CATEGORIAS:
            raise SystemExit('sin categoría fiable para %s' % archivo)

        if archivo in textos:
            por_nombre[apodo(titulo)] = textos[archivo]
        if archivo == destacado:
            nombre_destacado = apodo(titulo)

        partes.append(item(
            titulo=titulo,
            nombre=apodo(titulo),
            contenido=cuerpo_del_articulo(fuente, mapa),
            resumen=resumen,
            fecha=fecha_de_alta(os.path.join(DOCS, archivo)),
            post_id=siguiente, tipo='post', categoria=categoria,
            miniatura=id_de.get(portada),
            tarjeta=textos.get(archivo), fijo=archivo == destacado))
        siguiente += 1
        articulos += 1

    # --- las 10 páginas
    paginas = 0
    for archivo, (nombre, titulo) in PAGINAS.items():
        ruta = os.path.join(DOCS, archivo)
        fuente = open(ruta, encoding='utf-8').read()
        partes.append(item(
            titulo=titulo,
            nombre=nombre,
            contenido=cuerpo_de_la_pagina(fuente, mapa),
            resumen=html.unescape(etiqueta(fuente, r'<meta name="description" content="(.*?)">') or ''),
            fecha=fecha_de_alta(ruta),
            post_id=siguiente, tipo='page', orden=paginas))
        siguiente += 1
        paginas += 1

    escribir_tarjetas(por_nombre, nombre_destacado)
    open(HOJA_BLOQUES, 'w', encoding='utf-8').write(CONVERSOR.hoja())

    partes.append('</channel>\n</rss>\n')

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    open(SALIDA, 'w', encoding='utf-8').write('\n'.join(partes))
    escribir_migracion('\n'.join(partes))

    return len(id_de), articulos, paginas


if __name__ == '__main__':
    imagenes, articulos, paginas = generar()
    print('imágenes:  %d' % imagenes)
    print('artículos: %d' % articulos)
    print('páginas:   %d' % paginas)
    print('archivo:   %s (%.0f KB)' % (
        os.path.relpath(SALIDA, RAIZ), os.path.getsize(SALIDA) / 1024))
