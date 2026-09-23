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
- **Armar páginas** con los patrones del tema: héroe, servicios, convenios,
  cursos, citas, preguntas frecuentes, franja de mar. Se insertan desde el
  botón **+** → pestaña **Patrones** → *Secciones del sitio*.
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
