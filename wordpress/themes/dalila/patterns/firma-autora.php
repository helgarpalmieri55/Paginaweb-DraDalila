<?php
/**
 * Title: Firma de la autora
 * Slug: dalila/firma-autora
 * Categories: dalila-piezas
 * Description: El recuadro con el retrato de la doctora, su credencial y los enlaces, al pie de cada artículo.
 * Inserter: yes
 */
?>
<!-- wp:group {"className":"seccion seccion--agua","style":{"spacing":{"padding":{"top":"8px","bottom":"30px"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group seccion seccion--agua" style="padding-top:8px;padding-bottom:30px">
	<!-- wp:media-text {"mediaId":0,"mediaType":"image","mediaWidth":20,"className":"autora","verticalAlignment":"center"} -->
	<div class="wp-block-media-text is-stacked-on-mobile is-vertically-aligned-center autora" style="grid-template-columns:20% auto">
		<figure class="wp-block-media-text__media">
			<img src="<?php echo esc_url( get_template_directory_uri() . '/assets/img/doctora-avatar.jpg' ); ?>" alt="Retrato de la Dra. Dalila Peñaranda" class="autora__foto"/>
		</figure>
		<div class="wp-block-media-text__content">
			<!-- wp:paragraph -->
			<p><strong>Dra. Dalila Peñaranda</strong></p>
			<!-- /wp:paragraph -->
			<!-- wp:paragraph -->
			<p>Pediatra y especialista en nutrición infantil. Atiende en el High Park Medical Center de Barranquilla y por videollamada a familias dentro y fuera de Colombia.</p>
			<!-- /wp:paragraph -->
			<!-- wp:paragraph {"className":"autora__enlaces"} -->
			<p class="autora__enlaces"><a href="/sobre-mi/">Conoce a la doctora</a> <a href="/citas/">Agenda una consulta</a> <a data-red="instagram" href="https://www.instagram.com/dra.dalilapenaranda/" target="_blank" rel="noopener">Sígueme en Instagram</a></p>
			<!-- /wp:paragraph -->
		</div>
	</div>
	<!-- /wp:media-text -->
</div>
<!-- /wp:group -->
