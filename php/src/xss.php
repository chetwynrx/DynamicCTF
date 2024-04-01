<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XSS Capture The Flag Challenge</title>
</head>
<body>
    <h1>XSS Capture The Flag Challenge</h1>
    
    <!-- Challenge 1: Reflected XSS -->
    <h2>Challenge 1: Reflected XSS</h2>
    <p>Search for a product:</p>
    <form action="xss.php" method="GET">
        <input type="text" name="search" id="search">
        <input type="submit" value="Search">
    </form>
    <?php
        if(isset($_GET['search'])){
            echo "<p>Search results for: " . $_GET['search'] . "</p>";
        }
    ?>

    <!-- Challenge 2: Stored XSS -->
    <h2>Challenge 2: Stored XSS</h2>
    <p>Leave a comment:</p>
    <form action="xss.php" method="POST">
        <textarea name="comment" id="comment" rows="4" cols="50"></textarea><br>
        <input type="submit" value="Submit Comment">
    </form>
    <?php
        if(isset($_POST['comment'])){
            echo "<div id='comments'><p>" . $_POST['comment'] . "</p></div>";
        }
    ?>

    <!-- Challenge 3: DOM-based XSS -->
    <h2>Challenge 3: DOM-based XSS</h2>
    <p>Click on a category:</p>
    <ul id="categories">
        <li><a href="#">Category 1</a></li>
        <li><a href="#">Category 2</a></li>
        <li><a href="#">Category 3</a></li>
    </ul>
    <div id="result"></div>
    <script>
        // Vulnerable JavaScript code for Challenge 3: DOM-based XSS
        document.getElementById('categories').addEventListener('click', function(event) {
            const category = event.target.innerText;
            document.getElementById('result').innerHTML = '<p>Displaying results for category: ' + category + '</p>';
        });
    </script>
</body>
</html>
