/* global wp */
/**
 * «Texto del sitio»: una etiqueta cualquiera (span, strong, a, small, div…)
 * con su texto editable y los mismos atributos y clases del diseño original.
 * Si el original lleva un ícono SVG al principio o al final, se guarda tal
 * cual y no se toca al editar.
 */
( function ( blocks, element, blockEditor, components, i18n ) {
	'use strict';

	var el = element.createElement;
	var __ = i18n.__;

	// En el editor no se navega ni se esconde nada: fuera href y hidden.
	function atributosDelEditor( atributos ) {
		var copia = Object.assign( {}, atributos );
		delete copia.href;
		delete copia.hidden;
		return copia;
	}

	function icono( a ) {
		return el( 'span', {
			style: { display: 'contents' },
			dangerouslySetInnerHTML: { __html: a.icono }
		} );
	}

	blocks.registerBlockType( 'dalila/texto', {
		__experimentalLabel: function ( a, contexto ) {
			if ( contexto && 'list-view' === contexto.context && a.contenido ) {
				return a.contenido.replace( /<[^>]+>/g, '' ).slice( 0, 40 );
			}
		},
		edit: function ( props ) {
			var a = props.attributes;
			var propsBloque = blockEditor.useBlockProps( atributosDelEditor( a.atributos ) );

			function cambiarAtributo( nombre, valor ) {
				var nuevos = Object.assign( {}, a.atributos );
				nuevos[ nombre ] = valor;
				props.setAttributes( { atributos: nuevos } );
			}

			var panel = el(
				blockEditor.InspectorControls,
				null,
				'a' === a.etiqueta
					? el(
						components.PanelBody,
						{ title: __( 'Enlace', 'dalila' ), initialOpen: true },
						el( components.TextControl, {
							label: __( 'Dirección', 'dalila' ),
							help: __( 'A dónde lleva al hacer clic: una página del sitio (/citas/) o una dirección completa.', 'dalila' ),
							value: a.atributos.href || '',
							onChange: function ( v ) {
								cambiarAtributo( 'href', v );
							}
						} )
					)
					: null
			);

			var texto = {
				value: a.contenido,
				onChange: function ( v ) {
					props.setAttributes( { contenido: v } );
				},
				placeholder: __( 'Escribe aquí…', 'dalila' )
			};

			var cuerpo = a.icono
				? el(
					a.etiqueta,
					propsBloque,
					a.iconoAlFinal ? null : icono( a ),
					el( blockEditor.RichText, Object.assign( { tagName: 'span' }, texto ) ),
					a.iconoAlFinal ? icono( a ) : null
				)
				: el( blockEditor.RichText, Object.assign( {}, propsBloque, { tagName: a.etiqueta }, texto ) );

			return el( element.Fragment, null, panel, cuerpo );
		},
		save: function ( props ) {
			var a = props.attributes;
			var atributos = Object.assign( {}, a.atributos );
			atributos.className = a.className || undefined;
			var antes = a.icono && ! a.iconoAlFinal ? el( element.RawHTML, null, a.icono ) : null;
			var despues = a.icono && a.iconoAlFinal ? el( element.RawHTML, null, a.icono ) : null;
			return el( a.etiqueta, atributos, antes, el( blockEditor.RichText.Content, { value: a.contenido } ), despues );
		}
	} );
} )( wp.blocks, wp.element, wp.blockEditor, wp.components, wp.i18n );
