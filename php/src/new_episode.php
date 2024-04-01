<?php

#$time_start = microtime(true);

$wd = getcwd();

$host = 'mysqldb';

$user = 'root';

//database user password

$pass = 'password';

$mydatabase = "classicmodels";


### Read the dbname.txt file so we know what database to reset
$remove_file = fopen("/var/www/html/remove_row.txt","r");
$remove_file_query = fgets($remove_file);
fclose($remove_file);

echo $remove_file_query . "<br>";

$conn = new mysqli($host, $user, $pass, $mydatabase);


### Filename for database to reset
#$location = "/var/www/html/$dbname";

### Get the name of the db in the dbname text file
### This resets the database using the multi_query reading the contents of the .sql file 
#$commands = file_get_contents($location);   
$flag_reset = $remove_file_query;

### Reset the flag based on the above
#$flag_reset;

if ($conn->query($flag_reset) === TRUE) {
    echo "Record deleted successfully <br>";
  } else {
    echo "Error deleting record: " . $conn->error;
  }
  
$conn->close();

echo "Removing previous flag from DB <br>";

#echo "Waiting 5 seconds to complete <br>";
#sleep(5) ;


### COOKIE TESTING
#print_r($_COOKIE) ; 

#file_put_contents("/var/www/html/cookies.txt", $_COOKIE['agent_id'] . "\n", FILE_APPEND);

#if($_COOKIE['client_id'] != '1') {
#    header("Location: index_0.php");
#    exit;
#}

#echo $wd . "Yes" ; 

### Run the SQL Query Generator script locally on the server
$command_exec = escapeshellcmd("python3 /var/www/html/sql_gen.py");
$str_output = shell_exec($command_exec);

echo "<br> " ;

echo $str_output ;

echo "<br> " ;

### Comment Delimiter Filtering
$hashComment = '$data = preg_replace("!§!", "",$data); # comment filter ';
$dashComment = '$data = preg_replace("!§!", "",$data); # comment filter ';
$multiComment = '$data = preg_replace("!§!", "",$data); # comment filter ';
$commentArray = array($hashComment, $dashComment, $multiComment);

$rand_keys = array_rand($commentArray, 2);

$tmpfile = "index.tmp" ;
echo "<br> " ;
echo " Generating new episode";
### Not the most efficient solution when working with large files but will do for now

$lines = file('query.txt', FILE_IGNORE_NEW_LINES); # Read content of queries.txt as array
$query = $lines[array_rand($lines)]; # Select random value in queries.txt

echo "<br> <br>" ;

$php_workaround = file_get_contents('php_query.txt'); # lazy workaround for development will look at a better fix

$columns_to_use = file_get_contents('columns.txt');
#$column_content = implode("", $columns_to_use); # convert to string

echo "<b>New SQL Query is: </b> <br/>" . $query ; # Return new SQL query for debugging (if needed)

###### WRITE QUERY TO FILE FOR PERFORMANCE TESTING
$collated_query_file = fopen("/var/www/html/collated_queries.txt", "a");
$collated_query = $query . "\n";
fwrite($collated_query_file, $collated_query);

#### Modify SQL query in index.php
# Read contents of defined episode as an array                                      ### Edited
$file = 'index.tmp'; # The episode we want to modify

$content = file($file);


foreach($content as $line) {
    if(strpos($line, "#dynamic_query") !== FALSE) {
        #$line = $php_workaround . $query . '")) {' . "#dynamic_query" . "\r\n";
        $line = $php_workaround . $query . '")) {' . "#dynamic_query";
    }
    if(strpos($line, "# comment filter") !== FALSE) {
        #$line = $php_workaround . $query . '")) {' . "#dynamic_query" . "\r\n";
        $line = $commentArray[$rand_keys[0]];
    }
    if(strpos($line, "#field-to-replace") !== FALSE) {
      #$line = $php_workaround . $query . '")) {' . "#dynamic_query" . "\r\n";
      $line = $columns_to_use;
  }
    $newdata[] = $line;
}

$allContent = implode("", $newdata); # convert to string
file_put_contents("index.php", $allContent);




################# TESTING API
#echo "I am testing the new python file: ";

#echo "<br/>" ; 

#echo "DOES IT WORK: New SQL Query is: " . "<b>" . $query . "</b>"; # Return new SQL query for debugging (if needed)

#$fh = opendir(getcwd());
#while (($entry = readdir($fh)) !== false) { echo $entry; }
#fclose($fh);

#$time_end = microtime(true);

#$execution_time = ($time_end - $time_start);


#echo '<br> <br> <b>API Total Execution Time:</b> '.$execution_time.' secs';

?>

