<?php 


$dbfile = fopen("dbname.txt","r");
$dbname = fgets($dbfile);
fclose($dbfile);

$location = "/var/www/html/$dbname";

$host = 'mysqldb';

$user = 'root';

//database user password

$pass = 'password';

// database name

$mydatabase = 'example';

// check the mysql connection status

$conn = new mysqli($host, $user, $pass, $mydatabase);


$commands = file_get_contents($location);   
$test = $conn->multi_query($commands);

$test

?> 