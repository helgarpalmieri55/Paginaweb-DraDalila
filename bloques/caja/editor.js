/* global wp */
/**
 * «Caja del sitio»: un contenedor con la etiqueta, las clases y los
 * atributos del diseño original (blockquote, details, nav, un enlace que
 * envuelve una tarjeta…). Lo de adentro son bloques; para agregar otra caja
 * igual se duplica.
 */
( function ( blocks, element, blockEditor, components, i18n ) {
	'use strict';

	var el = element.createElement;
	var __ = i18n.__;

	var NOMBRES = {
		blockquote: __( 'Testimonio o cita', 'dalila' ),
		details: __( 'Pregunta desplegable', 'dalila' ),
		nav: __( 'Navegación', 'dalila' ),
		a: __( 'Enlace', 'dalila' ),
		ol: __( 'Lista numerada', 'dalila' ),
		ul: __( 'Lista', 'dalila' ),
		li: __( 'Elemento de lista', 'dalila' )
	};

	blocks.registerBlockType( 'dalila/caja', {
		__experimentalLabel: function ( a ) {
			var nombre = NOMBRES[ a.etiqueta ] || __( 'Caja', 'dalila' );
			var clase = ( a.className || '' ).split( ' ' ).filter( function ( c ) {
				return c && 'reveal' !== c && 0 !== c.indexOf( 'retraso-' ) && 0 !== c.indexOf( 'en-' );
			} )[ 0 ];
			return clase ? nombre + ' · ' + clase.replace( /[-_]+/g, ' ' ) : nombre;
		},
		edit: function ( props ) {
			var a = props.attributes;
			var atributos = Object.assign( {}, a.atributos );
			delete atributos.href;
			delete atributos.hidden;
			// Las preguntas desplegables se muestran abiertas para poder editarlas.
			if ( 'details' === a.etiqueta ) {
				atributos.open = true;
			}
			var propsInternos = blockEditor.useInnerBlocksProps( blockEditor.useBlockProps( atributos ) );

			var panel = 'a' === a.etiqueta
				? el(
					blockEditor.InspectorControls,
					null,
					el(
						components.PanelBody,
						{ title: __( 'Enlace', 'dalila' ), initialOpen: true },
						el( components.TextControl, {
							label: __( 'Dirección', 'dalila' ),
							value: a.atributos.href || '',
							onChange: function ( v ) {
								props.setAttributes( { atributos: Object.assign( {}, a.atributos, { href: v } ) } );
							}
						} )
					)
				)
				: null;

			return el( element.Fragment, null, panel, el( a.etiqueta, propsInternos ) );
		},
		save: function ( props ) {
			var a = props.attributes;
			var atributos = Object.assign( {}, a.atributos );
			atributos.className = a.className || undefined;
			return el( a.etiqueta, atributos, el( blockEditor.InnerBlocks.Content ) );
		}
	} );
} )( wp.blocks, wp.element, wp.blockEditor, wp.components, wp.i18n );
