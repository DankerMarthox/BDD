
<?php
    session_start();
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
        
        //check if empty data
        if (empty($username)) { array_push($errors, "Username is required"); }
        if (empty($email)) { array_push($errors, "Email is required"); }
        if (empty($password)) { array_push($errors, "Password is required"); }
        
        //check if user registered
        $user_chck = "SELECT * from usuarios where username='$username' or email= '$email' limit 1;";
        $chck = pg_query($db_connection, $user_chck);
        $result = pg_fetch_assoc($chck);
        echo pg_query($db_connection, "SELECT * from usuarios;");

        //if registered
        if($result){
            if($result["username"]===$username){
                array_push($errors, "Username already exists");
            }
            if($result["email"]===$email){
                array_push($errors, "Email already exists");
            }
        }
        //if not registered, then do
        if(count($errors)==0){

            $query = "INSERT INTO usuarios (username, email, user_pass, bio) values('$username', '$email', '$password','$bio')";
            pg_query($db, $query);

            $_SESSION['username'] = $username;
            $_SESSION['success'] = "Logged in!";

            header('location: menu.php');
        }
    }
    
    
?>