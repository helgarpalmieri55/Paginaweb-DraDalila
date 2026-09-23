<?php
/**
 * Title: Cursos y talleres
 * Slug: dalila/cursos
 * Categories: dalila-secciones
 * Description: Las tarjetas de los cursos, con el botón que lleva a Hotmart o a WhatsApp.
 * Inserter: yes
 */
?>
<!-- wp:group {"className": "seccion seccion--crema", "layout": {"type": "default"}, "tagName": "section", "anchor": "cursos", "align": "full"} -->
<section class="wp-block-group alignfull seccion seccion--crema" id="cursos">
<!-- wp:group {"className": "wrap", "layout": {"type": "default"}} -->
<div class="wp-block-group wrap">
<!-- wp:heading {"level": 2, "className": "titulo"} -->
<h2 class="wp-block-heading titulo">Cursos y talleres</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {"className": "bajada"} -->
<p class="bajada">Un curso en video, dos talleres en grupo y la escuela para padres.</p>
<!-- /wp:paragraph -->

<!-- wp:group {"className": "rejilla rejilla--3", "layout": {"type": "default"}} -->
<div class="wp-block-group rejilla rejilla--3">
<!-- wp:html -->
<article class="curso"><img src="<?php echo esc_url( get_template_directory_uri() . '/assets/img/curso-complementaria.jpg' ); ?>" alt="Bebé comiendo con cuchara en su silla" width="800" height="1199" loading="lazy"><div class="curso__cuerpo"><strong>Curso de alimentación complementaria</strong><p>De la leche a la cuchara: la silla, las texturas y los alérgenos, paso a paso.</p><div class="curso__pie"><span class="curso__precio">$149.000</span><a href="/cursos/">Ver el curso →</a></div></div></article>
<!-- /wp:html -->

<!-- wp:html -->
<article class="curso"><img src="<?php echo esc_url( get_template_directory_uri() . '/assets/img/curso-lonchera.jpg' ); ?>" alt="Comida saludable lista en porciones" width="800" height="533" loading="lazy"><div class="curso__cuerpo"><strong>Taller de lonchera saludable</strong><p>Qué poner para que aguante la mañana y vuelva vacía.</p><div class="curso__pie"><span class="curso__precio">$119.000</span><a href="/cursos/">Ver el curso →</a></div></div></article>
<!-- /wp:html -->

<!-- wp:html -->
<article class="curso"><img src="<?php echo esc_url( get_template_directory_uri() . '/assets/img/curso-dormir.jpg' ); ?>" alt="Bebé durmiendo tranquilo" width="800" height="534" loading="lazy"><div class="curso__cuerpo"><strong>Escuela para padres</strong><p>Encuentros presenciales: un cuento, las emociones que destapa y una conversación.</p><div class="curso__pie"><span class="curso__precio" style="font-size:16px;color:var(--suave)">Encuentros presenciales</span><a href="/cursos/">Ver el curso →</a></div></div></article>
<!-- /wp:html -->
</div>
<!-- /wp:group -->
</div>
<!-- /wp:group -->
</section>
<!-- /wp:group -->
