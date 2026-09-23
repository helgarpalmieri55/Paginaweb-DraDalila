<?php
/**
 * Registro del bloque «Franja de mar».
 *
 * El dibujo lo arma assets/js/franjas.js al cargar la página, a partir de la
 * escena elegida. Aquí solo se registra el bloque para que aparezca en el
 * escritorio con su selector de escena y de colores.
 *
 * @package dalila
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function dalila_registrar_bloques() {
	register_block_type( get_template_directory() . '/bloques/franja' );
}
add_action( 'init', 'dalila_registrar_bloques' );

/**
 * En el escritorio no corre franjas.js, así que la franja se vería vacía.
 * Este trocito la dibuja también dentro del editor.
 */
function dalila_franjas_en_el_editor() {
	$dir = get_template_directory_uri();

	wp_enqueue_script( 'dalila-franjas-editor', $dir . '/assets/js/franjas.js', array(), DALILA_VERSION, true );
	wp_add_inline_script(
		'dalila-franjas-editor',
		"document.documentElement.setAttribute('data-base', " . wp_json_encode( trailingslashit( $dir ) ) . ');',
		'before'
	);
}
add_action( 'enqueue_block_editor_assets', 'dalila_franjas_en_el_editor' );
