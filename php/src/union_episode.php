<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

echo "Hello World Test - Union";

echo "<br />";


echo "<br />";

//These are the defined authentication environment in the db service

// The MySQL service named in the docker-compose.yml.

$host = 'mysqldb';

// Database use name

$user = 'root';

//database user password

$pass = 'password';

// database name

$mydatabase = 'example';

// check the mysql connection status

$conn = new mysqli($host, $user, $pass, $mydatabase);

if ($conn-> connect_errno) {
  echo "Failed to connect to MySQL: " . $conn -> connect_error;
  exit();
}

echo '<form action="episode1.php" method="post">';
echo 'Name: <input type="text" name="name">';
echo 'E-mail: <input type="text" name="email">' ;
echo '<input type="submit">';
echo '</form>'; 

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  $data = $_REQUEST['name'];

  echo $data;

  echo "<br />";

  $string = "Robert";


  if ($result = $conn->query("SELECT name, company FROM customers where surname = '$data' UNION SELECT username, password FROM users WHERE surname = '$data'")) {

    echo "<br/>";
    
    while($row = mysqli_fetch_array($result))

    {
  
    ### HERE YOU CAN CHANGE THE NAME OF THE RETURNED HTML COLUMNS ON THE PAGE
    echo "<b>Name:</b> " . $row['name'] . " ";
  
    echo "<b>Company: </b>" . $row['company'] . "<br />";
  
  
  
  
    }
  
    echo "Returned rows are: " . $result -> num_rows;
  
      //Free result set
    #$result -> free_result();
  }
  else {
    printf("Error Message: %s\n", $conn->error);
  }
  
  
}

$conn->close();
?>







