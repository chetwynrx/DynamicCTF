<?php
// Database connection
$servername = "mysqldb";
$username = "root"; // 
$password = "password";
$dbname = "usersdb"; 

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // SQL query to check if the provided username and password match
    $sql = "SELECT * FROM users WHERE username='$username' AND password='$password'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // Login successful, redirect to a logged-in page
        header("Location: logged_in.php");
        exit();
    } else {
        // Invalid username or password
        echo "Invalid username or password.";
    }
}

$conn->close();
?>
