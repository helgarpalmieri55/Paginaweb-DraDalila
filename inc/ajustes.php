<?php
/**
 * «Datos del consultorio»: la pantalla donde se editan el teléfono, el correo,
 * la dirección, las tarifas y los enlaces de compra sin tocar una línea de código.
 *
 * Todo vive en una sola opción, para que respaldar y restaurar sea simple.
 *
 * @package dalila
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const DALILA_OPCION = 'dalila_datos';

/**
 * Los valores con los que arranca el sitio si nadie ha tocado nada.
 */
function dalila_datos_por_defecto() {
	return array(
		'whatsapp'           => '+57 304 653 2006',
		'mensaje_whatsapp'   => 'Hola doctora, quiero agendar una cita',
		'correo'             => 'nutripedcm@gmail.com',
		'direccion'          => 'Calle 1C # 30-40, High Park Medical Center',
		'direccion2'         => 'Consultorio 129 · Barranquilla, Colombia',
		'precio_presencial'  => '$180.000',
		'precio_virtual'     => '45 USD',
		'instagram'          => 'https://www.instagram.com/dra.dalilapenaranda/',
		'hotmart_complementaria' => '',
		'hotmart_lonchera'       => '',
		'hotmart_habitos'        => '',
		'hotmart_escuela'        => '',
	);
}

/**
 * Los datos guardados, completados con los de fábrica.
 */
function dalila_datos() {
	return wp_parse_args( (array) get_option( DALILA_OPCION, array() ), dalila_datos_por_defecto() );
}

/**
 * Los mismos datos con la forma que espera el JavaScript del sitio.
 */
function dalila_config() {
	$d = dalila_datos();

	return array(
		'whatsapp'        => $d['whatsapp'],
		'mensajeWhatsApp' => $d['mensaje_whatsapp'],
		'correo'          => $d['correo'],
		'direccion'       => $d['direccion'],
		'direccion2'      => $d['direccion2'],
		'precioPresencial' => $d['precio_presencial'],
		'precioVirtual'    => $d['precio_virtual'],
		'mostrarPrecios'   => true,
		'mostrarPepe'      => true,
		'redes'   => array( 'instagram' => $d['instagram'] ),
		'hotmart' => array(
			'complementaria' => $d['hotmart_complementaria'],
			'lonchera'       => $d['hotmart_lonchera'],
			'habitos'        => $d['hotmart_habitos'],
			'escuela'        => $d['hotmart_escuela'],
		),
	);
}

/**
 * Los campos, agrupados como se leen en la pantalla.
 */
function dalila_campos() {
	return array(
		'contacto' => array(
			'titulo'  => __( 'Contacto', 'dalila' ),
			'ayuda'   => __( 'Aparecen en la portada, en contacto, en el pie y en el botón flotante de WhatsApp.', 'dalila' ),
			'campos'  => array(
				'whatsapp'         => array( __( 'WhatsApp', 'dalila' ), 'text', __( 'Con indicativo, como se quiere ver: +57 304 653 2006', 'dalila' ) ),
				'mensaje_whatsapp' => array( __( 'Mensaje con el que abre WhatsApp', 'dalila' ), 'text', '' ),
				'correo'           => array( __( 'Correo', 'dalila' ), 'email', '' ),
				'direccion'        => array( __( 'Dirección, primera línea', 'dalila' ), 'text', '' ),
				'direccion2'       => array( __( 'Dirección, segunda línea', 'dalila' ), 'text', __( 'Consultorio, ciudad y país.', 'dalila' ) ),
				'instagram'        => array( __( 'Instagram', 'dalila' ), 'url', '' ),
			),
		),
		'tarifas' => array(
			'titulo' => __( 'Tarifas de la consulta', 'dalila' ),
			'ayuda'  => __( 'Se muestran en la portada y en «Citas y tarifas». Escríbelas como se leen, con el signo y los puntos.', 'dalila' ),
			'campos' => array(
				'precio_presencial' => array( __( 'Consulta presencial', 'dalila' ), 'text', '' ),
				'precio_virtual'    => array( __( 'Consulta virtual', 'dalila' ), 'text', '' ),
			),
		),
		'cursos' => array(
			'titulo' => __( 'Enlaces de compra de los cursos', 'dalila' ),
			'ayuda'  => __( 'Mientras un enlace esté vacío, ese botón abre WhatsApp con el nombre del curso ya escrito. Al pegar el enlace de Hotmart, el botón pasa a llevar allí.', 'dalila' ),
			'campos' => array(
				'hotmart_complementaria' => array( __( 'Alimentación complementaria', 'dalila' ), 'url', '' ),
				'hotmart_lonchera'       => array( __( 'Taller Lonchera Nutritiva', 'dalila' ), 'url', '' ),
				'hotmart_habitos'        => array( __( 'El ABC de los hábitos alimentarios', 'dalila' ), 'url', '' ),
				'hotmart_escuela'        => array( __( 'Escuela para padres', 'dalila' ), 'url', '' ),
			),
		),
	);
}

