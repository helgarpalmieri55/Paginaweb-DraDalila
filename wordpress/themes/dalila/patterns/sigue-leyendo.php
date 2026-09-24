<?php
/**
 * Title: Sigue leyendo
 * Slug: dalila/sigue-leyendo
 * Categories: dalila-secciones
 * Description: Tres artículos relacionados, al cerrar una entrada del blog.
 * Inserter: yes
 */
?>
<!-- wp:group {"className":"seccion seccion--agua","layout":{"type":"constrained"}} -->
<div class="wp-block-group seccion seccion--agua">
	<!-- wp:heading {"className":"titulo"} -->
	<h2 class="wp-block-heading titulo">Sigue leyendo</h2>
	<!-- /wp:heading -->

	<!-- wp:paragraph {"className":"bajada"} -->
	<p class="bajada">Otros temas que suelen venir en la misma consulta.</p>
	<!-- /wp:paragraph -->

	<!-- wp:query {"queryId":2,"query":{"perPage":3,"postType":"post","order":"desc","orderBy":"date","exclude":[],"inherit":false},"layout":{"type":"default"}} -->
	<div class="wp-block-query">
		<!-- wp:post-template {"className":"rejilla rejilla--3 rejilla--piezas","layout":{"type":"grid","columnCount":3}} -->
			<!-- wp:post-featured-image {"isLink":true} /-->
			<!-- wp:group {"className":"articulo__cuerpo","layout":{"type":"default"}} -->
			<div class="wp-block-group articulo__cuerpo">
				<!-- wp:post-terms {"term":"category","className":"chip"} /-->
				<!-- wp:post-title {"level":3,"isLink":true} /-->
				<!-- wp:post-excerpt {"excerptLength":18,"showMoreOnNewLine":false,"moreText":"Leer más →"} /-->
			</div>
			<!-- /wp:group -->
		<!-- /wp:post-template -->
	</div>
	<!-- /wp:query -->
</div>
<!-- /wp:group -->
