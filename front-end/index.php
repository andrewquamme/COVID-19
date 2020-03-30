<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!-->
<html class="no-js">
<!--<![endif]-->

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>Covid-19 Visualization</title>
  <meta name="description" content="">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="css/reset.css">
  <link rel="stylesheet" href="css/style.css">
</head>

<body>
  <!--[if lt IE 7]>
      <p class="browsehappy">You are using an <strong>outdated</strong> browser. Please <a href="#">upgrade your browser</a> to improve your experience.</p>
    <![endif]-->
  <div id="content">
    <div id="chart-container">
      <canvas class="graphCanvas"></canvas>
    </div>

    <div id="chart-options">
      <label for="cases">Show Cases</label>
      <input class="cases" type="checkbox" name="cases" value="cases" checked>
      <label for="deaths">Show Deaths</label>
      <input class="deaths" type="checkbox" name="deaths" value="deaths" checked>
      <label for="logarithmic">Logarithmic Scale</label>
      <input class="logarithmic" type="checkbox" name="logarithmic" value="logarithmic">
    </div>

    <div id="state-selection">
      <label for="states">Choose a state:</label>
      <select class="states">
      </select>
    </div>

    <div hidden id="county-selection">
      <label for="counties">Choose a county:</label>
      <select class="counties">
      </select>
    </div>
  </div>

  <script src="js/jquery.min.js"></script>
  <script src="js/Chart.min.js"></script>
  <script src="js/app.js"></script>

</body>

</html>