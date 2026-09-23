<?php
/**
 * Plugin Name: Posicionamiento · Dra. Dalila Peñaranda
 * Description: Los datos estructurados y las etiquetas sociales que ya tenía el sitio, ahora alimentados por Ajustes → Datos del consultorio. Va en mu-plugins para que esté siempre activo.
 * Version: 1.0.0
 * Author: novieri
 *
 * Es el mismo esquema que generaba herramientas/seo.py: Physician con la
 * dirección y los servicios, Person de la doctora, migas de pan, BlogPosting en
 * los artículos y las preguntas frecuentes que haya en la página.
 *
 * Lo que no lleva, a propósito: horarios de atención, títulos universitarios,
 * registro médico ni reseñas. Ninguno está confirmado, y un dato inventado en
 * los datos estructurados es peor que no ponerlo.
 *
 * @package dalila
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const DALILA_SEO_ESPECIALIDADES = array( 'Pediatric', 'DietNutrition' );

const DALILA_SEO_SERVICIOS = array(
	array( 'Control pediátrico', 'Revisión completa del crecimiento, el desarrollo, la alimentación y el esquema de vacunación, desde recién nacido hasta la adolescencia.' ),
	array( 'Nutrición infantil', 'Valoración nutricional con antropometría y plan de alimentación ajustado a la edad, los hábitos y la realidad de cada casa.' ),
	array( 'Crecimiento y desarrollo', 'Seguimiento de talla, peso y perímetro cefálico sobre las curvas de la OMS, y de los hitos del desarrollo.' ),
	array( 'Alimentación complementaria', 'Acompañamiento en el inicio de sólidos: texturas, cantidades, señales de alarma y manejo de la selectividad.' ),
	array( 'Asesoría a padres', 'Lactancia, sueño, pataletas y dudas de crianza resueltas con tiempo y sin apuro.' ),
	array( 'Consulta virtual', 'Videollamada para familias dentro y fuera de Colombia, con el plan enviado por correo.' ),
);

const DALILA_SEO_TEMAS = array(
	'Pediatría', 'Nutrición infantil', 'Lactancia materna', 'Alimentación complementaria',
	'Crecimiento y desarrollo infantil', 'Puericultura', 'Selectividad alimentaria',
);

/**
 * Los datos del consultorio. Si el tema no está activo, valores de respaldo.
 */
function dalila_seo_datos() {
	if ( function_exists( 'dalila_datos' ) ) {
		return dalila_datos();
	}

	return array(
		'whatsapp'   => '+57 304 653 2006',
		'correo'     => 'nutripedcm@gmail.com',
		'direccion'  => 'Calle 1C # 30-40, High Park Medical Center',
		'direccion2' => 'Consultorio 129 · Barranquilla, Colombia',
		'instagram'  => 'https://www.instagram.com/dra.dalilapenaranda/',
	);
}

/**
 * ¿Hay ya un plugin de SEO puesto? Si lo hay, este se aparta de las etiquetas
 * meta y deja solo los datos estructurados, para no duplicar nada.
 */
function dalila_seo_hay_otro_plugin() {
	return defined( 'WPSEO_VERSION' )        // Yoast
		|| defined( 'RANK_MATH_VERSION' )    // Rank Math
		|| defined( 'SEOPRESS_VERSION' )     // SEOPress
		|| defined( 'AIOSEO_VERSION' );      // All in One SEO
}

/**
 * Las identidades, que son las mismas en todas las páginas.
 */
