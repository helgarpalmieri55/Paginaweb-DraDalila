<?php
/**
 * Piezas propias de los artículos: la firma con fecha y tiempo de lectura, y
 * el tiempo de lectura suelto por si se quiere usar en otro lado.
 *
 * @package dalila
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Minutos de lectura, a 200 palabras por minuto, que es el promedio de un
 * lector adulto en español.
 */
function dalila_minutos_de_lectura( $post_id = null ) {
	$post_id  = $post_id ? $post_id : get_the_ID();
	$palabras = str_word_count( wp_strip_all_tags( get_post_field( 'post_content', $post_id ) ) );

	return max( 1, (int) ceil( $palabras / 200 ) );
}

/**
 * [dalila_lectura] → «4 min de lectura»
 */
function dalila_atajo_lectura() {
	return sprintf(
		/* translators: %d: minutos. */
		esc_html__( '%d min de lectura', 'dalila' ),
		dalila_minutos_de_lectura()
	);
}
add_shortcode( 'dalila_lectura', 'dalila_atajo_lectura' );

/**
 * [dalila_firma] → la línea completa bajo el título del artículo:
 * quién lo firma, cuándo y cuánto se demora en leerse.
 */
function dalila_atajo_firma() {
	$fecha = get_the_date( 'j \d\e F \d\e Y' );

	return sprintf(
		'<a href="%1$s">%2$s</a>, %3$s · <time datetime="%4$s">%5$s</time> · %6$s',
		esc_url( home_url( '/sobre-mi/' ) ),
		esc_html__( 'la Dra. Dalila Peñaranda', 'dalila' ),
		esc_html__( 'pediatra y especialista en nutrición infantil', 'dalila' ),
		esc_attr( get_the_date( 'c' ) ),
		esc_html( $fecha ),
		esc_html( dalila_atajo_lectura() )
	);
}
add_shortcode( 'dalila_firma', 'dalila_atajo_firma' );

/**
 * Las fechas en español, sin depender de la configuración del servidor.
 */
function dalila_meses_en_espanol( $traducido, $original ) {
	$meses = array(
		'January'   => 'enero',
		'February'  => 'febrero',
		'March'     => 'marzo',
		'April'     => 'abril',
		'May'       => 'mayo',
		'June'      => 'junio',
		'July'      => 'julio',
		'August'    => 'agosto',
		'September' => 'septiembre',
		'October'   => 'octubre',
		'November'  => 'noviembre',
		'December'  => 'diciembre',
	);

	return isset( $meses[ $original ] ) ? $meses[ $original ] : $traducido;
}
add_filter( 'gettext_with_context', 'dalila_meses_en_espanol', 10, 2 );
