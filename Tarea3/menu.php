<?php 
    session_start();

    if(!isset($_SESSION['username'])){
        $_SESSION['msg'] = "You must log in";
        header('location: Login.php');
    }
    if(isset($_GET['logout'])){
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
    <link rel="stylesheet" href="StylesLogo.css">

    <title>Menu :)</title>
    
    <?php if(isset($_SESSION['success'])): ?>
    <?php echo $_SESSION['success'];
        unset($_SESSION['success']);
    ?>
    <?php endif ?>

    <?php 
        if(isset($_SESSION['username'])): ?>
            <strong><?php echo $_SESSION['username'];?></strong>
            <p href="menu.php?logout='1'" style="color: red;">logout</p> 
    <?php endif ?>
</head>
<body>
    <?php include 'globalhead.php';?>
    
</body>
</html>