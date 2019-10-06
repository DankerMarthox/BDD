


<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<title>Instagramn't</title>
	<link rel="stylesheet" href=" /Tarea3/styles/StylesLogo.css">
</head>

<body>
	<?php  if (count($errors) > 0) : ?>
	<div class="error">
		<?php foreach ($errors as $error) : ?>
		<?php echo $error?>!<br>
		<?php endforeach ?>
	</div>
	<?php  endif ?>	
</body>
</html>

