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

/**
 * La firma de la autora va en el mismo lugar que en el sitio: después de
 * «Sigue leyendo» y antes del cierre del artículo. Como el cierre viene dentro
 * del contenido, la firma se mete justo antes de él. Si un artículo nuevo no
 * trae cierre, la firma queda al final.
 */
function dalila_firma_en_su_lugar( $html ) {
	if ( ! is_singular( 'post' ) ) {
		return $html;
	}

	$patron = WP_Block_Patterns_Registry::get_instance()->get_registered( 'dalila/firma-autora' );
	if ( ! $patron || preg_match( '/class="[^"]*\bautora\b/', $html ) ) {
		return $html;
	}

	$firma  = do_blocks( $patron['content'] );
	// El último <section> con la clase «cierre», venga como HTML o como grupo.
	if ( preg_match_all( '/<section class="[^"]*\bcierre\b/', $html, $hallados, PREG_OFFSET_CAPTURE ) ) {
		$cierre = end( $hallados[0] );
		return substr_replace( $html, $firma, $cierre[1], 0 );
	}

	$fin = strrpos( $html, '</div>' );

	return false === $fin ? $html . $firma : substr_replace( $html, $firma, $fin, 0 );
}
add_filter( 'render_block_core/post-content', 'dalila_firma_en_su_lugar' );

/**
 * Las migas del artículo terminan en su título, como en el sitio:
 * Inicio › Blog › Dolor de oído a medianoche.
 */
function dalila_migas_con_titulo( $html ) {
	if ( ! is_singular( 'post' ) || false === strpos( $html, 'class="migas' ) || false !== strpos( $html, 'aria-current' ) ) {
		return $html;
	}

	$flecha = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>';
	$titulo = sprintf( '<span aria-current="page">%s</span>', esc_html( get_the_title( get_queried_object_id() ) ) );

	return preg_replace( '#</nav>#', $flecha . "\n\t\t\t\t" . $titulo . "\n\t\t\t</nav>", $html, 1 );
}
add_filter( 'render_block_core/html', 'dalila_migas_con_titulo' );

/**
 * Un artículo nuevo empieza con la misma sección de lectura que los que ya
 * están publicados, para que el texto quede con el ancho y el aire del sitio.
 */
function dalila_molde_de_articulo( $argumentos, $tipo ) {
	if ( 'post' !== $tipo ) {
		return $argumentos;
	}

	$argumentos['template'] = array(
		array(
			'core/group',
			array(
				'className' => 'seccion seccion--crema seccion--lectura',
				'layout'    => array( 'type' => 'constrained' ),
			),
			array(
				array(
					'core/group',
					array(
						'className' => 'prosa',
						'layout'    => array( 'type' => 'constrained' ),
					),
					array(
						array( 'core/paragraph', array( 'placeholder' => __( 'Empieza a escribir el artículo…', 'dalila' ) ) ),
					),
				),
			),
		),
	);

	return $argumentos;
}
add_filter( 'register_post_type_args', 'dalila_molde_de_articulo', 10, 2 );
