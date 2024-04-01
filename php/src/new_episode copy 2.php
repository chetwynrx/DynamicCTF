<?php

echo "Generating new episode \n";
### Not the most efficient solution when working with large files but will do for now

$lines = file('query.txt', FILE_IGNORE_NEW_LINES); # Read content of queries.txt as array
$query = $lines[array_rand($lines)]; # Select random value in queries.txt

echo "<br>" ;

echo $query ;

echo "<br>" ;

$php_workaround = file_get_contents('php_query.txt'); # lazy workaround for development will look at a better fix

echo "New SQL Query is: " . "<b>" . $query . "</b>"; # Return new SQL query for debugging (if needed)

#### Modify SQL query in index.php
# Read contents of defined episode as an array                                      ### Edited
$file = 'index.php'; # The episode we want to modify

$content = file($file);

foreach($content as $line) {
    if(strpos($line, "#dynamic_query") !== FALSE) {
        #$line = $php_workaround . $query . '")) {' . "#dynamic_query" . "\r\n";
        $line = $php_workaround . $query . '")) {' . "#dynamic_query";
    }
    $newdata[] = $line;
}
$allContent = implode("", $newdata); # convert to string
file_put_contents("index.php", $allContent);



################# TESTING API
echo "I am testing the new python file: ";

$wd = getcwd();

echo $wd . "Yes" ; 

$command_exec = escapeshellcmd("python3 /var/www/html/sql_gen.py");
$str_output = shell_exec($command_exec);

echo "<br/>" ; 

echo "DOES IT WORK: New SQL Query is: " . "<b>" . $query . "</b>"; # Return new SQL query for debugging (if needed)

#$fh = opendir(getcwd());
#while (($entry = readdir($fh)) !== false) { echo $entry; }
#fclose($fh);



?>

