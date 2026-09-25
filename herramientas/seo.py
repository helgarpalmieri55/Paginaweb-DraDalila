#!/usr/bin/env python3
"""
Genera los metadatos de posicionamiento del sitio de la Dra. Dalila Peñaranda.

Escribe, en cada página de docs/, un bloque delimitado por <!-- SEO --> … <!-- /SEO -->
con la canónica, las etiquetas sociales y los datos estructurados JSON-LD. Fuera de
ese bloque no toca nada: el título y la descripción de cada página se escriben a mano
y este script solo los lee.

También genera docs/sitemap.xml, docs/robots.txt y docs/llms.txt.

Se puede volver a ejecutar cuantas veces haga falta:

    python3 herramientas/seo.py

El día que el sitio tenga dominio propio, se cambia BASE y se vuelve a ejecutar.
"""

import html
import json
import os
import re
import subprocess
import sys
from datetime import date

# ---------------------------------------------------------------- configuración

BASE = 'https://helgarpalmieri55.github.io/Paginaweb-DraDalila/'

MARCA      = 'Dra. Dalila Peñaranda'
NOMBRE     = 'Dra. Dalila Peñaranda — Pediatría y Nutrición Infantil'
TELEFONO   = '+573046532006'
CORREO     = 'nutripedcm@gmail.com'
CALLE      = 'Calle 1C # 30-40, High Park Medical Center, consultorio 129'
CIUDAD     = 'Barranquilla'
REGION     = 'Atlántico'
PAIS       = 'CO'
INSTAGRAM  = 'https://www.instagram.com/dra.dalilapenaranda/'

# Servicios tal como aparecen en servicios.html.
SERVICIOS = [
    ('Control pediátrico',        'Revisión completa del crecimiento, el desarrollo, la alimentación y el esquema de vacunación, desde recién nacido hasta la adolescencia.'),
    ('Nutrición infantil',        'Valoración nutricional con antropometría y plan de alimentación ajustado a la edad, los hábitos y la realidad de cada casa.'),
    ('Crecimiento y desarrollo',  'Seguimiento de talla, peso y perímetro cefálico sobre las curvas de la OMS, y de los hitos del desarrollo.'),
    ('Alimentación complementaria','Acompañamiento en el inicio de sólidos: texturas, cantidades, señales de alarma y manejo de la selectividad.'),
    ('Asesoría a padres',         'Lactancia, sueño, pataletas y dudas de crianza resueltas con tiempo y sin apuro.'),
    ('Consulta virtual',          'Videollamada para familias dentro y fuera de Colombia, con el plan enviado por correo.'),
]

TEMAS = [
    'Pediatría', 'Nutrición infantil', 'Lactancia materna',
    'Alimentación complementaria', 'Crecimiento y desarrollo infantil',
    'Puericultura', 'Selectividad alimentaria',
]

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')

# Páginas que no queremos en el sitemap ni ofrecidas a los buscadores como destino.
BAJA_PRIORIDAD = {'aviso-medico.html', 'privacidad.html'}

# Nombre corto de cada página para las migas de pan.
MIGAS = {
    'sobre-mi.html':    'Sobre mí',
    'servicios.html':   'Servicios',
    'consultorio.html': 'El consultorio',
    'cursos.html':      'Cursos',
    'blog.html':        'Blog',
    'citas.html':       'Citas y tarifas',
    'contacto.html':    'Contacto',
    'aviso-medico.html':'Aviso médico',
    'privacidad.html':  'Política de privacidad',
}

INICIO, FIN = '<!-- SEO -->', '<!-- /SEO -->'

# Tarjeta para compartir en redes y en WhatsApp: 1200x630, generada con
# herramientas/tarjeta-social.mjs a partir de docs/_og.html.
IMAGEN_SOCIAL = 'assets/img/og-portada.jpg'
IMAGENES_GENERICAS = {'assets/img/doctora-pepe.jpg', 'assets/img/logo.webp'}

# ------------------------------------------------------------------ utilidades

def texto(fragmento):
    """Deja solo el texto legible de un trozo de HTML."""
    fragmento = re.sub(r'<svg.*?</svg>', ' ', fragmento, flags=re.S)
    fragmento = re.sub(r'<br\s*/?>', ' ', fragmento)
    fragmento = re.sub(r'<[^>]+>', ' ', fragmento)
    return re.sub(r'\s+', ' ', html.unescape(fragmento)).strip()


