<?php 

/**
 * Run file for the python script because I can't get it to work on my evil Apache :)
 * @licence GNU GPL v3+
 * @author Jeroen De Dauw < jeroendedauw@gmail.com >
 */

$args = array();

foreach ( $_GET as $name => $value ) {
	$args[] = escapeshellcmd( $name ) . ' ' . escapeshellcmd( $value );
}

echo shell_exec( 'python src/icalfix.py ' . implode( ' ', $args ) );

?>