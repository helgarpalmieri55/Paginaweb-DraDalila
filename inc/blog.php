<?php
/**
 * El blog: el artículo destacado, los filtros por categoría y la rejilla de
 * tarjetas, con el mismo marcado del sitio para que se vea idéntico y para
 * que el filtro de site.js funcione sin cambios.
 *
 * Se usan desde la plantilla del blog con [dalila_destacado],
 * [dalila_filtros] y [dalila_articulos].
 *
 * @package dalila
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * El color del distintivo de cada categoría, el mismo del sitio.
 */
function dalila_color_de_categoria( $slug ) {
	$colores = array(
		'nutricion'   => 'verde',
		'lactancia'   => 'rosa',
		'salud'       => 'rosa',
		'crecimiento' => 'azul',
	);

	return isset( $colores[ $slug ] ) ? $colores[ $slug ] : 'rosa';
}

/**
 * La categoría que se muestra en la tarjeta: la primera que no sea la de
 * «Sin categoría».
 */
function dalila_categoria_de( $post_id ) {
	foreach ( get_the_category( $post_id ) as $categoria ) {
		if ( (int) get_option( 'default_category' ) !== $categoria->term_id || 1 === count( get_the_category( $post_id ) ) ) {
			return $categoria;
		}
	}

	return null;
}

/**
 * El texto corto de la tarjeta. Si la entrada no tiene uno propio en el campo
 * «dalila_tarjeta», se usa su extracto.
 */
function dalila_texto_de_tarjeta( $post_id ) {
	$texto = get_post_meta( $post_id, 'dalila_tarjeta', true );

	return $texto ? $texto : wp_strip_all_tags( get_the_excerpt( $post_id ) );
}

/**
 * El artículo destacado: el que esté fijado arriba (Entradas → Editar →
 * «Fijar en la parte superior del blog»). Si no hay ninguno, el más reciente.
 */
function dalila_id_destacado() {
	static $id = null;

	if ( null === $id ) {
		$fijos = array_filter( array_map( 'intval', (array) get_option( 'sticky_posts', array() ) ) );
		$ids   = get_posts(
			array(
				'post_type'           => 'post',
				'post_status'         => 'publish',
				'posts_per_page'      => 1,
				'post__in'            => $fijos ? $fijos : null,
				'ignore_sticky_posts' => true,
				'fields'              => 'ids',
			)
		);
		$id = $ids ? (int) $ids[0] : 0;
	}

	return $id;
}

/**
 * La portada de la entrada con las medidas reales, para que no salte al cargar.
 */
function dalila_portada( $post_id, $clase = '' ) {
	$imagen_id = get_post_thumbnail_id( $post_id );
	if ( ! $imagen_id ) {
		return '';
	}

	$imagen = wp_get_attachment_image_src( $imagen_id, 'large' );
	if ( ! $imagen ) {
		return '';
	}

	$alt = get_post_meta( $imagen_id, '_wp_attachment_image_alt', true );

	return sprintf(
		'<img%s src="%s" alt="%s" width="%d" height="%d" loading="lazy">',
		$clase ? ' class="' . esc_attr( $clase ) . '"' : '',
		esc_url( $imagen[0] ),
		esc_attr( $alt ? $alt : get_the_title( $post_id ) ),
		(int) $imagen[1],
		(int) $imagen[2]
	);
}

/**
 * [dalila_destacado] → el artículo grande de arriba del blog.
 */
function dalila_atajo_destacado() {
	if ( ! is_home() || is_paged() ) {
		return '';
	}

	$id = dalila_id_destacado();
	if ( ! $id ) {
		return '';
	}

	$categoria = dalila_categoria_de( $id );
	$chip      = $categoria ? sprintf(
		'<span class="chip chip--%s">%s</span>',
		esc_attr( dalila_color_de_categoria( $categoria->slug ) ),
		esc_html( mb_strtolower( $categoria->name ) )
	) : '';

	return sprintf(
		'<article class="destacado reveal">%1$s<div class="destacado__cuerpo">%2$s<h2>%3$s</h2><p>%4$s</p><p class="articulo__fecha">%5$s</p><p style="margin-top:20px"><a class="btn btn--rosa btn--chico" href="%6$s">%7$s</a></p></div></article>',
		dalila_portada( $id, 'pieza' ),
		$chip,
		esc_html( get_the_title( $id ) ),
		esc_html( dalila_texto_de_tarjeta( $id ) ),
		esc_html( sprintf( __( '%d min de lectura', 'dalila' ), dalila_minutos_de_lectura( $id ) ) ),
		esc_url( get_permalink( $id ) ),
		esc_html__( 'Leer el artículo →', 'dalila' )
	);
}
add_shortcode( 'dalila_destacado', 'dalila_atajo_destacado' );

/**
 * [dalila_filtros] → los botones «Todo · Nutrición · Lactancia…».
 * Solo aparecen las categorías que tienen artículos.
 */
function dalila_atajo_filtros() {
	if ( ! is_home() ) {
		return '';
	}

	$categorias = get_terms(
		array(
			'taxonomy'   => 'category',
			'hide_empty' => true,
			'orderby'    => 'term_id',
			'exclude'    => array( (int) get_option( 'default_category' ) ),
		)
	);
	if ( is_wp_error( $categorias ) || count( $categorias ) < 2 ) {
		return '';
	}

	$botones = '<button class="filtro" type="button" data-cat="todo" aria-pressed="true">' . esc_html__( 'Todo', 'dalila' ) . '</button>';
	foreach ( $categorias as $categoria ) {
		$botones .= sprintf(
			'<button class="filtro" type="button" data-cat="%s" aria-pressed="false">%s</button>',
			esc_attr( $categoria->slug ),
			esc_html( $categoria->name )
		);
	}

	return '<div class="filtros reveal" role="group" aria-label="' . esc_attr__( 'Filtrar por categoría', 'dalila' ) . '">' . $botones . '</div>';
}
add_shortcode( 'dalila_filtros', 'dalila_atajo_filtros' );

