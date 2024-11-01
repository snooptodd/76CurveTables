<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-$wrap">
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

<style>
  table {
  background: auto;
  width: auto;
  }
  width {
    width: 250;
  }

</style>

</center>

  <?php

  $sDataPath = './graphs';
  $aGraph=[];
  $output='';
  $wrap=6;

  function fancyboxEntry($group,$name,$link) {
    //$output='<div style="width: min-content;"> <a data-fancybox="'.$group.'" data-caption="'.$name.'" title="'.$name.'" href="'.$link.'"> <img src="'.$link.'" height="250"> '.$name.' </a> </div>' ;
    $output='<a data-fancybox="'.$group.'" data-caption="'.$name.'" title="'.$name.'" href="'.$link.'"> <img src="'.$link.'" height="250"> </a> <p> <center> '.$name.' </center> </p>' ;
    return $output; 
  }

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
  
  function nothingElseWorks($faPath,$faNames,$pathName) {
    $faGraph = array();
    switch (count($faNames)) {
      case 7:
        $faGraph[$faPath[1]][$faNames[0]][$faNames[1]][$faNames[2]][$faNames[3]][$faNames[4]][$faNames[5]][$faNames[6]]=$pathName;
      case 6:
        $faGraph[$faPath[1]][$faNames[0]][$faNames[1]][$faNames[2]][$faNames[3]][$faNames[4]][$faNames[5]]=$pathName;
      case 5:
        $faGraph[$faPath[1]][$faNames[0]][$faNames[1]][$faNames[2]][$faNames[3]][$faNames[4]]=$pathName;
        break;
      case 4:
        $faGraph[$faPath[1]][$faNames[0]][$faNames[1]][$faNames[2]][$faNames[3]]=$pathName;
        break;
      case 3:
        $faGraph[$faPath[1]][$faNames[0]][$faNames[1]][$faNames[2]]=$pathName;
        break;
      case 2:
        $faGraph[$faPath[1]][$faNames[0]][$faNames[1]]=$pathName;
        break;
      default:
        # code...
        break;
    }
    return $faGraph;
  }
  // get list of files in dir
  // loop through the list to create a gallery for fancybox 
  // the list of files is big and ugly and i dont understand how to put names on fancybox thumbnails. 
  // so lets create a page for the graphs by enemy
  
  // glob works on file system level so the path has to exist and be accessible to the web server. 
  // $graphs = glob("./$sDataPath/*.png");
  $graphs = filesIn($sDataPath,'.*');

  // foreach ($graphs as $ggetPathName => $gvalue) {
  foreach ($graphs as $gvalue) {
    // split the pile into chunks. by race. ./graphs/armor_alien_cold.png
    $aNames=explode('_',$gvalue->getBaseName('.'.$gvalue->getExtension()));
    $aPath=explode('/',$gvalue->getPath());
    // create an array with the [race] [subrace]? [type] [damagetype] = graph
    if (count($aNames)>7) {
      //continue;
      throw new Exception("more than 7 getPathNames in aNames", 1);      
    }
    switch ($aPath[1]) {
      case 'creatures':
        switch ($aNames[0]) {
          case 'health':
            if (count($aNames)==2) {
              $aGraph[$aPath[1]][$aNames[1]][$aNames[0]]=$gvalue->getPathName();
            } else {
              $aGraph[$aPath[1]][$aNames[1].'-'.$aNames[2]][$aNames[0]]=$gvalue->getPathName();
            }
            break;
          case 'armor':
            if (count($aNames)==3) {
              $aGraph[$aPath[1]][$aNames[1]][$aNames[0]][$aNames[2]]=$gvalue->getPathName();
            } else {
              $aGraph[$aPath[1]][$aNames[1].'-'.$aNames[2]][$aNames[0]][$aNames[3]]=$gvalue->getPathName();
            }
            break;
          case 'weapon':
            if (count($aNames)==2) {
              $aGraph[$aPath[1]][$aNames[1]][$aNames[0]]=$gvalue->getPathName();
            } elseif (count($aNames)==3) {
              $aGraph[$aPath[1]][$aNames[1]][$aNames[0]][$aNames[2]]=$gvalue->getPathName();
            } elseif (count($aNames)==4) {
              $aGraph[$aPath[1]][$aNames[1].'-'.$aNames[2]][$aNames[0]][$aNames[3]]=$gvalue->getPathName();
            } elseif (count($aNames)==5) {
              $aGraph[$aPath[1]][$aNames[1].'-'.$aNames[2].'-'.$aNames[3]][$aNames[0]][$aNames[4]]=$gvalue->getPathName();
            } else {
              $aGraph = array_merge_recursive($aGraph, nothingElseWorks($aPath,$aNames,$gvalue->getPathName()));
            }
            break;
          default:
            $aGraph = array_merge_recursive($aGraph, nothingElseWorks($aPath,$aNames,$gvalue->getPathName()));
        }
        break;
      case '':
        break;
      default:
      $aGraph = array_merge_recursive($aGraph, nothingElseWorks($aPath,$aNames,$gvalue->getPathName()));
    }
  }
  //   <table>
  //   <thead>
  //     <tr>Alien </tr>
  //   </thead>
  //   <tbody>
  //     <tr>
  //       <td>HTML tables</td>
  //       <td>22</td>
  //     </tr>
  //     <tr>
  //       <td>Web accessibility</td>
  //       <td>45</td>
  //     </tr>
  //     <tr>
  //       <td>JavaScript frameworks</td>
  //       <td>29</td>
  //     </tr>
  //     <tr>
  //       <td>Web performance</td>
  //       <td>36</td>
  //     </tr>
  //   </tbody>
  // </table>
  
  ksort($aGraph);
  //echo '';
  // Level 1
  foreach ($aGraph as $Level1Key => $Level1value) {
    //$output.='<h1>'.$Level1Key.'</h1> <table> <thead> <tr> <td> </td> </tr> </thead> <tbody>';
    
    // Level 2
    foreach ($Level1value as $Level2Key => $Level2value) {
      $i=0;
      $output.='<h1>'.$Level1Key.' '.$Level2Key.'</h1> <table> <thead> <tr> <td> </td> </tr> </thead> <tbody>';
      $output.='<tr>';
      if (is_string($Level2value)) {
        $name=$Level2Key;
        $output.='<td>'.fancyboxEntry($Level3Key,$name,$Level2value).'</td>';
        $i+=1;
        if ( $i >= $wrap ) {
          $output.='</tr><tr>';
          $i=0;
        }
        continue;
      } 
        // Level 3
        foreach ($Level2value as $Level3Key => $Level3value) {
          if (is_string($Level3value)) {
            $name=$Level2Key.' '.$Level3Key;
            $output.='<td>'.fancyboxEntry($Level3Key,$name,$Level3value).'</td>';
            $i+=1;
            if ( $i >= $wrap ) {
              $output.='</tr><tr>';
              $i=0;
            }
            continue;
          }
          //Level 4
          foreach ($Level3value as $Level4key => $Level4value) {
            if (is_string($Level4value)) {
              $name=$Level2Key.' '.$Level3Key.' '.$Level4key;
              $output.='<td>'.fancyboxEntry($Level3Key,$name,$Level4value).'</td>';
              $i+=1;
              if ( $i >= $wrap ) {
                $output.='</tr><tr>';
                $i=0;
              }
              continue;
              }
            //Level 5
            foreach ($Level4value as $Level5key => $Level5value) {
              if (is_string($Level5value)) {
                $name=$Level2Key.' '.$Level3Key.' '.$Level4key.' '.$Level5key;
                $output.='<td>'.fancyboxEntry($Level3Key,$name,$Level5value).'</td>';
                $i+=1;
                if ( $i >= $wrap ) {
                  $output.='</tr><tr>';
                  $i=0;
                }
                continue;
                }
              //Level 6
              foreach ($Level5value as $Level6key => $Level6value) {
                if (is_string($Level6value)) {
                  $name=$Level2Key.' '.$Level3Key.' '.$Level4key.' '.$Level5key.' '.$Level6key;
                  $output.='<td>'.fancyboxEntry($Level3Key,$name,$Level6value).'</td>';
                  $i+=1;
                  if ( $i >= $wrap ) {
                    $output.='</tr><tr>';
                    $i=0;
                  }
                  continue;
                  }
                //Level 7
                foreach ($Level6value as $Level7key => $Level7value) {
                  if (is_string($Level7value)) {
                    $name=$Level2Key.' '.$Level3Key.' '.$Level4key.' '.$Level5key.' '.$Level6key;
                    $output.='<td>'.fancyboxEntry($Level3Key,$name,$Level7value).'</td>';
                    $i+=1;
                    if ( $i >= $wrap ) {
                      $output.='</tr><tr>';
                      $i=0;
                    }
                    continue;
                    }
                  //Level 8
                  foreach ($Level7value as $Level8key => $Level8value) {
                    if (is_string($Level8value)) {
                      $name=$Level2Key.' '.$Level3Key.' '.$Level4key.' '.$Level5key.' '.$Level6key.' '.$Level7key;
                      $output.='<td>'.fancyboxEntry($Level3Key,$name,$Level8value).'</td>';
                      $i+=1;
                      if ( $i >= $wrap ) {
                        $output.='</tr><tr>';
                        $i=0;
                      }
                      continue;
                      }
                  } // level 8
                } // level 7
              } // level 6
            } // level 5
          } // level 4
        } // Level 3 
      $output.='</tr></tbody></table>
';
    } // Level 2
    $output.='';
  } // Level 1
  print("$output");
  ?>

</center>
</body>
</html>