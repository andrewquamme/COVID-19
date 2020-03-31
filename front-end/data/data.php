<?php
header('Content-Type: application/json');
require_once('db.php');

$query = $_GET["query"];
$state = $_GET["state"];
$county = $_GET["county"];

switch ($query) {
	case "getStates":
		$sqlQuery = "
			SELECT DISTINCT state
			FROM states
			ORDER BY state";
		break;
	case "getCounties":
		$sqlQuery = "
			SELECT DISTINCT county
			FROM counties
			WHERE state = '{$state}'
			ORDER BY county";
		break;
	case "getData":
		if ($state == "United States") {
			$sqlQuery = "
			SELECT date, cases, deaths
			FROM usa
			ORDER BY date";
		} elseif ($state == "Veterans Affairs") {
			$sqlQuery = "
				SELECT date, cases, deaths
				FROM veterans
				ORDER BY date";
		} elseif ($county == "") {
			$sqlQuery = "
				SELECT date, cases, deaths
				FROM states
				WHERE state = '{$state}'
				ORDER BY date";
		} else {
			$sqlQuery = "
				SELECT date, cases, deaths
				FROM counties
				WHERE county = '{$county}'
				AND state = '{$state}'
				ORDER BY date";
		}
		break;
}

$result = mysqli_query($conn,$sqlQuery);

$data = array();
foreach ($result as $row) {
	$data[] = $row;
}

mysqli_close($conn);

echo json_encode($data);
?>