function getReport() {
    //Widgets count
    // $('.count-to').countTo();

    //Sales count to
    // $('.sales-count-to').countTo({
    //     formatter: function (value, options) {
    //         return '$' + value.toFixed(2).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, ' ').replace('.', ',');
    //     }
    // });

    // initRealTimeChart();
    // new Chart(document.getElementById("line_chart").getContext("2d"), getChartJs('bar'));
    // new Chart(document.getElementById("line_chart").getContext("2d"), getChartJs('bar_new'));
    // $.getJSON('https://raw.githubusercontent.com/yoshiki-o0/primely_web_console/master/data/data.json').then(function(data) {

    $.getJSON('http://127.0.0.1:5000/report').then(function(data) {
        console.log(data)
        new Chart(document.getElementById('line_chart').getContext('2d'),
                  getChartJs('bar_new', data))
    })
    // $.ajax({
    //   type: 'GET',
    //   url: {{ url_for('report')| tojson }},
    //   data: $(this).serialize()
    // }).done(renderChart)
    
    // function renderChart(data) {
    //   new Chart(document.getElementById('line_chart').getContext('2d'),
    //             getChartJs('bar_new', data))
    // }

    // initDonutChart();
    // initSparkline();
}

// $('#run'.on('submit', getReport));
$('#view').submit(function(){
  getReport();
  return false
})

function deletePdf() {
  $.ajax({
    method: 'DELETE',
    url: 'api/delete',
    success: function(result) {
      console.log('Deleted PDF')}
  });
}

$('#delete').submit(function(){
  deletePdf();
  return false
})

function deleteReport() {
  $.ajax({
    method: 'DELETE',
    url: 'api/reset',
    success: function(result) {
      console.log('Deleted report')}
  });
}

$('#reset').submit(function(){
  deleteReport();
  return false
})

function executeConversion() {
  $.get('http://127.0.0.1:5000/api/convert').done(function() {
    alert('Conversion complete');
    getReport();
  });
}

$('#run').submit(function(){
  executeConversion();
  return false
})


function uploadFiles() {
  var form_data = new FormData();
  var ins = document.getElementById('upload').files.length

  for (var x = 0; x < ins; x++) {
    form_data.append("files[]", document.getElementById('upload').files[x]);
  }

  $.ajax({
    method: 'POST',
    url: '/api/uploads',
    data: form_data,
    success: function(result) {
      alert('Uploaded PDF')}
  });
}

$('#upload').submit(function(){
// $('#upload').on('click', function(){
  // uploadFiles();
  var form_data = new FormData();
  var ins = document.getElementById('upload').files.length;

  for (var x = 0; x < ins; x++) {
    form_data.append("file[]", document.getElementById('upload').file[x]);
  }

  $.ajax({
    method: 'POST',
    url: '/api/uploads',
    data: form_data,
    success: function(result) {
      alert('Uploaded PDF')}
  });

  return false
})

// $(getReport);
$(document).ready(function() {
  getReport();
});


var realtime = 'on';
// function initRealTimeChart() {
//     //Real time ==========================================================================================
//     var plot = $.plot('#real_time_chart', [getRandomData()], {
//         series: {
//             shadowSize: 0,
//             color: 'rgb(0, 188, 212)'
//         },
//         grid: {
//             borderColor: '#f3f3f3',
//             borderWidth: 1,
//             tickColor: '#f3f3f3'
//         },
//         lines: {
//             fill: true
//         },
//         yaxis: {
//             min: 0,
//             max: 100
//         },
//         xaxis: {
//             min: 0,
//             max: 100
//         }
//     });

//     function updateRealTime() {
//         plot.setData([getRandomData()]);
//         plot.draw();

//         var timeout;
//         if (realtime === 'on') {
//             timeout = setTimeout(updateRealTime, 320);
//         } else {
//             clearTimeout(timeout);
//         }
//     }

//     updateRealTime();

//     $('#realtime').on('change', function () {
//         realtime = this.checked ? 'on' : 'off';
//         updateRealTime();
//     });
//     //====================================================================================================
// }

