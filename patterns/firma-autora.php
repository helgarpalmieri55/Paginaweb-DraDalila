<?php
/**
 * Title: Firma de la autora
 * Slug: dalila/firma-autora
 * Categories: dalila-piezas
 * Description: El recuadro con el retrato de la doctora al pie de cada artículo. El texto es el mismo del sitio.
 * Inserter: yes
 */
?>
<!-- wp:group {"className":"seccion seccion--agua","style":{"spacing":{"padding":{"top":"8px","bottom":"30px"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group seccion seccion--agua" style="padding-top:8px;padding-bottom:30px">

	<!-- wp:group {"tagName":"aside","className":"autora","layout":{"type":"default"}} -->
	<aside class="wp-block-group autora">

		<!-- wp:image {"width":"240px","height":"240px","className":"autora__foto"} -->
		<figure class="wp-block-image autora__foto"><img src="<?php echo esc_url( get_template_directory_uri() . '/assets/img/doctora-avatar.jpg' ); ?>" alt="Retrato de la Dra. Dalila Peñaranda" width="240" height="240"/></figure>
		<!-- /wp:image -->

		<!-- wp:group {"layout":{"type":"default"}} -->
		<div class="wp-block-group">
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
		<!-- /wp:group -->

	</aside>
	<!-- /wp:group -->

</div>
<!-- /wp:group -->
