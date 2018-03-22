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
class expertValue{
	var $frame;
	var $value;
}
	//Controllo il video che sto caricando per poter leggere il giusto file csv.
	$vid = $_GET['vid'];
	$type = $_GET['type'];
	$name = explode(".",$vid)[0];
	
	//Apro il file contenente i valori posizione della bounding box.
	if(file_exists("openface/csv/reduced_".$name.".csv")){
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
			$jsonArrayPosition = json_encode($allPositions);
		}
	}else {
		echo "Openface file does not exist.<br>";
	}

	//Apro il file degli esperti corrispondente, se esiste.
	if(file_exists("annotation/expert/expert_".$type."_".$name.".csv")){
		$fileHandle = fopen("annotation/expert/expert_".$type."_".$name.".csv", "r");
		$count = 0;
		$allExpertValue = array();


		while(($row = fgetcsv($fileHandle,0,";")) != FALSE){
			if($count != 0){
				//echo $row[2] . "<br>";
				$expert = new expertValue();
				$expert->frame = $row[0];
				$expert->value = $row[2];
			
				array_push($allExpertValue,$expert);
			}
			$count ++;
			$jsonArrayExpert = json_encode($allExpertValue);
		}
	}else{
		$jsonArrayExpert = null;
		echo "Expert file does not exist.<br>";
	}
?>

