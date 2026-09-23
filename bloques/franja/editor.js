/* global wp */
( function ( blocks, element, blockEditor, components, i18n ) {
	'use strict';

	var el = element.createElement;
	var __ = i18n.__;

	// Las seis escenas son las mismas que conoce franjas.js.
	var ESCENAS = [
		{ value: 0, label: __( 'Escena 1 · coral y tortuga', 'dalila' ) },
		{ value: 1, label: __( 'Escena 2 · el pez que cruza', 'dalila' ) },
		{ value: 2, label: __( 'Escena 3 · la ballena entera', 'dalila' ) },
		{ value: 3, label: __( 'Escena 4 · estrellas de mar', 'dalila' ) },
		{ value: 4, label: __( 'Escena 5 · el bosque de corales', 'dalila' ) },
		{ value: 5, label: __( 'Escena 6 · burbujas y tortuga', 'dalila' ) }
	];

	var FONDOS = [
		{ value: 'crema', label: __( 'Crema', 'dalila' ) },
		{ value: 'agua', label: __( 'Agua', 'dalila' ) }
	];

	blocks.registerBlockType( 'dalila/franja', {
		edit: function ( props ) {
			var a = props.attributes;
			var propsBloque = blockEditor.useBlockProps( {
				className: 'franja franja--' + a.desde,
				'data-escena': a.escena,
				'data-hasta': a.hasta
			} );

			return el(
				element.Fragment,
				null,
				el(
					blockEditor.InspectorControls,
					null,
					el(
						components.PanelBody,
						{ title: __( 'La franja', 'dalila' ), initialOpen: true },
						el( components.SelectControl, {
							label: __( 'Escena', 'dalila' ),
							value: a.escena,
							options: ESCENAS,
							onChange: function ( v ) {
								props.setAttributes( { escena: parseInt( v, 10 ) } );
							},
							help: __( 'Cada escena reparte distinto la ballena, los corales y las estrellas.', 'dalila' )
						} ),
						el( components.SelectControl, {
							label: __( 'Color de la sección de arriba', 'dalila' ),
							value: a.desde,
							options: FONDOS,
							onChange: function ( v ) {
								props.setAttributes( { desde: v } );
							}
						} ),
						el( components.SelectControl, {
							label: __( 'Color de la sección de abajo', 'dalila' ),
							value: a.hasta,
							options: FONDOS,
							onChange: function ( v ) {
								props.setAttributes( { hasta: v } );
							},
							help: __( 'Las olas terminan con este color, para que se funda con lo que sigue.', 'dalila' )
						} )
					)
				),
				el( 'div', propsBloque )
			);
		},
		save: function () {
			return null;
		}
	} );
} )( wp.blocks, wp.element, wp.blockEditor, wp.components, wp.i18n );