function dalila_seo_identidades() {
	$d    = dalila_seo_datos();
	$casa = trailingslashit( home_url() );

	$practica = array(
		'@type'       => array( 'Physician', 'MedicalBusiness' ),
		'@id'         => $casa . '#consultorio',
		'name'        => 'Dra. Dalila Peñaranda — Pediatría y Nutrición Infantil',
		'alternateName' => 'Dra. Dalila Peñaranda',
		'description' => 'Consulta de pediatría y nutrición infantil en Barranquilla, con atención presencial y virtual desde recién nacidos hasta la adolescencia.',
		'url'         => $casa,
		'telephone'   => preg_replace( '/[^\d+]/', '', $d['whatsapp'] ),
		'email'       => $d['correo'],
		'address'     => array(
			'@type'           => 'PostalAddress',
			'streetAddress'   => trim( $d['direccion'] . ', ' . preg_replace( '/\s*·.*$/u', '', $d['direccion2'] ) ),
			'addressLocality' => 'Barranquilla',
			'addressRegion'   => 'Atlántico',
			'addressCountry'  => 'CO',
		),
		'medicalSpecialty' => DALILA_SEO_ESPECIALIDADES,
		'areaServed'       => array(
			array( '@type' => 'City', 'name' => 'Barranquilla' ),
			array( '@type' => 'AdministrativeArea', 'name' => 'Atlántico, Colombia' ),
		),
		'availableService' => array_map(
			function ( $s ) {
				return array( '@type' => 'MedicalProcedure', 'name' => $s[0], 'description' => $s[1] );
			},
			DALILA_SEO_SERVICIOS
		),
		'physician'  => array( '@id' => $casa . '#dalila' ),
		'employee'   => array( '@id' => $casa . '#dalila' ),
		'sameAs'     => array_values( array_filter( array( $d['instagram'] ) ) ),
		'knowsLanguage'        => 'es',
		'isAcceptingNewPatients' => true,
		'currenciesAccepted'   => 'COP, USD',
	);

	$logo = get_theme_mod( 'custom_logo' ) ? wp_get_attachment_image_url( get_theme_mod( 'custom_logo' ), 'full' ) : '';
	if ( $logo ) {
		$practica['logo']  = $logo;
		$practica['image'] = $logo;
	}

	$doctora = array(
		'@type'          => 'Person',
		'@id'            => $casa . '#dalila',
		'name'           => 'Dalila Peñaranda',
		'honorificPrefix' => 'Dra.',
		'jobTitle'       => 'Pediatra y especialista en nutrición infantil',
		'description'    => 'Pediatra con subespecialidad en nutrición infantil. Atiende en Barranquilla y por videollamada a familias dentro y fuera de Colombia.',
		'url'            => $casa . 'sobre-mi/',
		'worksFor'       => array( '@id' => $casa . '#consultorio' ),
		'knowsAbout'     => DALILA_SEO_TEMAS,
		'knowsLanguage'  => 'es',
		'sameAs'         => array_values( array_filter( array( $d['instagram'] ) ) ),
	);

	$sitio = array(
		'@type'      => 'WebSite',
		'@id'        => $casa . '#sitio',
		'url'        => $casa,
		'name'       => get_bloginfo( 'name' ),
		'inLanguage' => 'es-CO',
		'publisher'  => array( '@id' => $casa . '#consultorio' ),
	);

	return array( $sitio, $practica, $doctora );
}

/**
 * Las preguntas frecuentes que haya en la página, sacadas de su propio texto.
 * Así nunca se desfasan de lo que se ve.
 */
function dalila_seo_preguntas( $contenido, $id_pagina ) {
	if ( ! preg_match_all( '#<details[^>]*>(.*?)</details>#is', $contenido, $bloques ) ) {
		return null;
	}

	$pares = array();
	foreach ( $bloques[1] as $bloque ) {
		if ( ! preg_match( '#<summary[^>]*>(.*?)</summary>#is', $bloque, $p ) ) {
			continue;
		}
		$pregunta  = trim( wp_strip_all_tags( preg_replace( '#<svg.*?</svg>#is', '', $p[1] ) ) );
		$respuesta = trim( wp_strip_all_tags( preg_replace( '#<summary.*?</summary>#is', '', $bloque ) ) );
		$respuesta = trim( preg_replace( '/\s+/u', ' ', $respuesta ) );

		// Nada que siga marcado como pendiente entra en los datos estructurados.
		if ( '' === $respuesta || false !== mb_stripos( $respuesta, 'pendiente de confirmar' ) ) {
			continue;
		}
		$pares[] = array(
			'@type'          => 'Question',
			'name'           => $pregunta,
			'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $respuesta ),
		);
	}

	if ( ! $pares ) {
		return null;
	}

	return array(
		'@type'      => 'FAQPage',
		'@id'        => get_permalink( $id_pagina ) . '#faq',
		'mainEntity' => $pares,
	);
}

/**
 * El bloque completo de datos estructurados de la página que se está viendo.
 */
