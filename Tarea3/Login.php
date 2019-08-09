


<?php include('connect.php') ?>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Instagramn't</title>
        <link rel="stylesheet" href="StylesLogo.css">
    </head>
<body>
    
    <div class="form-area">
        <img class="c-img" src='chaldea_logo.png' float:"left" width="80px">
        <right><h2>Instagramn't</h2></right>
        <form action="/Tarea3/Login.php" method="POST">
            Username:<br>
            <input type="text" name="username" placeholder="Username"><br><br>
            Password:<br>
            <input type="password" name="password" placeholder="Password"><br><br>            
            
            <button class='btn' type="submit" name="login_usr">
            Log-In!
            </button>
        </form>
        <form action="/Tarea3/signUp.php">
            <input type="submit" value="Not Registered? Do it now.">
        </form>
    </div>  
</body>
</html>