def etiqueta(fuente, patron, grupo=1):
    m = re.search(patron, fuente, re.S)
    return m.group(grupo) if m else None


def _git(*args):
    try:
        return subprocess.run(['git'] + list(args), capture_output=True, text=True,
                              cwd=os.path.dirname(DOCS)).stdout.strip()
    except Exception:
        return ''


def fecha_publicacion(ruta):
    """El día que la página entró al repositorio."""
    return _git('log', '--diff-filter=A', '--format=%ad', '--date=short', '-1', '--', ruta) \
        or date.today().isoformat()


def fecha_git(ruta, relativa=None):
    """Fecha del último commit que tocó el archivo; hoy si está sin confirmar."""
    hoy = date.today().isoformat()
    if _git('status', '--porcelain', '--', ruta):
        return hoy
    return _git('log', '-1', '--format=%ad', '--date=short', '--', ruta) or hoy


def medidas(relativa):
    """Ancho y alto reales de una imagen del sitio."""
    try:
        from PIL import Image
        with Image.open(os.path.join(DOCS, relativa)) as im:
            return im.size
    except Exception:
        return None


def jsonld(*nodos):
    grafo = {'@context': 'https://schema.org', '@graph': [n for n in nodos if n]}
    cuerpo = json.dumps(grafo, ensure_ascii=False, indent=2)
    return '<script type="application/ld+json">\n' + cuerpo + '\n</script>'

# --------------------------------------------------------------- nodos comunes

ID_PRACTICA = BASE + '#consultorio'
ID_DOCTORA  = BASE + '#dalila'
ID_SITIO    = BASE + '#sitio'


def nodo_practica():
    """La consulta como negocio local. Sin horarios ni reseñas: aún no están confirmados."""
    return {
        '@type': ['Physician', 'MedicalBusiness'],
        '@id': ID_PRACTICA,
        'name': NOMBRE,
        'alternateName': MARCA,
        'description': ('Consulta de pediatría y nutrición infantil en Barranquilla, '
                        'con atención presencial y virtual desde recién nacidos hasta la adolescencia.'),
        'url': BASE,
        'image': BASE + 'assets/img/consultorio-ballena.webp',
        'logo': BASE + 'assets/img/logo.webp',
        'telephone': TELEFONO,
        'email': CORREO,
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': CALLE,
            'addressLocality': CIUDAD,
            'addressRegion': REGION,
            'addressCountry': PAIS,
        },
        'medicalSpecialty': ['Pediatric', 'DietNutrition'],
        'areaServed': [
            {'@type': 'City', 'name': 'Barranquilla'},
            {'@type': 'AdministrativeArea', 'name': 'Atlántico, Colombia'},
        ],
        'availableService': [
            {'@type': 'MedicalProcedure', 'name': n, 'description': d}
            for n, d in SERVICIOS
        ],
        'physician': {'@id': ID_DOCTORA},
        'employee': {'@id': ID_DOCTORA},
        'sameAs': [INSTAGRAM],
        'knowsLanguage': 'es',
        'isAcceptingNewPatients': True,
        'currenciesAccepted': 'COP, USD',
    }


def nodo_doctora():
    """La doctora, con los títulos que constan en sus diplomas y certificados."""
    return {
        '@type': 'Person',
        '@id': ID_DOCTORA,
        'name': 'Dalila Peñaranda',
        'honorificPrefix': 'Dra.',
        'jobTitle': 'Pediatra y especialista en nutrición infantil',
        'description': ('Pediatra de la Universidad Libre con posgrado en nutrición pediátrica '
                        '(PGPN, Boston University School of Medicine) y formación como terapista de '
                        'alimentación (SOS Approach to Feeding). Atiende en Barranquilla y por '
                        'videollamada a familias dentro y fuera de Colombia.'),
        'url': BASE + 'sobre-mi.html',
        'image': BASE + 'assets/img/doctora-retrato-estudio.webp',
        'worksFor': {'@id': ID_PRACTICA},
        'alumniOf': [
            {'@type': 'CollegeOrUniversity', 'name': 'Fundación Universitaria San Martín'},
            {'@type': 'CollegeOrUniversity', 'name': 'Universidad Libre'},
        ],
        'hasCredential': CREDENCIALES,
        'knowsAbout': TEMAS,
        'knowsLanguage': 'es',
        'sameAs': [INSTAGRAM],
    }