function dalila_seo_grafo() {
	$casa  = trailingslashit( home_url() );
	$nodos = dalila_seo_identidades();

	if ( is_singular() ) {
		$id      = get_queried_object_id();
		$url     = get_permalink( $id );
		$titulo  = get_the_title( $id );
		$resumen = wp_strip_all_tags( get_the_excerpt( $id ) );
		$imagen  = get_the_post_thumbnail_url( $id, 'full' );

		if ( is_singular( 'post' ) ) {
			$nodos[] = array(
				'@type'            => 'BreadcrumbList',
				'@id'              => $url . '#migas',
				'itemListElement'  => array(
					array( '@type' => 'ListItem', 'position' => 1, 'name' => 'Inicio', 'item' => $casa ),
					array( '@type' => 'ListItem', 'position' => 2, 'name' => 'Blog', 'item' => get_permalink( get_option( 'page_for_posts' ) ) ),
					array( '@type' => 'ListItem', 'position' => 3, 'name' => $titulo ),
				),
			);
			$nodos[] = array_filter( array(
				'@type'            => 'BlogPosting',
				'@id'              => $url . '#articulo',
				'headline'         => mb_substr( $titulo, 0, 110 ),
				'name'             => $titulo,
				'description'      => $resumen,
				'url'              => $url,
				'mainEntityOfPage' => array( '@type' => 'WebPage', '@id' => $url ),
				'image'            => $imagen,
				'datePublished'    => get_the_date( 'c', $id ),
				'dateModified'     => get_the_modified_date( 'c', $id ),
				'author'           => array( '@id' => $casa . '#dalila' ),
				'publisher'        => array( '@id' => $casa . '#consultorio' ),
				'inLanguage'       => 'es-CO',
			) );
		} else {
			$nodos[] = array_filter( array(
				'@type'       => 'WebPage',
				'@id'         => $url . '#pagina',
				'url'         => $url,
				'name'        => $titulo,
				'description' => $resumen,
				'isPartOf'    => array( '@id' => $casa . '#sitio' ),
				'about'       => array( '@id' => $casa . '#consultorio' ),
				'inLanguage'  => 'es-CO',
				'primaryImageOfPage' => $imagen,
			) );
		}

		$faq = dalila_seo_preguntas( get_post_field( 'post_content', $id ), $id );
		if ( $faq ) {
			$nodos[] = $faq;
		}
	}

	return array( '@context' => 'https://schema.org', '@graph' => array_values( $nodos ) );
}

/**
 * Lo que se imprime en la cabecera de cada página.
 */
function dalila_seo_cabecera() {
	if ( is_admin() || is_feed() ) {
		return;
	}

	echo "\n<!-- Posicionamiento · Dra. Dalila Peñaranda -->\n";

	if ( ! dalila_seo_hay_otro_plugin() ) {
		$titulo  = wp_get_document_title();
		$resumen = '';
		$imagen  = '';

		if ( is_singular() ) {
			$id      = get_queried_object_id();
			$resumen = wp_strip_all_tags( get_the_excerpt( $id ) );
			$imagen  = get_the_post_thumbnail_url( $id, 'full' );
		}
		if ( ! $resumen ) {
			$resumen = get_bloginfo( 'description' );
		}

		$url = is_singular() ? get_permalink() : home_url( add_query_arg( array() ) );

		printf( '<meta name="description" content="%s">' . "\n", esc_attr( $resumen ) );
		printf( '<meta name="robots" content="%s">' . "\n", 'index, follow, max-image-preview:large, max-snippet:-1' );
		printf( '<meta property="og:type" content="%s">' . "\n", is_singular( 'post' ) ? 'article' : 'website' );
		printf( '<meta property="og:url" content="%s">' . "\n", esc_url( $url ) );
		printf( '<meta property="og:site_name" content="%s">' . "\n", esc_attr( get_bloginfo( 'name' ) ) );
		printf( '<meta property="og:locale" content="%s">' . "\n", 'es_CO' );
		printf( '<meta property="og:title" content="%s">' . "\n", esc_attr( $titulo ) );
		printf( '<meta property="og:description" content="%s">' . "\n", esc_attr( $resumen ) );
		printf( '<meta name="twitter:card" content="%s">' . "\n", 'summary_large_image' );
		if ( $imagen ) {
			printf( '<meta property="og:image" content="%1$s">' . "\n<meta name=\"twitter:image\" content=\"%1\$s\">\n", esc_url( $imagen ) );
		}
		printf( '<meta name="geo.region" content="%s">' . "\n", 'CO-ATL' );
		printf( '<meta name="geo.placename" content="%s">' . "\n", 'Barranquilla' );
		printf( '<link rel="canonical" href="%s">' . "\n", esc_url( $url ) );
	}

	printf(
		'<script type="application/ld+json">%s</script>' . "\n",
		wp_json_encode( dalila_seo_grafo(), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT )
	);
}
add_action( 'wp_head', 'dalila_seo_cabecera', 5 );
