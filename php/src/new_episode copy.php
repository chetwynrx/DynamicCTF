<?php

echo "Generating new episode \n";
### Not the most efficient solution when working with large files but will do for now

$lines = file('query.txt', FILE_IGNORE_NEW_LINES); # Read content of queries.txt as array
$query = $lines[array_rand($lines)]; # Select random value in queries.txt

$php_workaround = file_get_contents('php_query.txt'); # lazy workaround for development will look at a better fix

echo "New SQL Query is: " . "<b>" . $query . "</b>"; # Return new SQL query for debugging (if needed)

#### Modify SQL query in index.php
# Read contents of defined episode as an array                                      ### Edited
$file = 'index.php'; # The episode we want to modify

$content = file($file);

foreach($content as $line) {
    if(strpos($line, "#dynamic_query") !== FALSE) {
        $line = $php_workaround . $query . '")) {' . "#dynamic_query" . "\r\n";
    }
    $newdata[] = $line;
}
$allContent = implode("", $newdata); # convert to string
file_put_contents("index.php", $allContent)

?>

