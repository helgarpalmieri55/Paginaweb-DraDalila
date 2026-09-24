<?php
/**
 * Los patrones viven como archivos en /patterns y WordPress los registra solo.
 * Aquí quedan únicamente los ajustes que no caben en un archivo de patrón.
 *
 * @package dalila
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Los patrones traen textos e imágenes de ejemplo que el community manager
 * reemplaza. Para que no se le cuelen los de WordPress ni los del directorio
 * de patrones remoto, se apagan los dos.
 */
function dalila_solo_nuestros_patrones() {
	remove_theme_support( 'core-block-patterns' );
}
add_action( 'after_setup_theme', 'dalila_solo_nuestros_patrones', 20 );

add_filter( 'should_load_remote_block_patterns', '__return_false' );
