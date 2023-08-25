(function() {
    var $chart = $('#chart-sales-dark');
  
    function init($chart) {
      var salesChart = new Chart($chart, {
        type: 'line',
        data: {
          labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          datasets: [{
            label: 'Performance',
            data: [0, 7, 7, 6, 5, 4, 3, 2, 1]
          }]
        },
        // other chart options and configurations
      });
  
      $chart.data('chart', salesChart);
    }
  
    if ($chart.length) {
      init($chart);
    }
  })();
  