/**
 * [dalila_articulos] → la rejilla de tarjetas. En el blog van todas menos la
 * destacada, para que el filtro las alcance a todas; en una categoría, una
 * etiqueta o una búsqueda, las de esa consulta.
 */
function dalila_atajo_articulos() {
	$argumentos = array(
		'post_type'           => 'post',
		'post_status'         => 'publish',
		'posts_per_page'      => -1,
		'ignore_sticky_posts' => true,
		'no_found_rows'       => true,
	);

	if ( is_home() ) {
		$argumentos['post__not_in'] = array( dalila_id_destacado() );
	} elseif ( is_category() || is_tag() ) {
		$argumentos['tax_query'] = array(
			array(
				'taxonomy' => get_queried_object()->taxonomy,
				'terms'    => get_queried_object_id(),
			),
		);
	} elseif ( is_search() ) {
		$argumentos['s'] = get_search_query();
	}

	$entradas = get_posts( $argumentos );
	if ( ! $entradas ) {
		return '<div class="sin-resultados reveal"><strong>' . esc_html__( 'Todavía no hay artículos en esta categoría', 'dalila' ) . '</strong><p>' . esc_html__( 'Escríbeme el tema que te gustaría leer y lo pongo en la lista.', 'dalila' ) . '</p></div>';
	}

	$tarjetas = '';
	foreach ( $entradas as $i => $entrada ) {
		$categoria = dalila_categoria_de( $entrada->ID );
		$retraso   = $i % 3;

		$tarjetas .= sprintf(
			'<article class="articulo reveal"%1$s%2$s>%3$s<div class="articulo__cuerpo">%4$s<h3>%5$s</h3><p>%6$s</p><p class="articulo__fecha">%7$s</p><p style="margin-top:12px"><a href="%8$s">%9$s</a></p></div></article>',
			$retraso ? ' data-delay="' . $retraso . '"' : '',
			$categoria ? ' data-cat="' . esc_attr( $categoria->slug ) . '"' : '',
			dalila_portada( $entrada->ID ),
			$categoria ? sprintf(
				'<span class="chip chip--%s">%s</span>',
				esc_attr( dalila_color_de_categoria( $categoria->slug ) ),
				esc_html( mb_strtolower( $categoria->name ) )
			) : '',
			esc_html( get_the_title( $entrada ) ),
			esc_html( dalila_texto_de_tarjeta( $entrada->ID ) ),
			esc_html( sprintf( __( '%d min de lectura', 'dalila' ), dalila_minutos_de_lectura( $entrada->ID ) ) ),
			esc_url( get_permalink( $entrada ) ),
			esc_html__( 'Leer más →', 'dalila' )
		);
	}

	$vacio = is_home() ? '<div class="sin-resultados reveal" hidden><strong>' . esc_html__( 'Todavía no hay artículos en esta categoría', 'dalila' ) . '</strong><p>' . esc_html__( 'Escríbeme el tema que te gustaría leer y lo pongo en la lista.', 'dalila' ) . '</p></div>' : '';

	return '<div class="rejilla rejilla--3 rejilla--piezas">' . $tarjetas . '</div>' . $vacio;
}
add_shortcode( 'dalila_articulos', 'dalila_atajo_articulos' );

/**
 * El campo «dalila_tarjeta» se puede ver y editar desde el panel de campos
 * personalizados de cada entrada.
 */
function dalila_registrar_tarjeta() {
	register_post_meta(
		'post',
		'dalila_tarjeta',
		array(
			'type'              => 'string',
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback'     => function () {
				return current_user_can( 'edit_posts' );
			},
		)
	);
}
add_action( 'init', 'dalila_registrar_tarjeta' );

/**
 * Una sola vez, en un sitio que ya se importó sin estos datos: copia a cada
 * entrada el resumen que tenía en su tarjeta y fija el artículo destacado.
 * No pisa nada que ya exista.
 */
function dalila_pasar_tarjetas() {
	if ( get_option( 'dalila_tarjetas_pasadas' ) ) {
		return;
	}

	$datos = require __DIR__ . '/tarjetas.php';

	foreach ( $datos['tarjetas'] as $nombre => $texto ) {
		$entrada = get_page_by_path( $nombre, OBJECT, 'post' );
		if ( $entrada && '' === get_post_meta( $entrada->ID, 'dalila_tarjeta', true ) ) {
			update_post_meta( $entrada->ID, 'dalila_tarjeta', $texto );
		}
	}

	if ( $datos['destacado'] && ! get_option( 'sticky_posts' ) ) {
		$entrada = get_page_by_path( $datos['destacado'], OBJECT, 'post' );
		if ( $entrada ) {
			stick_post( $entrada->ID );
		}
	}

	update_option( 'dalila_tarjetas_pasadas', 1, false );
}
add_action( 'admin_init', 'dalila_pasar_tarjetas' );

/**
 * El contenido que se importó antes de que la guía viviera en el tema todavía
 * apunta al sitio viejo. Se corrige al mostrarlo, para que la descarga siga
 * funcionando cuando GitHub Pages se baje.
 */
function dalila_descargas_del_tema( $html ) {
	$viejo = 'https://helgarpalmieri55.github.io/Paginaweb-DraDalila/assets/descargas/';
	if ( false === strpos( $html, $viejo ) ) {
		return $html;
	}

	return str_replace( $viejo, get_template_directory_uri() . '/assets/descargas/', $html );
}
add_filter( 'render_block', 'dalila_descargas_del_tema' );
