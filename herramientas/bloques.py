#!/usr/bin/env python3
"""
De HTML del sitio a bloques de WordPress que se editan uno por uno.

Recorre cada sección hasta el fondo:

- las cajas (section, div, article, aside, header, footer) pasan a bloques
  Grupo con las mismas clases, así que el diseño no cambia;
- los títulos, los párrafos y las listas pasan a sus bloques, y su texto se
  escribe directo sobre la página;
- los dibujos SVG, los botones, las imágenes sueltas y todo lo que depende de
  atributos propios (data-*, aria-*) se queda como bloque HTML, idéntico.

Los estilos en línea no caben en un bloque Grupo o Párrafo, así que cada uno
se convierte en una clase («en-xxxxxx») y se escribe en una hoja aparte,
con !important para que pese lo mismo que pesaba en línea.
"""

import hashlib
import html as html_lib
import json
import re

# Etiquetas que forman bloques: si aparecen dentro de algo, ese algo no es texto.
DE_BLOQUE = ('div', 'section', 'article', 'aside', 'header', 'footer', 'main', 'nav',
             'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'figure',
             'form', 'table', 'blockquote', 'details', 'hr', 'dl', 'fieldset')
HAY_BLOQUE = re.compile(r'<(?:%s)\b' % '|'.join(DE_BLOQUE), re.I)

# Las cajas que un Grupo sabe ser.
CAJAS = ('div', 'section', 'article', 'aside', 'header', 'footer', 'main')

# Lo que no se convierte nunca: dibujos, tablas, formularios, multimedia.
INTOCABLES = ('svg', 'form', 'select', 'textarea',
              'input', 'button', 'iframe', 'script', 'style', 'video', 'audio', 'picture',
              'canvas', 'hr', 'br')
HAY_INTOCABLE = re.compile(r'<(?:%s)\b' % '|'.join(t for t in INTOCABLES if t not in ('svg', 'br')), re.I)
SVG = re.compile(r'<svg\b.*?</svg>', re.S | re.I)


# Lo que puede ir dentro de un texto editable sin romperlo.
EN_LINEA = {'a', 'abbr', 'b', 'bdi', 'br', 'cite', 'code', 'data', 'del', 'em', 'i', 'ins',
            'kbd', 'mark', 'q', 's', 'small', 'span', 'strong', 'sub', 'sup', 'time', 'u', 'wbr'}


def solo_en_linea(fragmento):
    return all(t.lower() in EN_LINEA for t in re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)', SVG.sub('', fragmento)))


def texto_visible(fragmento):
    return re.sub(r'\s+', '', html_lib.unescape(re.sub(r'<[^>]+>', '', SVG.sub('', fragmento))))


def escapar(valor):
    return valor.replace('&', '&amp;').replace('"', '&quot;')

SUELTAS = ('br', 'hr', 'img', 'input', 'source', 'meta', 'link', 'wbr')
ETIQUETA = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>', re.S)
ATRIBUTO = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:\s*=\s*"([^"]*)")?')


def piezas(fragmento):
    """Los nodos de primer nivel: elementos y trozos de texto, en orden."""
    salida, profundidad, inicio, ultimo = [], 0, None, 0

    for m in ETIQUETA.finditer(fragmento):
        cierre, nombre, sola = m.group(1), m.group(2).lower(), m.group(3)

        if profundidad == 0 and not cierre and m.start() > ultimo:
            texto = fragmento[ultimo:m.start()]
            if texto.strip():
                salida.append(('texto', texto))

        if nombre in SUELTAS or sola:
            if profundidad == 0:
                salida.append(('el', fragmento[m.start():m.end()]))
                ultimo = m.end()
            continue

        if not cierre:
            if profundidad == 0:
                inicio = m.start()
            profundidad += 1
        else:
            profundidad -= 1
            if profundidad == 0 and inicio is not None:
                salida.append(('el', fragmento[inicio:m.end()]))
                inicio = None
                ultimo = m.end()

    if fragmento[ultimo:].strip() and profundidad == 0:
        salida.append(('texto', fragmento[ultimo:]))

    return salida


