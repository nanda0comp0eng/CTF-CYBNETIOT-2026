<?php
$host = @getenv('DB_HOST') ?: 'db';
$db = @getenv('DB_NAME') ?: 'movie_db';
$user = @getenv('DB_USER') ?: 'user';
$pass = @getenv('DB_PASS') ?: 'password';

$conn = mysqli_connect($host, $user, $pass, $db);

if (!$conn) {
     die("Connection failed: " . mysqli_connect_error());
}
?>