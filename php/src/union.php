<?php

# for the agent
$new_challenge_type = "union";

# for manual browsing
if (isset($_POST['union'])) {
    echo 'Changed to union challenge';
    $new_challenge_type = "union";
  }

$file = fopen("challenge_type.txt", "w");
fwrite($file, $new_challenge_type);
fclose($file);

header("Location: http://localhost:8000");

?>