<?php
	/*
	* Classe incaricata di leggere dai files csv le posizioni della bounding box della faccia, salvando i valori in una struttura da passare successivamente al js.
	*/
class position{
	var $frame;
	var $x0;
	var $x1;
	var $y0;
	var $y1;
}
	//Controllo il video che sto caricando per poter leggere il giusto file csv.
	$vid = $_GET['vid'];
	$name = explode(".",$vid)[0];
	
	//Open the file.
	$fileHandle = fopen("openface/csv/reduced_".$name.".csv", "r");
	$count = 0;
	$allPositions = array();


	while(($row = fgetcsv($fileHandle,0,",")) != FALSE){
	if($count != 0){
		//echo $row[0] . "<br>";
		$pos = new position();
		$pos->frame = $row[0];
		$pos->x0 = $row[2];
		$pos->x1 = $row[3];
		$pos->y0 = $row[4];
		$pos->y1 = $row[5];
		array_push($allPositions,$pos);
	}
	$count ++;
	$jsonArray = json_encode($allPositions);
	}
	/*foreach($allPositions as $aux){
		echo $aux->frame . " : " . $aux->x0 . "<br>";
	}*/
?>

