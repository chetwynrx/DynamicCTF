<?php 

# for the agent
$new_challenge_type = "bool";

# for manual browsing

if (isset($_POST['bool'])) {
  echo 'Changed to bool challenge';
  $new_challenge_type = "bool";
}

$file = fopen("challenge_type.txt", "w");
fwrite($file, $new_challenge_type);
fclose($file);

header("Location: http://localhost:8000/");

?>