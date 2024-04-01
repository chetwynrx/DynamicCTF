<?php

$cookie_name = "TestCookie" ;
$cookie_value = basename(__FILE__); 

setcookie($cookie_name, $cookie_value) ;
 
echo $cookie_name;
echo "<br>" ;
echo $cookie_value;

?>