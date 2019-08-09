<?php 
    session_start();

    if(!isset($_SESSION['username'])){
        $_SESSION['msg'] = "You must log in";
        header('location: /Tarea3/php_files/Login.php');
    }
    if(isset($_GET['logout'])){
        session_destroy();
        unset($_SESSION['username']);
        header("location: /Tarea3/php_files/Login.php");
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <?php include "globalhead.php";
            include "database.php";?>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href=" /Tarea3/styles/image_header.css">

    <title>Menu :)</title>
    
    <?php if(isset($_SESSION['success'])): ?>
    <?php echo $_SESSION['success'];
        unset($_SESSION['success']);
    ?>
    <?php endif ?>
</head>
    	
<body>
    <?php 
        $d=$_SESSION['username'];
        $bioD = pg_query($db_connection, "SELECT bio from usuarios where username='$d' limit 1");
    ?>
    <p style=><?php echo pg_fetch_array($bioD, 0, PGSQL_ASSOC)["bio"]?></p>
    <div class="form-area-images">
        <form action="image_upload.php">
            <input type="submit" value="Upload an image????">
        </form>
    </div>  

</body>
</html>