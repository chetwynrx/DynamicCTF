<?php

#ini_set('display_errors', 1);
#ini_set('display_startup_errors', 1);
#error_reporting(E_ALL);

echo "Welcome";
echo "<br />";

//These are the defined authentication environment in the db service

$host = 'mysqldb';

$user = 'root';

//database user password

$pass = 'password';

// database name

$mydatabase = 'classicmodels';

// check the mysql connection status

$conn = new mysqli($host, $user, $pass, $mydatabase);

#if ($conn-> connect_errno) {
#  echo "Failed to connect to MySQL: " . $conn -> connect_error;
# exit();
#}

echo '<form action="index.php" method="post">';
echo 'Name: <input type="text" name="name">';
echo 'E-mail: <input name="email">' ; #dynamic_form
echo '<input type="submit">';
echo '</form>'; 

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  $data = $_REQUEST['email'];

  echo "<br />";

  $string = "Robert";

  $data = preg_replace('!#!', '',$data); # comment filter 

  echo $data;




if ($result = $conn->query(" SELECT `phone`, `country`, `addressLine1` FROM `offices` WHERE postalCode = '$data'")) {#dynamic_query    
    while($row = mysqli_fetch_array($result))

    {

    
    echo "<b>Name:</b> " . $row['username'] . " ";
  
    echo "<b>Company: </b>" . $row['password'] . "<br />";

    echo "<b>Surname: </b>" . $row['flag'] . "<br />";
  
  
  
    }
  
    echo "Returned rows are: " . $result -> num_rows;
  
      //Free result set
    #$result -> free_result();
  }
  #else {
  #  printf("Error Message: %s\n", $conn->error);
  #}
  
  
}

$conn->close();
?>







