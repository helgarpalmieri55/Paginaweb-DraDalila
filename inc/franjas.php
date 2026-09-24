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
	register_block_type( get_template_directory() . '/bloques/imagen' );
}
add_action( 'init', 'dalila_registrar_bloques' );

/**
 * En el escritorio no corre la página completa, así que franjas.js se carga
 * aparte: el bloque lo usa para dibujar su escena mientras se edita.
 */
function dalila_registrar_franjas_del_editor() {
	$dir = get_template_directory_uri();

	wp_register_script( 'dalila-franjas-editor', $dir . '/assets/js/franjas.js', array(), DALILA_VERSION, true );
	wp_add_inline_script(
		'dalila-franjas-editor',
		"document.documentElement.setAttribute('data-base', " . wp_json_encode( trailingslashit( $dir ) ) . ');',
		'before'
	);
}
add_action( 'init', 'dalila_registrar_franjas_del_editor', 5 );

/**
 * Los estilos del sitio dentro del lienzo del editor, tal cual, para que lo
 * que se edita se vea como la página publicada.
 */
function dalila_estilos_en_el_editor() {
	if ( ! is_admin() ) {
		return;
	}

	$dir = get_template_directory_uri();

	wp_enqueue_style( 'dalila-base-editor', $dir . '/assets/css/site.css', array(), DALILA_VERSION );
	wp_enqueue_style( 'dalila-paginas-editor', $dir . '/assets/css/paginas.css', array( 'dalila-base-editor' ), DALILA_VERSION );
	wp_enqueue_style( 'dalila-wp-editor', $dir . '/assets/css/wordpress.css', array( 'dalila-paginas-editor' ), DALILA_VERSION );
	wp_enqueue_style( 'dalila-bloques-editor', $dir . '/assets/css/bloques.css', array( 'dalila-wp-editor' ), DALILA_VERSION );
	wp_enqueue_style( 'dalila-editor', $dir . '/assets/css/editor.css', array( 'dalila-bloques-editor' ), DALILA_VERSION );
}
add_action( 'enqueue_block_assets', 'dalila_estilos_en_el_editor' );