def abre(el):
    """La etiqueta de apertura: nombre y atributos."""
    m = re.match(r'<([a-zA-Z][a-zA-Z0-9]*)\b([^>]*?)/?>', el, re.S)
    nombre = m.group(1).lower()
    atributos = {}
    for a in ATRIBUTO.finditer(m.group(2)):
        atributos[a.group(1).lower()] = a.group(2) if a.group(2) is not None else ''
    return nombre, atributos, m.end()


def adentro(el, fin_apertura):
    cierre = el.rfind('</')
    return el[fin_apertura:cierre] if cierre >= fin_apertura else ''


class Conversor:
    def __init__(self):
        self.estilos = {}

    # ---------------------------------------------------------- estilos en línea

    def clase_de_estilo(self, estilo):
        estilo = '; '.join(d.strip() for d in estilo.split(';') if d.strip())
        if not estilo:
            return ''
        if estilo not in self.estilos:
            self.estilos[estilo] = 'en-' + hashlib.md5(estilo.encode()).hexdigest()[:6]
        return self.estilos[estilo]

    def hoja(self):
        filas = ['/* Generado por herramientas/bloques.py: los estilos que en el sitio',
                 '   iban en línea, convertidos en clases para que quepan en los bloques. */']
        for n in range(1, 6):
            filas.append('.reveal.retraso-%d { transition-delay: %gs; }' % (n, round(n * 0.08, 2)))
        for estilo, clase in sorted(self.estilos.items(), key=lambda x: x[1]):
            declaraciones = '; '.join(d.strip() + ' !important'
                                      for d in estilo.split(';') if d.strip())
            filas.append('.%s { %s; }' % (clase, declaraciones))
        return '\n'.join(filas) + '\n'

    # ---------------------------------------------------------------- bloques

    @staticmethod
    def html(el):
        return '<!-- wp:html -->\n%s\n<!-- /wp:html -->' % el.strip()

    def clases_y_ancla(self, atributos):
        """Las clases (con el estilo en línea ya convertido) y el id, o None si
        el elemento trae atributos que un bloque no sabe guardar."""
        extra = set(atributos) - {'class', 'id', 'style', 'data-delay', 'aria-label'}
        if extra:
            return None
        clases = atributos.get('class', '').split()
        # El escalonado de la animación de entrada pasa a una clase con el
        # mismo retraso que tenía en el sitio.
        if atributos.get('data-delay', '').isdigit():
            clases.append('retraso-' + atributos['data-delay'])
        if atributos.get('style'):
            clases.append(self.clase_de_estilo(atributos['style']))
        return ' '.join(c for c in clases if c), atributos.get('id')

    @staticmethod
    def comentario(nombre, datos):
        datos = {k: v for k, v in datos.items() if v not in (None, '', {})}
        return '<!-- wp:%s %s-->' % (nombre, json.dumps(datos, ensure_ascii=False) + ' ' if datos else '')

    def franja(self, atributos):
        escena = int(atributos.get('data-escena') or 0)
        clases = atributos.get('class', '')
        desde = 'agua' if 'franja--agua' in clases else 'crema'
        hasta = atributos.get('data-hasta') or ('crema' if desde == 'agua' else 'agua')
        return ('<!-- wp:dalila/franja {"escena":%d,"desde":"%s","hasta":"%s","align":"full"} /-->'
                % (escena, desde, hasta))

    def texto(self, nombre, atributos, contenido):
        """Título o párrafo con su contenido en línea."""
        if 'aria-label' in atributos:
            return None
        datos = self.clases_y_ancla(atributos)
        if datos is None:
            return None
        clases, ancla = datos

        if nombre == 'p':
            abre_p = '<p%s%s>' % (' class="%s"' % clases if clases else '',
                                  ' id="%s"' % ancla if ancla else '')
            return '%s\n%s%s</p>\n<!-- /wp:paragraph -->' % (
                self.comentario('paragraph', {'className': clases, 'anchor': ancla}),
                abre_p, contenido.strip())

        nivel = int(nombre[1])
        return '%s\n<%s class="wp-block-heading%s"%s>%s</%s>\n<!-- /wp:heading -->' % (
            self.comentario('heading', {'level': nivel, 'className': clases, 'anchor': ancla}),
            nombre, ' ' + clases if clases else '', ' id="%s"' % ancla if ancla else '',
            contenido.strip(), nombre)

    def imagen(self, atributos):
        """Una imagen suelta pasa al bloque «Imagen del sitio» (dalila/imagen),
        que guarda el mismo <img> y en el editor se cambia con «Reemplazar»."""
        propios = ('src', 'alt', 'width', 'height', 'loading', 'fetchpriority')
        if set(atributos) - set(propios) - {'class', 'style'} or not atributos.get('src'):
            return None
        clases = atributos.get('class', '').split()
        if atributos.get('style'):
            clases.append(self.clase_de_estilo(atributos['style']))
        clases = ' '.join(c for c in clases if c)

        # El mismo orden en que el bloque escribe sus atributos al guardar.
        partes = ['src="%s"' % atributos['src'], 'alt="%s"' % atributos.get('alt', '')]
        partes += ['%s="%s"' % (a, atributos[a]) for a in propios[2:] if a in atributos]
        if clases:
            partes.append('class="%s"' % clases)
        etiqueta_img = '<img ' + ' '.join(partes)
        etiqueta_img += '/>'
        return '%s\n%s\n<!-- /wp:dalila/imagen -->' % (
            self.comentario('dalila/imagen', {'className': clases}), etiqueta_img)

    def lista(self, nombre, atributos, contenido):
        # Con íconos, cada renglón va como «Texto del sitio», que los respeta.
        if 'aria-label' in atributos or SVG.search(contenido):
            return None
        datos = self.clases_y_ancla(atributos)
        if datos is None:
            return None
        clases, ancla = datos

        items = []
        for tipo, li in piezas(contenido):
            if tipo == 'texto':
                return None
            n, a, fin = abre(li)
            dentro = adentro(li, fin)
            datos_li = self.clases_y_ancla(a)
            if n != 'li' or datos_li is None or HAY_BLOQUE.search(dentro):
                return None
            cls_li, _ = datos_li
            items.append('%s\n<li%s>%s</li>\n<!-- /wp:list-item -->' % (
                self.comentario('list-item', {'className': cls_li}),
                ' class="%s"' % cls_li if cls_li else '', dentro.strip()))

        return '%s\n<%s class="wp-block-list%s"%s>\n%s\n</%s>\n<!-- /wp:list -->' % (
            self.comentario('list', {'ordered': True if nombre == 'ol' else None,
                                     'className': clases, 'anchor': ancla}),
            nombre, ' ' + clases if clases else '', ' id="%s"' % ancla if ancla else '',
            '\n'.join(items), nombre)

    def caja(self, nombre, atributos, contenido):
        datos = self.clases_y_ancla(atributos)
        if datos is None:
            return None
        hijos = piezas(contenido)
        if not hijos or any(t == 'texto' for t, _ in hijos):
            return None
        clases, ancla = datos

        dentro = '\n\n'.join(self.bloque(el) for _, el in hijos)
        etiqueta_aria = atributos.get('aria-label')
        datos_grupo = {'tagName': nombre if nombre != 'div' else None,
                       'anchor': ancla, 'ariaLabel': etiqueta_aria,
                       'className': clases, 'layout': {'type': 'default'}}
        return '%s\n<%s class="wp-block-group%s"%s%s>\n%s\n</%s>\n<!-- /wp:group -->' % (
            self.comentario('group', datos_grupo),
            nombre, ' ' + clases if clases else '', ' id="%s"' % ancla if ancla else '',
            ' aria-label="%s"' % etiqueta_aria if etiqueta_aria else '',
            dentro, nombre)

    def clases_y_resto(self, atributos):
        """Las clases (con estilo y retraso convertidos) y el resto de los
        atributos tal cual, en su orden, para los bloques del sitio."""
        clases = atributos.get('class', '').split()
        if atributos.get('data-delay', '').isdigit():
            clases.append('retraso-' + atributos['data-delay'])
        if atributos.get('style'):
            clases.append(self.clase_de_estilo(atributos['style']))
        resto = {k: html_lib.unescape(v) for k, v in atributos.items()
                 if k not in ('class', 'style', 'data-delay')}
        return ' '.join(c for c in clases if c), resto

    @staticmethod
    def abrir(nombre, resto, clases):
        partes = ['%s="%s"' % (k, escapar(v)) for k, v in resto.items()]
        if clases:
            partes.append('class="%s"' % clases)
        return '<%s%s>' % (nombre, ''.join(' ' + p for p in partes))

    def texto_sitio(self, nombre, atributos, contenido):
        """«Texto del sitio» (dalila/texto): una etiqueta con texto en línea,
        editable, con un ícono opcional al principio o al final."""
        if nombre in INTOCABLES or not solo_en_linea(contenido):
            return None
        if not texto_visible(contenido):
            return None

        icono, al_final = '', False
        if SVG.search(contenido):
            nodos = piezas(contenido)
            es_icono = lambda n: n[0] == 'el' and SVG.search(n[1]) and not texto_visible(n[1])
            if nodos and es_icono(nodos[0]):
                icono, resto_html = nodos[0][1].strip(), contenido.split(nodos[0][1], 1)[1]
            elif nodos and es_icono(nodos[-1]):
                icono, al_final = nodos[-1][1].strip(), True
                resto_html = contenido.rsplit(nodos[-1][1], 1)[0]
            else:
                return None
            if SVG.search(resto_html):
                return None
            texto = re.sub(r'\s+', ' ', resto_html)
            texto = texto.rstrip() if not al_final else texto.lstrip()
        else:
            texto = re.sub(r'\s+', ' ', contenido).strip()

        clases, resto = self.clases_y_resto(atributos)
        cuerpo = (texto + icono) if al_final else (icono + texto)
        datos = {'etiqueta': nombre, 'contenido': texto, 'atributos': resto,
                 'icono': icono, 'iconoAlFinal': True if al_final else None, 'className': clases}
        return '%s\n%s%s</%s>\n<!-- /wp:dalila/texto -->' % (
            self.comentario('dalila/texto', datos), self.abrir(nombre, resto, clases), cuerpo, nombre)

    def caja_sitio(self, nombre, atributos, contenido):
        """«Caja del sitio» (dalila/caja): cualquier contenedor con sus
        atributos, y adentro bloques."""
        if nombre in INTOCABLES:
            return None
        hijos = piezas(contenido)
        if not hijos or any(t == 'texto' for t, _ in hijos):
            return None
        # Solo dibujos, sin texto ni fotos (las estrellas, las burbujas): una pieza.
        if not texto_visible(contenido) and '<img' not in contenido:
            return None
        clases, resto = self.clases_y_resto(atributos)
        dentro = '\n\n'.join(self.bloque(el) for _, el in hijos)
        datos = {'etiqueta': nombre, 'atributos': resto, 'className': clases}
        return '%s\n%s\n%s\n</%s>\n<!-- /wp:dalila/caja -->' % (
            self.comentario('dalila/caja', datos), self.abrir(nombre, resto, clases), dentro, nombre)

    def bloque(self, el):
        el = el.strip()
        nombre, atributos, fin = abre(el)
        contenido = adentro(el, fin)

        if nombre == 'div' and 'franja' in atributos.get('class', '').split() and 'data-escena' in atributos:
            return self.franja(atributos)

        resultado = None
        if nombre == 'img':
            resultado = self.imagen(atributos)
        elif (nombre in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p') and not HAY_BLOQUE.search(contenido)
              and not SVG.search(contenido) and not HAY_INTOCABLE.search(contenido)):
            resultado = self.texto(nombre, atributos, contenido)
        elif nombre in ('ul', 'ol'):
            resultado = self.lista(nombre, atributos, contenido)
        elif nombre in CAJAS:
            resultado = self.caja(nombre, atributos, contenido)

        # Lo que no cabe en un bloque de WordPress va a los bloques del sitio.
        if resultado is None and nombre != 'img':
            resultado = self.texto_sitio(nombre, atributos, contenido)
        if resultado is None and nombre != 'img':
            resultado = self.caja_sitio(nombre, atributos, contenido)

        return resultado if resultado is not None else self.html(el)

    def convertir(self, fragmento):
        # Los comentarios del sitio («===== Hero =====») no son contenido.
        fragmento = re.sub(r'<!--(?!\s*/?wp:).*?-->', '', fragmento, flags=re.S)
        salida = []
        for tipo, el in piezas(fragmento):
            salida.append(self.html(el) if tipo == 'texto' else self.bloque(el))
        return '\n\n'.join(salida)