# Sus títulos y certificaciones, tal como constan en los documentos.
CREDENCIALES = [
    {'@type': 'EducationalOccupationalCredential', 'credentialCategory': 'degree',
     'name': 'Médico general', 'dateCreated': '2004-12-14',
     'recognizedBy': {'@type': 'CollegeOrUniversity', 'name': 'Fundación Universitaria San Martín'}},
    {'@type': 'EducationalOccupationalCredential', 'credentialCategory': 'degree',
     'name': 'Especialista en Pediatría', 'dateCreated': '2011-08-26',
     'recognizedBy': {'@type': 'CollegeOrUniversity', 'name': 'Universidad Libre'}},
    {'@type': 'EducationalOccupationalCredential', 'credentialCategory': 'certificate',
     'name': 'Post Graduate Program in Pediatric Nutrition (PGPN)', 'dateCreated': '2016',
     'recognizedBy': {'@type': 'CollegeOrUniversity', 'name': 'Boston University School of Medicine'}},
    {'@type': 'EducationalOccupationalCredential', 'credentialCategory': 'certificate',
     'name': 'SOS Trained Feeding Therapist', 'dateCreated': '2024-11-12',
     'recognizedBy': {'@type': 'Organization', 'name': 'SOS Approach to Feeding'}},
]


def nodo_sitio():
    return {
        '@type': 'WebSite',
        '@id': ID_SITIO,
        'url': BASE,
        'name': MARCA,
        'inLanguage': 'es-CO',
        'publisher': {'@id': ID_PRACTICA},
    }


def nodo_migas(ruta, titulo_corto, articulo=None):
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': BASE}]
    if articulo:
        items.append({'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': BASE + 'blog.html'})
        items.append({'@type': 'ListItem', 'position': 3, 'name': articulo})
    else:
        items.append({'@type': 'ListItem', 'position': 2, 'name': titulo_corto})
    return {'@type': 'BreadcrumbList', '@id': BASE + ruta + '#migas', 'itemListElement': items}


def nodo_faq(fuente, ruta):
    """Convierte los <details> de la página en preguntas frecuentes indexables."""
    pares = []
    for bloque in re.findall(r'<details[^>]*>(.*?)</details>', fuente, re.S):
        p = etiqueta(bloque, r'<summary[^>]*>(.*?)</summary>')
        if not p:
            continue
        r = texto(re.sub(r'<summary.*?</summary>', '', bloque, flags=re.S))
        p = texto(p)
        # Nada que siga marcado como pendiente entra en los datos estructurados.
        if not r or 'pendiente de confirmar' in r.lower():
            continue
        pares.append({'@type': 'Question', 'name': p,
                      'acceptedAnswer': {'@type': 'Answer', 'text': r}})
    if not pares:
        return None
    return {'@type': 'FAQPage', '@id': BASE + ruta + '#faq', 'mainEntity': pares}


# ------------------------------------------------------------ bloque por página

