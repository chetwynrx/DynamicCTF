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

echo '<form action="" method="post">';
echo 'Name: <input type="text" name="name">';
echo 'E-mail: <input name="email">' ; #dynamic_form
echo '<input type="submit">';
echo '</form>'; 

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  $data = $_REQUEST['email'];

  echo "<br />";

  $string = "Robert";

$data = preg_replace("!-!", "",$data); # comment filter 
$data = preg_replace("!table!", "",$data); # comment filter 
$data = preg_replace("!schema!", "",$data); # comment filter 
$data = preg_replace("!information!", "",$data); # comment filter 
$data = preg_replace("!information_schema.tables!", "",$data); # comment filter 
  #echo $data;


  

if ($result = $conn->query(" SELECT `customerNumber` FROM `customers` WHERE customerNumber = '$data'")) {#dynamic_query    
    
    $row = mysqli_fetch_array($result);

    #echo $row ; 

    if (!empty($row)) {
        $test = implode("<br>", $row) ;
        echo "Database entry exists <br>";
        echo "Returned entry is: <br> " . $test ; 
        
    }
    else
    {
        echo " Database entry does not exist <br>" ; 
    }

    #echo "Database Entry Exists: <br> " . $test ; 

    echo "<br>" ; 

    #$row = mysqli_fetch_row($result) ;

    #$id = $row['postalCode'] ;
    
    #echo $id ; 

    #echo "<b>Name:</b> " . $row['postalCode'] . " ";

    #echo "<b>Name:</b> " . $row['phone'] . " ";

    #echo "<b>Name:</b> " . $row['country'] . " ";

    #echo $result . "<br>" ;

    #echo $row[0] ; 
    
    #$test = implode("<br>", $result) ;

    #echo $test ; 



    #{

    #echo "Result is " . $result . "<br>" ;

    #echo "<b>Name:</b> " . $row['username'] . " ";
  
    #echo "<b>Company: </b>" . $row['password'] . "<br />";

    #echo "<b>Surname: </b>" . $row['flag'] . "<br />";
  
  
  
    #}
  
    #echo "Returned rows are: " . $result -> num_rows;
  
      //Free result set
    #$result -> free_result();
  }
  else {
    printf("Error Message: %s\n", $conn->error);
  }
  
  
}

$conn->close();
?>







