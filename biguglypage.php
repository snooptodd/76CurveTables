<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-$wrap">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>curve table graphs</title>

</head>
<body>

  <?php

  $sDataPath = 'graphs';
  $aGraph=[];
  $output='';
  $wrap=6;

  function filesIn(string $path, string $name): \Generator
  {
    if (! is_dir($path)) {
        throw new \RuntimeException("{$path} is not a directory ");
    }

    $it = new \RecursiveDirectoryIterator($path);
    $it = new \RecursiveIteratorIterator($it);
    $it = new \RegexIterator($it, '/'.$name.'\.png$/', \RegexIterator::MATCH);

    yield from $it;
  }
  


  $graphs = filesIn($sDataPath,'.*');
  

  foreach ($graphs as $gvalue) {
    $aNames=$gvalue->getBaseName('.'.$gvalue->getExtension());
    $aPath='./'.($gvalue->getPathName());
    $aGraph[$aNames]=$aPath;

  }
  
  ksort($aGraph);
  //echo '';
  // Level 1
  foreach ($aGraph as $Level1Key => $Level1value) {
    //$output.='<h1>'.$Level1Key.'</h1> <table> <thead> <tr> <td> </td> </tr> </thead> <tbody>';
    $output.='<a href="'.$Level1value.'">'. $Level1Key.'</a><br>';

  } // Level 1
  print("$output");
  ?>

</body>
</html>