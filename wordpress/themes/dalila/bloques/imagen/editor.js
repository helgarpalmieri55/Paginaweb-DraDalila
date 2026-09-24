/* global wp */
/**
 * «Imagen del sitio»: guarda un <img> idéntico al del diseño original, con
 * sus clases, para que el marco, el recorte y la sombra sigan saliendo de la
 * hoja de estilos. En el editor se cambia con «Reemplazar».
 */
( function ( blocks, element, blockEditor, components, i18n ) {
	'use strict';

	var el = element.createElement;
	var __ = i18n.__;

	// Los atributos del <img>, en el orden en que se escriben.
	function atributosDeImagen( a ) {
		return {
			src: a.url,
			alt: a.alt || '',
			width: a.width || undefined,
			height: a.height || undefined,
			loading: a.loading || undefined,
			fetchpriority: a.fetchpriority || undefined
		};
	}

	blocks.registerBlockType( 'dalila/imagen', {
		edit: function ( props ) {
			var a = props.attributes;

			function elegir( medio ) {
				if ( ! medio || ! medio.url ) {
					return;
				}
				// La versión grande basta para la web; si no existe, la original.
				var grande = medio.sizes && medio.sizes.large ? medio.sizes.large : medio;
				props.setAttributes( {
					url: grande.url || medio.url,
					alt: medio.alt || a.alt,
					width: String( grande.width || medio.width || '' ) || undefined,
					height: String( grande.height || medio.height || '' ) || undefined
				} );
			}

			return el(
				element.Fragment,
				null,
				el(
					blockEditor.BlockControls,
					{ group: 'other' },
					el( blockEditor.MediaReplaceFlow, {
						mediaURL: a.url,
						allowedTypes: [ 'image' ],
						accept: 'image/*',
						onSelect: elegir,
						name: __( 'Reemplazar', 'dalila' )
					} )
				),
				el(
					blockEditor.InspectorControls,
					null,
					el(
						components.PanelBody,
						{ title: __( 'La imagen', 'dalila' ), initialOpen: true },
						el( components.TextareaControl, {
							label: __( 'Texto alternativo', 'dalila' ),
							help: __( 'Describe la imagen para quien no puede verla y para los buscadores.', 'dalila' ),
							value: a.alt,
							onChange: function ( v ) {
								props.setAttributes( { alt: v } );
							}
						} )
					)
				),
				a.url
					? el( 'img', blockEditor.useBlockProps( atributosDeImagen( a ) ) )
					: el(
						'div',
						blockEditor.useBlockProps(),
						el( blockEditor.MediaPlaceholder, {
							icon: 'format-image',
							labels: { title: __( 'Imagen del sitio', 'dalila' ) },
							allowedTypes: [ 'image' ],
							accept: 'image/*',
							onSelect: elegir
						} )
					)
			);
		},
		save: function ( props ) {
			// La clase va escrita aquí: es la que le da al <img> su forma en el
			// diseño (marco, recorte, alto) y tiene que guardarse con él.
			var atributos = atributosDeImagen( props.attributes );
			atributos.className = props.attributes.className || undefined;
			return el( 'img', atributos );
		}
	} );
} )( wp.blocks, wp.element, wp.blockEditor, wp.components, wp.i18n );
