<?php 
    session_start();

    if(!isset($_SESSION['username'])){
        $_SESSION['msg'] = "You must log in";
        header('location: signUp.php');
    }
    if(!isset($_SESSION['logout'])){
        session_destroy();
        unset($_SESSION['username']);
        header("location: Login.php");
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Menu :)</title>
    <?php 
        if(isset($_SESSION['success'])): ?>
    IT WORKED
</head>
<body>
</body>
</html>