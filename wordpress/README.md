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
