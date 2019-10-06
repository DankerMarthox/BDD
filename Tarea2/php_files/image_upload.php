<?php
  include("database.php");

  // Initialize message variable
  $msg = "";

  // If upload button is clicked ...
  if (isset($_POST['upload'])) {
  	// Get image name
  	$image = $_FILES['image']['name'];
  	// Get text
  	$image_text = pg_escape_string($db_connection, $_POST['image_text']);

  	// image file directory
  	$target = "Tarea3/img/".basename($image);

  	$sql = "INSERT INTO images (image, image_text) VALUES ('$image', '$image_text')";
  	// execute query
  	pg_query($db, $sql);

  	if (move_uploaded_file($_FILES['image']['tmp_name'], $target)) {
  		$msg = "Image uploaded successfully";
  	}else{
  		$msg = "Failed to upload image";
  	}
  }
  $result = pg_query($db_connection, "SELECT * FROM fotos");
?>
<!DOCTYPE html>
<html>
<head>
<title>Image Upload</title>
<link rel="stylesheet" href="/Tarea3/styles/image_header.css">
</head>
<body>


<div id="content" class="form-area">    
	<img class="c-img" src='/TAREA3/img/chaldea_logo.png' float:"left" width="80px">
	<right><h2>Upload an Image!</h2></right>
	<?php
		$description ="";
		while ($row = pg_fetch_array($result)) {
		echo "<div id='img_div'>";
			echo "<img src='/Tarea3/img/".$row['image']."' >";
			echo "<p>".$row['image_text']."</p>";
		echo "</div>";
		}
	?>
	<form method="POST" action="Tarea3/php_files/image_upload.php" enctype="multipart/form-data">
		<input type="hidden" name="size" value="1000000">
		<div>
			<input type="file" name="image">
		  </div>
			<input type="text" name="photo_description" placeholder="lil' description here"                    
				value="<?php echo $description; ?>"><br><br>
		  <div>
			  <button class="btn" type="submit" name="upload">Upload!</button>
		  </div>
		</form>
</div>
</body>
</html>