def bloque(ruta, fuente, fecha, publicada):
    """Arma el bloque SEO completo de una página."""
    titulo = html.unescape(etiqueta(fuente, r'<title>(.*?)</title>') or MARCA)
    descripcion = html.unescape(etiqueta(fuente, r'<meta name="description" content="(.*?)">') or '')
    imagen = etiqueta(fuente, r'<meta property="og:image" content="(.*?)">') or IMAGEN_SOCIAL
    # Al volver a ejecutar el script la etiqueta ya viene absoluta: la dejamos relativa.
    if imagen.startswith(BASE):
        imagen = imagen[len(BASE):]
    # Las páginas sin una imagen propia comparten la tarjeta de portada, que está
    # compuesta a 1200x630 y se ve entera al compartirla por WhatsApp.
    if imagen in IMAGENES_GENERICAS:
        imagen = IMAGEN_SOCIAL
    url = BASE if ruta == 'index.html' else BASE + ruta
    articulo = ruta.startswith('blog-')
    h1 = texto(etiqueta(fuente, r'<h1[^>]*>(.*?)</h1>') or titulo)

    # El texto alternativo de la imagen social se toma del propio sitio.
    alt = etiqueta(fuente, r'<img[^>]+src="' + re.escape(imagen) + r'"[^>]*alt="([^"]*)"') or h1

    lineas = [
        INICIO,
        '<link rel="canonical" href="%s">' % url,
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        '<meta property="og:type" content="%s">' % ('article' if articulo else 'website'),
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:site_name" content="%s">' % MARCA,
        '<meta property="og:locale" content="es_CO">',
        '<meta property="og:title" content="%s">' % html.escape(titulo, quote=True),
        '<meta property="og:description" content="%s">' % html.escape(descripcion, quote=True),
        '<meta property="og:image" content="%s">' % (BASE + imagen),
        '<meta property="og:image:alt" content="%s">' % html.escape(alt, quote=True),
    ]
    tam = medidas(imagen)
    if tam:
        lineas.insert(-1, '<meta property="og:image:width" content="%d">' % tam[0])
        lineas.insert(-1, '<meta property="og:image:height" content="%d">' % tam[1])

    if articulo:
        lineas += [
            '<meta property="article:published_time" content="%s">' % publicada,
            '<meta property="article:modified_time" content="%s">' % fecha,
            '<meta property="article:author" content="Dra. Dalila Peñaranda">',
        ]

    lineas += [
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % html.escape(titulo, quote=True),
        '<meta name="twitter:description" content="%s">' % html.escape(descripcion, quote=True),
        '<meta name="twitter:image" content="%s">' % (BASE + imagen),
        '<meta name="author" content="Dra. Dalila Peñaranda">',
        '<meta name="geo.region" content="CO-ATL">',
        '<meta name="geo.placename" content="Barranquilla">',
    ]

    # ------ datos estructurados
    nodos = [nodo_sitio(), nodo_practica(), nodo_doctora()]

    if ruta == 'index.html':
        nodos.append({
            '@type': 'WebPage', '@id': url + '#pagina', 'url': url,
            'name': titulo, 'description': descripcion,
            'isPartOf': {'@id': ID_SITIO}, 'about': {'@id': ID_PRACTICA},
            'inLanguage': 'es-CO', 'primaryImageOfPage': BASE + imagen,
        })
    elif articulo:
        nodos.append(nodo_migas(ruta, '', articulo=h1))
        nodos.append({
            '@type': 'BlogPosting', '@id': url + '#articulo',
            'headline': h1[:110], 'name': h1,
            'description': descripcion, 'url': url,
            'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
            'image': BASE + imagen,
            'datePublished': publicada, 'dateModified': fecha,
            'author': {'@id': ID_DOCTORA},
            'publisher': {'@id': ID_PRACTICA},
            'inLanguage': 'es-CO',
            'isPartOf': {'@type': 'Blog', '@id': BASE + 'blog.html#blog',
                         'name': 'Blog de la Dra. Dalila Peñaranda'},
        })
    else:
        nodos.append(nodo_migas(ruta, MIGAS.get(ruta, titulo.split('·')[0].strip())))
        nodos.append({
            '@type': 'WebPage', '@id': url + '#pagina', 'url': url,
            'name': titulo, 'description': descripcion,
            'isPartOf': {'@id': ID_SITIO}, 'about': {'@id': ID_PRACTICA},
            'inLanguage': 'es-CO', 'primaryImageOfPage': BASE + imagen,
            'breadcrumb': {'@id': BASE + ruta + '#migas'},
        })

    faq = nodo_faq(fuente, ruta)
    if faq:
        nodos.append(faq)

    lineas.append(jsonld(*nodos))
    lineas.append(FIN)
    return '\n'.join(lineas)


# Etiquetas que ahora administra este script y que hay que quitar de donde estaban.
SUELTAS = re.compile(
    r'^[ \t]*<(?:link rel="canonical"[^>]*|meta (?:property="og:[^"]*"|name="(?:twitter:[^"]*|robots|author|geo\.[^"]*)")[^>]*)>[ \t]*\n',
    re.M)


def escribir_paginas():
    tocadas = []
    for archivo in sorted(os.listdir(DOCS)):
        if not archivo.endswith('.html'):
            continue
        ruta = os.path.join(DOCS, archivo)
        fuente = open(ruta, encoding='utf-8').read()
        fecha = fecha_git(ruta)
        publicada = fecha_publicacion(ruta)

        # Fuera el bloque anterior y las etiquetas sueltas que quedaron de antes.
        limpio = re.sub(re.escape(INICIO) + r'.*?' + re.escape(FIN) + r'\n?', '', fuente, flags=re.S)
        limpio = SUELTAS.sub('', limpio)

        nuevo = bloque(archivo, fuente, fecha, publicada)
        ancla = re.search(r'^[ \t]*<meta name="description"[^>]*>[ \t]*\n', limpio, re.M)
        if not ancla:
            raise SystemExit('%s no tiene <meta name="description">' % archivo)
        salida = limpio[:ancla.end()] + nuevo + '\n' + limpio[ancla.end():]

        if salida != fuente:
            open(ruta, 'w', encoding='utf-8').write(salida)
            tocadas.append(archivo)
    return tocadas