// function initSparkline() {
//     $(".sparkline").each(function () {
//         var $this = $(this);
//         $this.sparkline('html', $this.data());
//     });
// }

// function initDonutChart() {
//     Morris.Donut({
//         element: 'donut_chart',
//         data: [{
//             label: 'Chrome',
//             value: 37
//         }, {
//             label: 'Firefox',
//             value: 30
//         }, {
//             label: 'Safari',
//             value: 18
//         }, {
//             label: 'Opera',
//             value: 12
//         },
//         {
//             label: 'Other',
//             value: 3
//         }],
//         colors: ['rgb(233, 30, 99)', 'rgb(0, 188, 212)', 'rgb(255, 152, 0)', 'rgb(0, 150, 136)', 'rgb(96, 125, 139)'],
//         formatter: function (y) {
//             return y + '%'
//         }
//     });
// }

var data = [], totalPoints = 110;
// function getRandomData() {
//     if (data.length > 0) data = data.slice(1);

//     while (data.length < totalPoints) {
//         var prev = data.length > 0 ? data[data.length - 1] : 50, y = prev + Math.random() * 10 - 5;
//         if (y < 0) { y = 0; } else if (y > 100) { y = 100; }

//         data.push(y);
//     }

//     var res = [];
//     for (var i = 0; i < data.length; ++i) {
//         res.push([i, data[i]]);
//     }

//     return res;
// }

function getChartJs(type, data) {
    //Chart js ==========================================================================================
    var config = null;

    if (type === 'bar') {
        config = {
            type: 'bar',
            data: {
                labels: ["January", "February", "March", "April", "May", "June", "July"],
                datasets: [{
                    label: "My First dataset",
                    data: [65, 59, 80, 81, 56, 55, 40],
                    backgroundColor: 'rgba(0, 188, 212, 0.8)'
                }, {
                        label: "My Second dataset",
                        data: [28, 48, 40, 19, 86, 27, 90],
                        backgroundColor: 'rgba(233, 30, 99, 0.8)'
                    }]
            },
            options: {
                responsive: true,
                legend: false
            }
        }
    }
    else if (type === 'bar_new') {
        console.log('bar_new is here')
        config = getPaycheckData(data)
    }
    return config;
    //====================================================================================================
}

function getPaycheckData(data) {
  
    // # Define struct ----------------------------------
    let config = {
      type: 'bar',
      data: {
        labels: [],
        datasets: []
      },
      options: {
        scales: {
          xAxes: [{stacked: true}],
          yAxes: [{stacked: true}]
        }
      }
    }
  
    let dataset = {
      label: [],
      data: [],
      backgroundColor: [],
      // borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }// END OF Define struct----------------------------------
  
    // # Preprocess data ----------------------------------
    const types = data['incomes']['rows']
    const dates = data['incomes']['columns']
    const incomes = data['incomes']['values']
    const len = types.length
    // END OF Preprocess data ----------------------------------
  
    // # Build config structure ----------------------------------
    // Prepare dataset structure
    for (let index = 0; index < len; index++) {
      // Loop for the length of rows(types)
      let deepClone = JSON.parse(JSON.stringify(dataset))
      config.data.datasets.push(deepClone)
    }// ENDO OF Build config structure ----------------------------------
    
    // Insert data to structure ----------------------------------
    config.data.labels.push(...dates)
    types.forEach(function(type, i) {
      config.data.datasets[i].label.push(type)
    })
    incomes.forEach(function(income, i) {
      let arr = income
      let iterator = arr.values()
      for(let value of iterator) {
        config.data.datasets[i].data.push(value)
      }
    })
  
    let colors = []
    Object.keys(window.chartColors).forEach(function(key, i) {
      if (i < len) colors.push(key)
    })
    colors.forEach(function(color, i) {
      config.data.datasets[i].backgroundColor = window.chartColors[color]
    })// END OF Insert data to structure ----------------------------------
  
    return config
  }