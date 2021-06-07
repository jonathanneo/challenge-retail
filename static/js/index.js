

var metric = "Revenue"
var years = ["2004", "2005", "2006", "2007"]

$.get(`/api/timeseries/${metric.toLowerCase()}/${years}`, (res) => {
    var year = Object.keys(res);
    var metricValue = Object.values(res);
    var data = [
        {
            x: year,
            y: metricValue,
            type: 'bar',
            marker: {
                color: '#212529',
                width: 1
            }
        }
    ];
    var layout = {
        title: `Time Series (${metric})`,
        yaxis: {
            title: `${metric} ($ Billions)`
        },
        xaxis: {
            title: `Year`
        }
      };
    
    Plotly.newPlot('timeseries', data, layout);
});

function sortObject(unsorted){
    var sortedlist = Object.keys(unsorted).sort(function(a,b){return unsorted[a]-unsorted[b]});
    var sorted = {}
    sortedlist.forEach(function(item){
        sorted[item]=unsorted[item]
    })
    return sorted;
}

$.get(`/api/country/${metric.toLowerCase()}/${years}`, (res) => {
    
    var resSorted = sortObject(res);
    var country = Object.keys(resSorted);
    var metricValue = Object.values(resSorted);
    var data = [
        {
            y: country,
            x: metricValue,
            type: 'bar',
            marker: {
                color: '#212529',
                width: 1,
            },
            orientation: 'h'
        }
    ];
    var layout = {
        title: `Time Series (${metric})`,
        xaxis: {
            title: `${metric} ($ Millions)`
        },
        yaxis: {
            title: `Country`
        }
      };
    
    Plotly.newPlot('country', data, layout);
});