<?php
/**
 * La barra y el pie: el logo mientras no se haya subido uno y el enlace del
 * menú que corresponde a la página abierta.
 *
 * @package dalila
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Si todavía no hay logo en Apariencia → Editor → Identidad del sitio, el
 * bloque Logo no pinta nada. Mientras tanto se muestra el logo del sitio, el
 * mismo que va en el tema. Apenas se sube uno, manda el que se subió.
 */
function dalila_logo_de_respaldo( $html, $bloque ) {
	if ( '' !== trim( $html ) ) {
		return $html;
	}

	$clase = isset( $bloque['attrs']['className'] ) ? $bloque['attrs']['className'] : '';
	$img   = sprintf(
		'<img src="%s" alt="%s" width="615" height="260"%s>',
		esc_url( get_template_directory_uri() . '/assets/img/logo.webp' ),
		esc_attr__( 'Dra. Dalila Peñaranda — Pediatría y Nutrición', 'dalila' ),
		false !== strpos( $clase, 'pie__logo' ) ? ' loading="lazy"' : ''
	);

	return sprintf(
		'<div class="wp-block-site-logo %s"><a href="%s" rel="home">%s</a></div>',
		esc_attr( $clase ),
		esc_url( home_url( '/' ) ),
		$img
	);
}
add_filter( 'render_block_core/site-logo', 'dalila_logo_de_respaldo', 10, 2 );

/**
 * La ruta de la página abierta, como la escribe el menú: «/sobre-mi/».
 * Los artículos, sus categorías y el buscador cuentan como «/blog/».
 */
function dalila_ruta_actual() {
	if ( is_singular( 'post' ) || is_home() || is_category() || is_tag() || is_search() ) {
		return '/blog/';
	}

	$ruta = (string) wp_parse_url( add_query_arg( array() ), PHP_URL_PATH );
	$base = untrailingslashit( (string) wp_parse_url( home_url(), PHP_URL_PATH ) );
	if ( '' !== $base && 0 === strpos( $ruta, $base ) ) {
		$ruta = substr( $ruta, strlen( $base ) );
	}
	$ruta = '/' . ltrim( $ruta, '/' );

	return trailingslashit( $ruta );
}

/**
 * Marca con aria-current el enlace del menú de la página en la que se está,
 * que es de donde sale el fondo rosado del sitio.
 */
function dalila_menu_actual( $html, $bloque ) {
	$url = isset( $bloque['attrs']['url'] ) ? $bloque['attrs']['url'] : '';
	if ( '' === $url || false !== strpos( $html, 'aria-current' ) ) {
		return $html;
	}

	$ruta = wp_parse_url( $url, PHP_URL_PATH );
	if ( ! $ruta || '/' === $ruta || trailingslashit( $ruta ) !== dalila_ruta_actual() ) {
		return $html;
	}

	return preg_replace( '/<a /', '<a aria-current="page" ', $html, 1 );
}
add_filter( 'render_block_core/navigation-link', 'dalila_menu_actual', 10, 2 );
