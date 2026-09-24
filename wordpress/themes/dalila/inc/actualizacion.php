<?php
/**
 * Pasa las páginas y entradas de un sitio ya importado a la versión en
 * bloques editables (ver herramientas/bloques.py).
 *
 * Corre una sola vez, la primera vez que alguien con permiso entra al
 * escritorio. Solo reemplaza lo que sigue igual a como se importó; lo que
 * alguien ya editó no se toca y queda en un aviso para decidirlo a mano.
 * WordPress guarda la versión anterior como revisión, así que todo se puede
 * deshacer desde el historial de cada página.
 *
 * @package dalila
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const DALILA_BLOQUES_VERSION = 2;

/**
 * El contenido sin las direcciones de las imágenes, que el importador cambia
 * al subirlas. Es la misma cuenta que hace herramientas/wordpress.py.
 */
function dalila_normalizar_contenido( $contenido ) {
	$contenido = str_replace( "\r\n", "\n", $contenido );
	$contenido = preg_replace( '#https?://[^"\'\s)]+/([^/"\'\s)]+\.(?:webp|jpe?g|png|gif|svg|pdf))#i', '$1', $contenido );
	// WordPress le agrega «-1», «-scaled» o las medidas al nombre si ya existe.
	$contenido = preg_replace( '#(?:-\d+x\d+|-scaled|-\d+)+(\.(?:webp|jpe?g|png|gif|svg|pdf))\b#i', '$1', $contenido );

	return trim( $contenido );
}

/**
 * Las imágenes del contenido nuevo apuntan al sitio viejo; aquí se cambian
 * por las mismas que ya están en la biblioteca de medios.
 */
function dalila_imagenes_de_la_biblioteca( $contenido ) {
	return preg_replace_callback(
		'#https://helgarpalmieri55\.github\.io/Paginaweb-DraDalila/(assets/img/[^"\'\s)]+)#',
		function ( $m ) {
			$nombre   = sanitize_title( pathinfo( $m[1], PATHINFO_FILENAME ) );
			$adjuntos = get_posts(
				array(
					'post_type'      => 'attachment',
					'name'           => $nombre,
					'posts_per_page' => 1,
					'post_status'    => 'inherit',
				)
			);
			if ( $adjuntos ) {
				return wp_get_attachment_url( $adjuntos[0]->ID );
			}

			// Si no está en la biblioteca, la copia que trae el tema.
			if ( file_exists( get_template_directory() . '/' . $m[1] ) ) {
				return get_template_directory_uri() . '/' . $m[1];
			}

			return $m[0];
		},
		$contenido
	);
}

/**
 * Pone el contenido nuevo en una página o entrada.
 */
function dalila_poner_contenido_nuevo( $post_id, $contenido ) {
	return wp_update_post(
		array(
			'ID'           => $post_id,
			'post_content' => wp_slash( dalila_imagenes_de_la_biblioteca( $contenido ) ),
		),
		true
	);
}

/**
 * La actualización, una sola vez.
 */
function dalila_actualizar_a_bloques() {
	if ( (int) get_option( 'dalila_bloques_version' ) >= DALILA_BLOQUES_VERSION ) {
		return;
	}
	// Los bloques llevan SVG y HTML propio: solo quien puede guardar HTML sin
	// filtrar puede hacer el cambio sin que WordPress se lo recorte.
	if ( ! current_user_can( 'unfiltered_html' ) || wp_doing_ajax() ) {
		return;
	}

	$entradas  = require __DIR__ . '/migracion.php';
	$pendiente = array();

	foreach ( $entradas as $entrada ) {
		$post = get_page_by_path( $entrada['nombre'], OBJECT, $entrada['tipo'] );
		if ( ! $post ) {
			continue;
		}

		$huella = md5( dalila_normalizar_contenido( $post->post_content ) );
		if ( md5( dalila_normalizar_contenido( $entrada['contenido'] ) ) === $huella ) {
			continue; // Ya está al día.
		}
		if ( $huella !== $entrada['antes'] ) {
			// Alguien la editó después de importarla: se decide a mano.
			$pendiente[] = $post->ID;
			continue;
		}

		dalila_poner_contenido_nuevo( $post->ID, $entrada['contenido'] );
	}

	update_option( 'dalila_bloques_pendientes', $pendiente, false );
	update_option( 'dalila_bloques_version', DALILA_BLOQUES_VERSION, false );
}
add_action( 'admin_init', 'dalila_actualizar_a_bloques' );

/**
 * El aviso con lo que quedó sin actualizar porque ya tenía cambios.
 */
function dalila_aviso_de_bloques() {
	$pendiente = array_filter( (array) get_option( 'dalila_bloques_pendientes', array() ) );
	if ( ! $pendiente || ! current_user_can( 'unfiltered_html' ) ) {
		return;
	}

	$lista = array();
	foreach ( $pendiente as $id ) {
		$lista[] = sprintf( '<a href="%s">%s</a>', esc_url( get_edit_post_link( $id ) ), esc_html( get_the_title( $id ) ) );
	}

	$url = wp_nonce_url( admin_url( 'admin-post.php?action=dalila_bloques' ), 'dalila_bloques' );

	printf(
		'<div class="notice notice-warning"><p><strong>%1$s</strong> %2$s</p><p>%3$s</p><p><a class="button button-primary" href="%4$s">%5$s</a> <a class="button" href="%6$s">%7$s</a></p></div>',
		esc_html__( 'Páginas por pasar a bloques editables.', 'dalila' ),
		esc_html__( 'Estas se editaron después de importarlas, así que no se cambiaron solas. Si las actualizas, lo que tenían queda guardado en sus revisiones:', 'dalila' ),
		wp_kses_post( implode( ' · ', $lista ) ),
		esc_url( $url ),
		esc_html__( 'Actualizarlas igual', 'dalila' ),
		esc_url( wp_nonce_url( admin_url( 'admin-post.php?action=dalila_bloques&dejar=1' ), 'dalila_bloques' ) ),
		esc_html__( 'Dejarlas como están', 'dalila' )
	);
}
add_action( 'admin_notices', 'dalila_aviso_de_bloques' );

/**
 * Los dos botones del aviso.
 */
function dalila_resolver_bloques() {
	check_admin_referer( 'dalila_bloques' );
	if ( ! current_user_can( 'unfiltered_html' ) ) {
		wp_die( esc_html__( 'No tienes permiso para esto.', 'dalila' ) );
	}

	if ( empty( $_GET['dejar'] ) ) {
		$pendiente = (array) get_option( 'dalila_bloques_pendientes', array() );
		$entradas  = require __DIR__ . '/migracion.php';

		foreach ( $entradas as $entrada ) {
			$post = get_page_by_path( $entrada['nombre'], OBJECT, $entrada['tipo'] );
			if ( $post && in_array( $post->ID, $pendiente, true ) ) {
				dalila_poner_contenido_nuevo( $post->ID, $entrada['contenido'] );
			}
		}
	}

	delete_option( 'dalila_bloques_pendientes' );
	wp_safe_redirect( wp_get_referer() ? wp_get_referer() : admin_url() );
	exit;
}
add_action( 'admin_post_dalila_bloques', 'dalila_resolver_bloques' );
