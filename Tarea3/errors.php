


<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<title>Instagramn't</title>

</head>

<body>
	<?php  if (count($errors) > 0) : ?>
	<div class="error">
		<?php foreach ($errors as $error) : ?>
		<p><?php echo $error ?></p>
		<?php endforeach ?>
	</div>
	<?php  endif ?>	
</body>
</html>

