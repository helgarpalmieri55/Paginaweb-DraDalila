<?php
/**
 * Tema de la Dra. Dalila Peñaranda.
 *
 * El diseño vive en assets/css; este archivo solo lo conecta con WordPress y
 * expone los datos del consultorio para que se editen desde el escritorio.
 *
 * @package dalila
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'DALILA_VERSION', wp_get_theme()->get( 'Version' ) );

require_once __DIR__ . '/inc/ajustes.php';
require_once __DIR__ . '/inc/cabecera.php';
require_once __DIR__ . '/inc/patrones.php';
require_once __DIR__ . '/inc/franjas.php';
require_once __DIR__ . '/inc/articulos.php';
require_once __DIR__ . '/inc/blog.php';
require_once __DIR__ . '/inc/posicionamiento.php';

/**
 * Lo que el tema le dice a WordPress que sabe hacer.
 */
function dalila_soporte() {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'html5', array( 'style', 'script', 'navigation-widgets' ) );
	add_theme_support( 'editor-styles' );
	add_editor_style( 'assets/css/editor.css' );

	// El ancho del sitio y las alineaciones los define theme.json.
	remove_theme_support( 'core-block-patterns' );
}
add_action( 'after_setup_theme', 'dalila_soporte' );

/**
 * Hojas de estilo y guiones del sitio.
 *
 * Son los mismos archivos del sitio estático: si algo se corrige aquí, se
 * corrige en el diseño original y viceversa.
 */
function dalila_recursos() {
	$dir = get_template_directory_uri();

	wp_enqueue_style( 'dalila-base', $dir . '/assets/css/site.css', array(), DALILA_VERSION );
	wp_enqueue_style( 'dalila-paginas', $dir . '/assets/css/paginas.css', array( 'dalila-base' ), DALILA_VERSION );
	wp_enqueue_style( 'dalila-wp', $dir . '/assets/css/wordpress.css', array( 'dalila-paginas' ), DALILA_VERSION );

	wp_enqueue_script( 'dalila-franjas', $dir . '/assets/js/franjas.js', array(), DALILA_VERSION, true );
	wp_enqueue_script( 'dalila-sitio', $dir . '/assets/js/site.js', array(), DALILA_VERSION, true );

	// Los datos de contacto salen de los ajustes, no del código.
	wp_add_inline_script(
		'dalila-sitio',
		'window.DALILA_CONFIG = ' . wp_json_encode( dalila_config() ) . ';',
		'before'
	);
}
add_action( 'wp_enqueue_scripts', 'dalila_recursos' );

/**
 * Dos cosas van en la etiqueta <html>: la base con la que las franjas de mar
 * buscan sus dibujos, y la clase «no-js», que el guion del sitio quita al
 * cargar. Mientras está puesta, las franjas quedan en cero y no dejan un hueco
 * en blanco a quien navega sin JavaScript.
 */
function dalila_atributos_del_html( $salida ) {
	return $salida
		. ' class="no-js"'
		. ' data-base="' . esc_url( trailingslashit( get_template_directory_uri() ) ) . '"';
}
add_filter( 'language_attributes', 'dalila_atributos_del_html' );

/**
 * Precarga de las dos fuentes, que es lo que más pesa en la primera pintada.
 */
function dalila_precarga_fuentes() {
	$dir = get_template_directory_uri() . '/assets/fonts/';
	foreach ( array( 'baloo2-latin.woff2', 'nunito-latin.woff2' ) as $fuente ) {
		printf(
			'<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n",
			esc_url( $dir . $fuente )
		);
	}
}
add_action( 'wp_head', 'dalila_precarga_fuentes', 1 );

/**
 * Categorías propias para el selector de patrones del escritorio.
 */
function dalila_categorias_de_patrones() {
	register_block_pattern_category(
		'dalila-secciones',
		array( 'label' => __( 'Secciones del sitio', 'dalila' ) )
	);
	register_block_pattern_category(
		'dalila-piezas',
		array( 'label' => __( 'Piezas sueltas', 'dalila' ) )
	);
}
add_action( 'init', 'dalila_categorias_de_patrones' );
