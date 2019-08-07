


<html>
    <head>
        <meta charset="UTF-8">
        <title>Instagramn't</title>
        <link rel="stylesheet" href="StylesMenu.css">
    </head>
<body>

<?php
    require('database.php');

    // initializing variables
    $username = "";
    $password    = "";
    $email    = "";
    $bio    = "";
    $errors = array(); 

    //register user
    if (isset($_POST['reg_user'])){
        $username = pg_escape_string($db_connection,$_POST["username"]);
        $password = pg_escape_string($db_connection,$_POST["password"]);
        $email    = pg_escape_string($db_connection,$_POST["email"]);
        $bio      = pg_escape_string($db_connection,$_POST["bio"]);
        
        //insert only if submit
        $user_reg = "INSERT INTO usuarios (username, email, user_pass) 
                 VALUES ('$username', '$email', '$password');";
        $insert = pg_query($db_connection, $user_reg);
        $user_check_query = "SELECT * FROM usuarios";
        $select = pg_query($db_connection, $user_check_query);
        $val = pg_fetch_all($select);
    print_r($val);  
    }
    //comprobar si campos estan vacios
    //if (empty($username)) { array_push($errors, "Username is required"); }
    //if (empty($email)) { array_push($errors, "Email is required"); }
    //if (empty($password)) { array_push($errors, "Password is required"); }
    
    
?>
</html>