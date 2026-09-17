# Portadas de los artículos

Ocho artículos hablan de temas sobre los que la doctora no tiene una pieza de
Instagram: lavado nasal, sangrado de nariz, espasmo del sollozo, ronquido, dolor
de oído, el inhalador, bullying y qué leche después de los dos años.

Para esos se ilustraron portadas propias, en
`docs/assets/img/posts/portada-<tema>.webp`, de 1000×1000.

## Cómo se hicieron

Con el modelo **Seedream 5 Pro** (Magnific), en 1:1. Se descargaron a 1536×1536,
se redujeron a 1000×1000 y se guardaron en WebP al 82 %. La de *espasmo del
sollozo* además se recortó al centro, porque salió con más aire que las demás.

Si hay que rehacer alguna, este es el bloque de estilo, que es lo que mantiene a
las ocho dentro de la misma familia. Va al principio y al final de cada prompt,
con el asunto en medio:

> Soft watercolour children's book illustration. **[asunto]**. Gentle pastel
> palette: dusty blue, soft navy, pale cream, coral pink, sage green. Loose
> watercolour brush texture with visible paper grain, soft edges, generous
> negative space, plain pale cream background. Tender and calm, not clinical.
> No text, no letters, no words, no logos, no borders, no frame.

## Los asuntos

| Portada | Asunto |
|---|---|
| `portada-lavado-nasal` | A small plastic saline syringe and a little bottle of saline solution resting on a folded soft towel, with a few tiny water droplets around them, still life on a plain surface |
| `portada-sangrado-nariz` | A young child sitting calmly on a chair and leaning slightly forward, gently pinching the soft part of their own nose with two fingers, holding a small white tissue in the other hand. Seen from the side |
| `portada-espasmo-sollozo` | A parent standing and gently rocking a crying baby held against their shoulder, one hand on the baby's back, full figures, plenty of empty space around them |
| `portada-ronquido` | A child sleeping in bed at night, seen from the side, head on a pillow, mouth slightly open, a light blanket. A window behind with a crescent moon and a few stars |
| `portada-dolor-de-oido` | A young child lying in bed at night holding a warm folded cloth against one ear, a small bedside lamp glowing softly, a window with a crescent moon behind |
| `portada-inhalador` | A child's asthma inhaler with a clear plastic spacer chamber and a small soft mask attached, resting on a plain surface, still life seen from slightly above |
| `portada-bullying` | A child sitting alone on school steps with a backpack beside them, head lowered, while a small group of other children plays far away in the soft blurred background |
| `portada-leche-dos-anios` | Two glasses of milk on a wooden table beside a small bowl of fruit, soft morning light, still life |

## Dónde se usan

No hay que tocarlas a mano en las páginas: cada artículo toma su imagen de un
mapa único, así que la tarjeta del blog, las tarjetas de «sigue leyendo», la
figura dentro del artículo y la imagen para compartir muestran siempre la misma.
