# El sitio en WordPress

Esta carpeta es la versión WordPress del sitio de la Dra. Dalila Peñaranda, para
`dalilapenaranda.com` en Hostinger. El sitio estático de `docs/` sigue siendo la
referencia del diseño: el CSS y el JavaScript son literalmente los mismos
archivos, copiados aquí.

```
wordpress/
  themes/dalila/     el tema de bloques
  importacion/       el contenido listo para importar
  despliegue/        la guía de instalación
```

## Qué puede hacer el community manager

- **Escribir y editar artículos** del blog, con sus categorías e imagen destacada.
- **Armar páginas** con los quince patrones del tema. Se insertan desde el
  botón **+** → pestaña **Patrones** → *Secciones del sitio*:

  | Patrón | Para qué |
  |---|---|
  | Portada · Héroe | El bloque de entrada con la foto en polaroid |
  | Servicios | Las seis tarjetas con sus iconos |
  | Conoce a la doctora | El retrato con los tres pilares y la tarjeta de Pepe |
  | Nutrición y crecimiento | Las dos tarjetas grandes |
  | El consultorio, en la portada | Las postales con su pie de foto |
  | Cursos y talleres | Las tarjetas de curso con su botón de compra |
  | Convenios | Los logos de prepagadas y pólizas |
  | Tu cita | Las dos tarifas, presencial y virtual |
  | Testimonios | Las tarjetas con estrellas |
  | Preguntas frecuentes | El acordeón que además leen los buscadores |
  | Banda de contacto | La franja final con teléfono, correo y dirección |
  | Descarga de la guía | El regalo en PDF |
  | Sigue leyendo | Tres artículos relacionados |
  | Firma de la autora | El recuadro del pie de los artículos |
  | Cierre con llamado a la cita | La banda rosada del final |

  En nueve de ellos cada pieza repetida —una tarjeta, una pregunta, un logo— es
  un bloque suelto: para agregar una más se duplica y se escribe encima, sin
  tocar HTML.
- **Cambiar el menú y el pie** desde Apariencia → Editor.
- **Actualizar los datos del consultorio** —teléfono, correo, dirección,
  tarifas y enlaces de compra— en **Ajustes → Datos del consultorio**. Eso se
  refleja de una vez en toda la web, sin tocar página por página.

## Qué no debe tocar

El tema se despliega desde GitHub. Cualquier cambio hecho con el editor de
archivos de WordPress se pierde en el siguiente despliegue. Los textos, las
imágenes y las páginas sí viven en el servidor y no se tocan nunca desde aquí.

## La regla de esta mudanza

**No se cambia nada del diseño ni de los textos que ya existen.** WordPress es
solo un envase nuevo para lo mismo.

- El CSS y el JavaScript son los archivos de `docs/`, copiados sin editar.
- Los textos se importan tal cual: cada artículo conserva su propio cierre y sus
  propios tres artículos relacionados, que están escogidos a mano y son
  distintos en cada uno. La plantilla no impone ninguno.
- La plantilla solo aporta lo que sí es igual en los 25 artículos: la cabecera
  con título, entradilla y firma, y el recuadro de la autora al pie.

Lo único que no existía en el sitio estático es la **página de error 404**, que
WordPress necesita. Su texto se dejó al mínimo, a propósito, para que lo
escriba la doctora cuando quiera.
