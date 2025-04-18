<?php
  // create sub pages with json files printed.
  

  $sDataPath = 'graphs';
  $live='./json/Live_P58';
  $pts='./json/PTS_P60_11apr';
  
  $aGraph=[];
  $output='';
  $wrap=6;
  // $pagename='Curve Table Graphs';
  // $htmlheader='<!DOCTYPE html> <html lang="en"> 
  // <head> 	<meta charset="utf-8"> 	<meta name="viewport" content="width=device-width, initial-scale=1"> 	
  // <title>'.$pagename.'</title> 
  // <link rel="stylesheet" href="/76CurveTables/styles.css"> </head> <body>';
  $htmlfooter='</body> </html>';

  function filesIn(string $path, string $name): \Generator
  {
    if (! is_dir($path)) {
        throw new \RuntimeException("{$path} is not a directory ");
    }

    $it = new \RecursiveDirectoryIterator($path);
    $it = new \RecursiveIteratorIterator($it);
    $it = new \RegexIterator($it, '/'.$name.'/', \RegexIterator::MATCH);

    yield from $it;
  }
  
  function htmlheader(string $pagename) {
    return '<!DOCTYPE html> <html lang="en"> 
  <head> 	<meta charset="utf-8"> 	<meta name="viewport" content="width=device-width, initial-scale=1"> 	
  <title>'.$pagename.'</title> 
  <link rel="stylesheet" href="/76CurveTables/styles.css"> </head> <body>';
  }

  $graphs = filesIn($sDataPath,'.*\.png');
  foreach ($graphs as $gvalue) {
    $aNames=$gvalue->getBaseName('.'.$gvalue->getExtension());
    $aPath='./'.($gvalue->getPathName());
    $aGraph[$aNames]=$aPath;

  }
  
  $output=htmlheader('Curve Table Graphs');
  ksort($aGraph);
  
  // Level 1
  foreach ($aGraph as $Level1Key => $Level1value) {
    //$output.='<h1>'.$Level1Key.'</h1> <table> <thead> <tr> <td> </td> </tr> </thead> <tbody>';
    $filename=$Level1Key;
    $subfile=str_replace('png','html',$Level1value);
    $subdata=htmlheader($filename);
    $count=1;
    $output.='<a href="'.$subfile.'">'.$filename.'</a><p>';
    $subdata.='<img src="'.$filename.'.png"><p>';
    foreach (filesIn($pts,'.*'.$filename.'\.json') as $jsonkey => $jsonvalue) {
      // key is path and file
      $jsondata=json_decode(file_get_contents($jsonkey),TRUE);
      $txtdata='';
      foreach ($jsondata["curve"] as $jsondatakey => $jsondatavalue) {
        $txtdata.='x = '.$jsondatavalue['x'].', y = '.$jsondatavalue['y']."<br>";
      }

      $subdata.= '<label for="pts'.$count.'">'.$jsonkey.'</label><br>';
      $subdata.= '<div class="box" id="pts'.$count.'">'.$txtdata.'</div>';
      $count+=1;
    }
    $subdata.='<p>';
    $count=1;
    foreach (filesIn($live,'.*'.$filename.'\.json') as $jsonkey => $jsonvalue) {
      $jsondata=json_decode(file_get_contents($jsonkey),TRUE);
      $txtdata='';
      foreach ($jsondata["curve"] as $jsondatakey => $jsondatavalue) {
        $txtdata.='x = '.$jsondatavalue['x'].', y = '.$jsondatavalue['y']."<br>";
      }
     
      $subdata.= '<label for="live'.$count.'">'.$jsonkey.'</label><br>';
      $subdata.= '<div class="box" id="live'.$count.'">'.$txtdata.'</div>';
      $count+=1;
    }
    $subdata.=$htmlfooter;
    file_put_contents($subfile,$subdata);

  } // Level 1
  // print("$output");
  $output.=$htmlfooter;
  $index = fopen("index.html","w") or die("unable to open index.html");
  fwrite($index,$output);
  fclose($index);
?>