<?php
if(isset($_COOKIE['TestCookie']))
{
$test = $_COOKIE['TestCookie'];
echo "Welcome back! <br> You last visited on ". $test;
echo "Updating challenge on " . $test;
}
else
{
echo "Welcome to our site!";
}
?>