/**
 * Deja la pantalla en el menú de Ajustes.
 */
function dalila_menu_de_ajustes() {
	add_options_page(
		__( 'Datos del consultorio', 'dalila' ),
		__( 'Datos del consultorio', 'dalila' ),
		'manage_options',
		'dalila-datos',
		'dalila_pantalla_de_ajustes'
	);
}
add_action( 'admin_menu', 'dalila_menu_de_ajustes' );

/**
 * Registra la opción y limpia lo que llega del formulario.
 */
function dalila_registrar_ajustes() {
	register_setting(
		'dalila_datos_grupo',
		DALILA_OPCION,
		array(
			'type'              => 'array',
			'sanitize_callback' => 'dalila_limpiar_datos',
			'default'           => dalila_datos_por_defecto(),
		)
	);
}
add_action( 'admin_init', 'dalila_registrar_ajustes' );

/**
 * Cada campo se limpia según lo que es: los enlaces como enlaces, el correo
 * como correo y el resto como texto plano.
 */
function dalila_limpiar_datos( $entrada ) {
	$limpio = array();

	foreach ( dalila_campos() as $grupo ) {
		foreach ( $grupo['campos'] as $clave => $campo ) {
			$valor = isset( $entrada[ $clave ] ) ? $entrada[ $clave ] : '';

			switch ( $campo[1] ) {
				case 'url':
					$limpio[ $clave ] = esc_url_raw( trim( $valor ) );
					break;
				case 'email':
					$limpio[ $clave ] = sanitize_email( $valor );
					break;
				default:
					$limpio[ $clave ] = sanitize_text_field( $valor );
			}
		}
	}

	return $limpio;
}

/**
 * La pantalla.
 */
function dalila_pantalla_de_ajustes() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$datos = dalila_datos();
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'Datos del consultorio', 'dalila' ); ?></h1>
		<p class="description" style="max-width:60ch">
			<?php esc_html_e( 'Lo que se escriba aquí se actualiza de una vez en todo el sitio: la portada, el pie de página, la página de contacto y el botón de WhatsApp.', 'dalila' ); ?>
		</p>

		<form action="options.php" method="post">
			<?php settings_fields( 'dalila_datos_grupo' ); ?>

			<?php foreach ( dalila_campos() as $grupo ) : ?>
				<h2><?php echo esc_html( $grupo['titulo'] ); ?></h2>
				<?php if ( $grupo['ayuda'] ) : ?>
					<p class="description" style="max-width:60ch"><?php echo esc_html( $grupo['ayuda'] ); ?></p>
				<?php endif; ?>

				<table class="form-table" role="presentation">
					<tbody>
					<?php foreach ( $grupo['campos'] as $clave => $campo ) : ?>
						<tr>
							<th scope="row">
								<label for="dalila-<?php echo esc_attr( $clave ); ?>">
									<?php echo esc_html( $campo[0] ); ?>
								</label>
							</th>
							<td>
								<input
									type="<?php echo esc_attr( 'email' === $campo[1] ? 'email' : ( 'url' === $campo[1] ? 'url' : 'text' ) ); ?>"
									id="dalila-<?php echo esc_attr( $clave ); ?>"
									name="<?php echo esc_attr( DALILA_OPCION . '[' . $clave . ']' ); ?>"
									value="<?php echo esc_attr( $datos[ $clave ] ); ?>"
									class="regular-text">
								<?php if ( $campo[2] ) : ?>
									<p class="description"><?php echo esc_html( $campo[2] ); ?></p>
								<?php endif; ?>
							</td>
						</tr>
					<?php endforeach; ?>
					</tbody>
				</table>
			<?php endforeach; ?>

			<?php submit_button( __( 'Guardar los datos', 'dalila' ) ); ?>
		</form>
	</div>
	<?php
}
