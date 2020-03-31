'use strict';

var chart;

function populateStates() {
  $.get("./data/data.php", { query: "getStates"}, function (data) {

    var stateSel = $(".states").empty();
    stateSel.append($('<option/>').html("--United States--").val("United States"));
    stateSel.append($('<option/>').html("--Veterans Affairs--").val("Veterans Affairs"));
    for (var i in data){
      stateSel.append($('<option/>').html(data[i].state).val(data[i].state));
    }
  }); 
}

function populateCounties(state) {
  $.get("./data/data.php", {query: "getCounties",
                            state: state}, function(data) {

    var countySel = $(".counties");
    countySel.empty();
    if (data.length > 0) {
      countySel.append($('<option/>').html(`--${state}--`).val(""));
      for (var i in data){
        countySel.append($('<option/>').html(data[i].county).val(data[i].county));
      }
      $('#county-selection').show();
    }
  })
}

function showGraph(state, county) {
  $.get("./data/data.php", { query: "getData", 
                             state: state, 
                            county: county },
                            function (data) {

    if (county != "") {
      var location = `${county} County, ${state}`;
    } else {
      var location = state;
    }
    var dates = [];
    var cases = [];
    var deaths = [];
    var date = data[data.length-1].date;

    for (var i in data) {
      dates.push(data[i].date);
      cases.push(data[i].cases);
      deaths.push(data[i].deaths);
    }

    var chartdata = {
      labels: dates,
      datasets: [
        {
          label: 'Cases',
          borderColor: 'blue',
          fill: false,
          data: cases,
          hidden: !$("input.cases").prop("checked"),
        },
        {
          label: 'Deaths',
          borderColor: 'red',
          fill: false,
          data: deaths,
          hidden: !$("input.deaths").prop("checked"),
        }
      ]
    };

    var graphTarget = $(".graphCanvas").empty();

    if (chart) {
      chart.data = chartdata;
      chart.options.title.text = `COVID-19 Data for ${location} as of ${date}`;
      chart.update();

    } else {
        chart = new Chart(graphTarget, {
          type: 'line',
          data: chartdata,
          options: {
            responsive: true,
            title: {
              display: true,
              text: `COVID-19 Data for ${location} as of ${date}`,
            },
            scales: {
              yAxes: [{
                display: true,
                type: 'linear',
              }]
            }
          }
        });
    } 
  });
}

$(document).ready(function () {
  populateStates();

  showGraph("United States","");

  $("select.states").change( function() {
    var selectedState = $(this).children("option:selected").val();
    showGraph(selectedState, "");
    $('#county-selection').hide();
    populateCounties(selectedState);
  });

  $("select.counties").change( function() {
    var selectedCounty = $(this).children("option:selected").val();
    var selectedState = $(".states option:selected").val();
    showGraph(selectedState, selectedCounty);
  });

  $("input.cases").click( function() {
    if($(this).prop("checked")){
      chart.data.datasets[0].hidden = false;
      chart.update();
    }
    else {
      chart.data.datasets[0].hidden = true;
      chart.update();
    }
  });

  $("input.deaths").click( function() {
    if($(this).prop("checked")){
      chart.data.datasets[1].hidden = false;
      chart.update();
    }
    else {
      chart.data.datasets[1].hidden = true;
      chart.update();
    }
  });

  $("input.logarithmic").click( function() {
    if($(this).prop("checked")){
      chart.options.scales.yAxes[0].type = 'logarithmic';
      chart.update();
    }
    else {
      chart.options.scales.yAxes[0].type = 'linear';
      chart.update();
    }
  });

});