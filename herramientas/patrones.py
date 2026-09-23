#!/usr/bin/env python3
"""
Saca de docs/ cada sección del sitio y la deja como patrón del tema, para que
el community manager pueda insertarlas al armar una página nueva.

    python3 herramientas/patrones.py

La regla es la de siempre: no se cambia nada. Las secciones llevan SVG
dibujados a mano, fotos con cinta washi y rejillas propias, así que viajan como
bloque HTML —idénticas— salvo las que son texto puro, que se convierten en
bloques de verdad para que se editen con comodidad.
"""

import html
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RAIZ, 'docs')
PATRONES = os.path.join(RAIZ, 'wordpress', 'themes', 'dalila', 'patterns')

sys.path.insert(0, os.path.join(RAIZ, 'herramientas'))
from wordpress import (construir_mapa, reescribir, elementos, interior, etiqueta,  # noqa: E402
                       texto_plano, ORIGEN)

# Cada patrón: archivo de origen, marca del comentario que lo abre, nombre,
# título y descripción. El orden es el de la portada.
SECCIONES = [
    ('index.html', 'Hero',                   'portada-hero',        'Portada · Héroe',
     'El bloque de entrada: el titular, el texto, los dos botones y la foto en polaroid con su nota.'),
    ('index.html', 'Servicios',              'servicios',           'Servicios',
     'Las seis tarjetas de servicios con sus iconos dibujados.'),
    ('index.html', 'La doctora',             'conoce-a-la-doctora', 'Conoce a la doctora',
     'El retrato con los tres pilares, y la tarjeta de Pepe.'),
    ('index.html', 'Nutrición / crecimiento','nutricion-crecimiento','Nutrición y crecimiento',
     'Las dos tarjetas grandes de nutrición infantil y crecimiento.'),
    ('index.html', 'Consultorio',            'consultorio-portada', 'El consultorio, en la portada',
     'Las postales del consultorio con su pie de foto.'),
    ('index.html', 'Cursos',                 'cursos',              'Cursos y talleres',
     'Las tarjetas de los cursos, con el botón que lleva a Hotmart o a WhatsApp.'),
    ('index.html', 'Convenios',              'convenios',           'Convenios',
     'Los logos de las medicinas prepagadas y pólizas que atiende.'),
    ('index.html', 'Citas',                  'citas',               'Tu cita',
     'Las dos tarjetas de tarifa, presencial y virtual. Los precios salen de Ajustes → Datos del consultorio.'),
    ('index.html', 'Testimonios',            'testimonios',         'Testimonios',
     'Las tarjetas de testimonios con sus estrellas.'),
    ('index.html', 'Preguntas frecuentes',   'faq',                 'Preguntas frecuentes',
     'El acordeón de preguntas. Lo que se escriba aquí es lo que Google y los buscadores de respuestas leen.'),
    ('index.html', 'Contacto',               'banda-contacto',      'Banda de contacto',
     'La franja final con el teléfono, el correo y la dirección.'),
    ('blog.html',  None,                     'descarga-guia',       'Descarga de la guía',
     'El bloque del regalo: la portada del PDF, el texto y el botón de descarga.'),
]


def seccion_por_comentario(fuente, marca):
    """La sección que sigue a <!-- ===== marca ===== -->."""
    m = re.search(r'<!-- =+ %s =+ -->\s*' % re.escape(marca), fuente)
    if not m:
        return None
    resto = fuente[m.end():]
    piezas = elementos(resto)
    return piezas[0] if piezas else None


def seccion_descarga(fuente):
    i = fuente.find('<div class="descarga')
    if i < 0:
        return None
    return elementos(fuente[i:])[0]


# Los contenedores cuyos hijos son piezas repetidas: una tarjeta, una pregunta,
# un logo. Se parten en bloques sueltos para que añadir uno más sea duplicar y
# escribir, en vez de editar HTML a mano.
LISTAS = ('rejilla', 'faq__lista', 'logos', 'mosaico', 'pilares')


def clases_de(elemento):
    return (etiqueta(elemento, r'^<[^>]*\bclass="([^"]*)"') or '')


def nombre_de(elemento):
    return (etiqueta(elemento, r'^<([a-zA-Z][a-zA-Z0-9]*)') or '').lower()


def grupo(clases, ancla, dentro, etiqueta_html='div', alineado=False):
    atributos = {'className': clases, 'layout': {'type': 'default'}}
    if etiqueta_html != 'div':
        atributos['tagName'] = etiqueta_html
    if ancla:
        atributos['anchor'] = ancla
    if alineado:
        atributos['align'] = 'full'

    import json
    abre = '<%s class="wp-block-group%s %s"%s>' % (
        etiqueta_html,
        ' alignfull' if alineado else '',
        clases,
        ' id="%s"' % ancla if ancla else '')
    return ('<!-- wp:group %s -->\n%s\n%s\n</%s>\n<!-- /wp:group -->'
            % (json.dumps(atributos, ensure_ascii=False), abre, dentro, etiqueta_html))


