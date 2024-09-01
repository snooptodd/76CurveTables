<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>curve table graphs</title>

	<!-- Add latest jQuery and fancyBox files -->
<script src="//code.jquery.com/jquery-3.3.1.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.3.5/jquery.fancybox.min.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.3.5/jquery.fancybox.min.js"></script>

<!-- <script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js"></script>
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.css"
/> -->


</head>
<body>
<script>
Fancybox.bind("[data-fancybox]", {
	Toolbar: {
          display: {
            left: [],
            middle: [],
            right: ["close"],
          },
        },

        Images: {
		      initialSize: "max",
          Panzoom: {
            panMode: "mousemove",
            mouseMoveFactor: 1.1,
            mouseMoveFriction: 0.12
          },
		},
});
</script>
<center>

  <?php

  $sDataPath = './graphs/';
  // get list of files in dir
  // loop through the list to create a gallery for fancybox 
  
  // glob works on file system level so the path has to exist and be accessible to the web server. 
  $graphs = glob("$sDataPath/*.png");

  foreach ($graphs as $key => $value) {
    echo '<a 
        data-fancybox="graphs" 
        data-caption="'.$value.'" 
        title="'.$value.'" 
        href="'.$value.'"> 
        <img src="'.$value.'" 
        height="250"> 
        </a> ' ;
  }
  
  ?>
</center>
</body>
</html>