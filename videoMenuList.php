<?php
    $video = Model::getVideoByUsrId($id);

    while($row = mysqli_fetch_array($video)){
		if($row['name'] == "Example.mp4"){
			echo 
          '<li>'
            . '<a href="index.php?id='.$id.'&vid='.$row['name'].'&type=example">'
            . (Model::doesAnnotationExist($id,$row['name'],'arousal') ?  
              '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span> ' :
              '<span class="glyphicon glyphicon-unchecked" aria-hidden="true"></span> ')
            . $row['name'] . '</a>'
        . '</li>';
		}else{
			echo 
          '<li>'
            . '<a href="index.php?id='.$id.'&vid='.$row['name'].'&type=arousal">'
            . (Model::doesAnnotationExist($id,$row['name'],'arousal') ?  
              '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span> ' :
              '<span class="glyphicon glyphicon-unchecked" aria-hidden="true"></span> ')
            . $row['name'] . ' - Arousal </a>'
        . '</li>'
        . '<li>'
            . '<a href="index.php?id='.$id.'&vid='.$row['name'].'&type=valence">'
            . (Model::doesAnnotationExist($id,$row['name'],'valence') ?  
              '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span> ' :
              '<span class="glyphicon glyphicon-unchecked" aria-hidden="true"></span> ')
            . $row['name'] . ' - Valence </a>'
        . '</li>'
		;
		} 
    }
?>
