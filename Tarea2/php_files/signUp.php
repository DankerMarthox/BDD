
<?php include('connect.php') ?>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Sign Up!</title>
        <link rel="stylesheet" href="/TAREA3/styles/StylesLogo.css">
    </head>
<body>
    <div class="form-area-register">    
        <img class="c-img" src='/TAREA3/img/chaldea_logo.png' float:"left" width="80px">
        <right><h2>Instagramn't<br>Sign Up!</h2></right>

        <form action="/TAREA3/php_files/signUp.php" method="POST">
            <?php include('errors.php'); ?>
            Username:<br>
            <input type="text" name="username" placeholder="Username" 
                    value="<?php echo $username; ?>"><br><br>
            Password:<br>
            <input type="password" name="password" placeholder="Password"                    
                    value="<?php echo $password; ?>"><br><br>
            Short biography of you:<br>
            <input type="text" name="bio" placeholder="Brief description of you"                    
                    value="<?php echo $bio; ?>"><br><br>
            Your E-mail:<br>
            <input type="text" name="email" placeholder="your email address goes here"                    
                    value="<?php echo $email; ?>"><br><br>
        
            <button type="submit" class="btn" name="reg_user">Submit!</button>
        
            Already a member? <a href="/TAREA3/php_files/Login.php">Sign in</a> 
        </form>
    </div>
</body>
</html>