# ------------------------------------------------------- sitemap, robots, llms

def escribir_sitemap():
    filas = []
    for archivo in sorted(os.listdir(DOCS)):
        if not archivo.endswith('.html'):
            continue
        url = BASE if archivo == 'index.html' else BASE + archivo
        fecha = fecha_git(os.path.join(DOCS, archivo))
        if archivo == 'index.html':
            prioridad, frecuencia = '1.0', 'weekly'
        elif archivo in BAJA_PRIORIDAD:
            prioridad, frecuencia = '0.3', 'yearly'
        elif archivo.startswith('blog-'):
            prioridad, frecuencia = '0.7', 'monthly'
        else:
            prioridad, frecuencia = '0.9', 'monthly'
        filas.append('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n'
                     '    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>'
                     % (url, fecha, frecuencia, prioridad))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + '\n'.join(filas) + '\n</urlset>\n')
    open(os.path.join(DOCS, 'sitemap.xml'), 'w', encoding='utf-8').write(xml)
    return len(filas)


def escribir_robots():
    txt = ('# Sitio informativo de la Dra. Dalila Peñaranda\n'
           '# Pediatría y nutrición infantil · Barranquilla, Colombia\n\n'
           'User-agent: *\n'
           'Allow: /\n\n'
           'Sitemap: %ssitemap.xml\n' % BASE)
    open(os.path.join(DOCS, 'robots.txt'), 'w', encoding='utf-8').write(txt)


def escribir_llms():
    """Resumen en texto plano para los motores de respuesta generativos."""
    articulos = []
    for archivo in sorted(os.listdir(DOCS)):
        if not archivo.startswith('blog-') or not archivo.endswith('.html'):
            continue
        fuente = open(os.path.join(DOCS, archivo), encoding='utf-8').read()
        titulo = texto(etiqueta(fuente, r'<h1[^>]*>(.*?)</h1>') or archivo)
        desc = html.unescape(etiqueta(fuente, r'<meta name="description" content="(.*?)">') or '')
        articulos.append('- [%s](%s%s): %s' % (titulo, BASE, archivo, desc))

    paginas = [('Sobre la doctora', 'sobre-mi.html'), ('Servicios', 'servicios.html'),
               ('El consultorio', 'consultorio.html'), ('Citas y tarifas', 'citas.html'),
               ('Cursos y talleres', 'cursos.html'), ('Blog', 'blog.html'),
               ('Contacto', 'contacto.html')]

    txt = """# Dra. Dalila Peñaranda — Pediatría y Nutrición Infantil

> Pediatra con subespecialidad en nutrición infantil en Barranquilla, Colombia.
> Atiende de forma presencial en el consultorio y por videollamada a familias
> dentro y fuera del país, desde recién nacidos hasta la adolescencia.

## Datos de contacto

- Consultorio: {calle}, {ciudad}, {region}, Colombia
- WhatsApp: {tel}
- Correo: {correo}
- Instagram: {ig}
- Sitio: {base}

## Qué atiende

{servicios}

## Páginas

{paginas}

## Artículos del blog

{articulos}

## Nota

Todo el contenido de este sitio es información general de educación en salud
y no reemplaza una consulta médica. Ante una urgencia hay que acudir al
servicio de salud más cercano.
""".format(
        calle=CALLE, ciudad=CIUDAD, region=REGION, tel='+57 304 653 2006',
        correo=CORREO, ig=INSTAGRAM, base=BASE,
        servicios='\n'.join('- **%s**: %s' % (n, d) for n, d in SERVICIOS),
        paginas='\n'.join('- [%s](%s%s)' % (n, BASE, r) for n, r in paginas),
        articulos='\n'.join(articulos))
    open(os.path.join(DOCS, 'llms.txt'), 'w', encoding='utf-8').write(txt)
    return len(articulos)


if __name__ == '__main__':
    tocadas = escribir_paginas()
    urls = escribir_sitemap()
    escribir_robots()
    arts = escribir_llms()
    print('páginas actualizadas: %d' % len(tocadas))
    print('sitemap.xml: %d URLs' % urls)
    print('robots.txt: escrito')
    print('llms.txt: %d artículos' % arts)