def a_bloque(el):
    """Un elemento suelto: título y párrafo simples pasan a bloque de verdad."""
    nombre = nombre_de(el)
    cls = clases_de(el)
    dentro = interior(el)

    if nombre in ('h2', 'h3') and 'style=' not in el.split('>')[0]:
        import json
        atributos = {'level': int(nombre[1])}
        if cls:
            atributos['className'] = cls
        return ('<!-- wp:heading %s -->\n<%s class="wp-block-heading%s">%s</%s>\n<!-- /wp:heading -->'
                % (json.dumps(atributos, ensure_ascii=False), nombre,
                   ' ' + cls if cls else '', dentro, nombre))

    if nombre == 'p' and 'style=' not in el.split('>')[0] and 'svg' not in el.lower():
        import json
        atributos = {'className': cls} if cls else {}
        return ('<!-- wp:paragraph %s-->\n<p%s>%s</p>\n<!-- /wp:paragraph -->'
                % (json.dumps(atributos, ensure_ascii=False) + ' ' if atributos else '',
                   ' class="%s"' % cls if cls else '', dentro))

    return '<!-- wp:html -->\n%s\n<!-- /wp:html -->' % el


def estructurar(seccion):
    """
    Convierte <section><div class="wrap">… en grupos de WordPress, con los
    títulos y los párrafos como bloques editables y cada pieza repetida suelta.
    Si la sección no tiene esa forma, devuelve None y se guarda como HTML.
    """
    if nombre_de(seccion) != 'section':
        return None

    clases = clases_de(seccion)
    ancla = etiqueta(seccion, r'^<section[^>]*\bid="([^"]+)"')
    hijos = elementos(interior(seccion))
    if len(hijos) != 1 or 'wrap' not in clases_de(hijos[0]).split():
        return None

    piezas = []
    for el in elementos(interior(hijos[0])):
        el = el.strip()
        if not el:
            continue
        cls = clases_de(el).split()
        if any(c.split('--')[0] in LISTAS for c in cls):
            dentro = '\n\n'.join(
                '<!-- wp:html -->\n%s\n<!-- /wp:html -->' % item.strip()
                for item in elementos(interior(el)) if item.strip())
            piezas.append(grupo(clases_de(el), None, dentro))
        else:
            piezas.append(a_bloque(el))

    return grupo(clases, ancla, grupo('wrap', None, '\n\n'.join(piezas)),
                 etiqueta_html='section', alineado=True)


def llevar_imagenes_al_tema(cuerpo):
    """
    Un patrón se inserta en una página nueva, así que no puede depender del
    sitio viejo: sus imágenes se copian dentro del tema y se apuntan desde ahí.
    El community manager las cambia después por las suyas desde la biblioteca.
    """
    import shutil

    def mover(m):
        ruta = m.group(1)
        origen = os.path.join(DOCS, ruta)
        destino = os.path.join(os.path.dirname(PATRONES), ruta)
        if os.path.exists(origen):
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            if not os.path.exists(destino) or os.path.getmtime(origen) > os.path.getmtime(destino):
                shutil.copy2(origen, destino)
        return ('src="<?php echo esc_url( get_template_directory_uri() . \'/%s\' ); ?>"' % ruta)

    return re.sub(r'src="%s(assets/img/[^"]+)"' % re.escape(ORIGEN), mover, cuerpo)


CABECERA = '''<?php
/**
 * Title: %(titulo)s
 * Slug: dalila/%(nombre)s
 * Categories: dalila-secciones
 * Description: %(descripcion)s
 * Inserter: yes
 */
?>
'''


def escribir_patron(nombre, titulo, descripcion, cuerpo):
    ruta = os.path.join(PATRONES, nombre + '.php')
    contenido = CABECERA % {'titulo': titulo, 'nombre': nombre, 'descripcion': descripcion}

    estructurado = estructurar(cuerpo)
    if estructurado:
        contenido += estructurado + '\n'
        forma = 'bloques'
    else:
        contenido += '<!-- wp:html -->\n' + cuerpo.strip() + '\n<!-- /wp:html -->\n'
        forma = 'html'

    open(ruta, 'w', encoding='utf-8').write(contenido)
    return len(contenido), forma


def generar():
    mapa = construir_mapa()
    hechos = []

    for archivo, marca, nombre, titulo, descripcion in SECCIONES:
        fuente = open(os.path.join(DOCS, archivo), encoding='utf-8').read()
        cuerpo = seccion_descarga(fuente) if marca is None else seccion_por_comentario(fuente, marca)

        if not cuerpo:
            print('  ⚠ no se encontró «%s» en %s' % (marca or nombre, archivo))
            continue

        # Las clases de aparición las pone el JavaScript al hacer scroll; en un
        # patrón recién insertado estorban, porque dejan la sección invisible
        # hasta que alguien pase por encima.
        cuerpo = re.sub(r'\s+data-delay="\d+"', '', cuerpo)
        cuerpo = re.sub(r'(class="[^"]*?)\s*\breveal(?:--\w+)?\b', r'\1', cuerpo)
        cuerpo = re.sub(r'\s*class="\s*"', '', cuerpo)
        cuerpo = re.sub(r'\s{2,}', ' ', cuerpo)
        cuerpo = re.sub(r'\s+(/?)>', r'\1>', cuerpo)

        cuerpo = llevar_imagenes_al_tema(reescribir(cuerpo, mapa))
        peso, forma = escribir_patron(nombre, titulo, descripcion, cuerpo)
        hechos.append((nombre, peso, forma))

    return hechos


if __name__ == '__main__':
    for nombre, peso, forma in generar():
        print('%-24s %5.1f KB  %s' % (nombre, peso / 1024, forma))
