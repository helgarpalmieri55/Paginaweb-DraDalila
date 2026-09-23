<?php
/**
 * La franja de mar en el sitio. El contenido lo dibuja franjas.js al cargar,
 * a partir de la escena; aquí solo va el envase con sus datos.
 *
 * @package dalila
 */

$escena = isset( $attributes['escena'] ) ? (int) $attributes['escena'] : 0;
$desde  = isset( $attributes['desde'] ) && 'agua' === $attributes['desde'] ? 'agua' : 'crema';
$hasta  = isset( $attributes['hasta'] ) && 'crema' === $attributes['hasta'] ? 'crema' : 'agua';

printf(
	'<div %s data-escena="%d" data-hasta="%s"></div>',
	get_block_wrapper_attributes( array( 'class' => 'franja franja--' . $desde ) ),
	$escena,
	esc_attr( $hasta )
);
