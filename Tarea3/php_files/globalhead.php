<!DOCTYPE html>
<html>

<head>
    <title>My Page</title>
</head>

<style>
    body {
    padding:10px;
    text-align: center;
    }

    header{
    padding: 40px;
    background: #3cc7e5;
    }

    usr{
    position:relative;
    display: inline-block;
    top:-100px;
    left: 560px;
    }

    tit {
    display:inline-block;
    transform:translate(-15%,-50%);
    color: white;
    font-size: 50px;
    }

    link{
    font-size: 20px;
    color: white;
    }

    side{
    position:relative;
    text-align:center
    }
    img{
    display: inline-block;
    border-radius: 100%;
    position: relative;
    right: 120px;
    width: 100px;
    }

    span {
    background: #fd0;
    }
</style>


<header>  
  <img src=http://vectips.com/wp-content/uploads/2017/03/project-preview-large-2.png>
  
  <tit>Instagramn't</tit>

  <side>
    <div class="topnav">
    <a class="active" href="#home" style="color: white">Inicio</a>
    <a href="#perfil" style="color: white">Perfil</a>
    <input type="text" placeholder="Usuario...">
    <input type="text" placeholder="Hashtag...">
    </div>
  </side>

</header>

<body><br>
  <h1 style=><?php echo $_SESSION['username']?></h1>    
</body>
</html>