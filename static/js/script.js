function skyPlotly(el, az, id, hour) {
    var id_str = [];

    for(var i = 0; i < id.length; i++) {
        var vec = [];
        for(var j = 0; j < id[i].length; j++) {
            vec[j] = 'PRN-' + id[i][j].toString();  
        }
        id_str[i] = vec;      
    }

    var data = [
        {
        type: "scatterpolar",
        mode: "markers+text",
        name: 'GPS ' + (az[hour].length).toString(),
        r: el[hour],
        theta: az[hour],
        text: id_str[hour],
        textposition: 'bottom',
        marker: {
            color: "#212529",
            symbol: "circle",
            size: 8
        }
        }
    ]

    var layout = {
        title: {
            text: ' Wykres Skyplot'
        },
        showlegend: true,
        autosize: true,
        polar: {
        domain: {
            x: [0,5],
            y: [5,0]
        },
        radialaxis: {
            tickfont: {
            size: 1
            }
        },
        angularaxis: {
            tickfont: {
            size: 8
            },
            rotation: 90,
            direction: "clockwise"
        }
        },
    }

    var config = {responsive: true}

    Plotly.newPlot('tester', data, layout, config);
}

function elevPlotly(route, x, y, colors, nr) {
    traceArr = new Array(nr);

    for(var i=0; i < nr; i++) {
        const randomColor = Math.floor(Math.random()*16777215).toString(16);
        var val = y[i];
        for(var j=0; j < y[i].length; j++) {
            if(val[j] < 0) {val[j] = ''}
        }

        var traceTemplate = {
            type: 'scatter',
            x: x,
            y: val,
            mode: 'lines',
            name: 'PRN-' + (i+1).toString(),
            line: {
                color: colors[i],
                width: 3
            }
        };
        traceArr[i] = traceTemplate;
    }
        
    var layout = {
        autosize: true,
        title: {
            text: 'Wykres elewacji od czasu'
        },
        xaxis: {
            title: 'Czas [min]'
        },
        yaxis: {
            title: 'Elewacja [°]'
        }
    };

    var config = {responsive: true}
        
    Plotly.newPlot(route, traceArr, layout, config);
}

function dopsPlotly(route, x, y, colors, id, names) {
    traceArr = new Array(id);

    for(var i=0; i < id; i++) {
        const randomColor = Math.floor(Math.random()*16777215).toString(16);
        var traceTemplate = {
            type: 'scatter',
            x: x,
            y: y[i],
            mode: 'lines',
            name: names[i],
            line: {
                color: colors[i],
                width: 3
            }
        };
        traceArr[i] = traceTemplate;
    }
        
    var layout = {
        autosize: true,
        title: {
            text: 'Wykres parametrów DOP od czasu'
        },
        xaxis: {
            title: 'Czas [min]'
        },
        yaxis: {
            title: 'Parametry DOP'
        }
    };

    var config = {responsive: true}
        
    Plotly.newPlot(route, traceArr, layout, config);
}

function satNrPlotly(route, x, y) {
    var data = [{
        x: x,
        y: y,
        type: 'bar'
    }];

    var layout = {
        autosize: true,
        title: {
            text: 'Wykres liczby satelitów od czasu'
        },
        xaxis: {
            title: 'Czas [min]'
        },
        yaxis: {
            title: 'Liczba satelitów na niebie'
        }
    }

    var config = {responsive: true}

    Plotly.newPlot(route, data, layout, config);
}

function groundtrack(route, lat, lon) {
    var data = [];
    var colors = randomColors(lat.length);
    
    for(var i=0; i < lat.length; i++) {
        var result = {
            type: 'scattergeo',
            lat: lat[i],
            lon: lon[i],
            mode: 'lines',
            name: 'PRN-' + (i+1).toString(),
            line:{
                width: 2,
                color: colors[i]
            }
        };

        data.push(result);
    }
    
    var layout = {
      title: 'Groundtrack satelitów',
      showlegend: true,
      geo: {
          resolution: 50,
          showland: true,
          showlakes: true,
          landcolor: 'rgb(204, 204, 204)',
          countrycolor: 'rgb(204, 204, 204)',
          lakecolor: 'rgb(255, 255, 255)',
          projection: {
            type: 'equirectangular'
          },
          coastlinewidth: 2,
          lataxis: {
            range: [ -90, 90 ],
            showgrid: true,
            tickmode: 'linear',
            dtick: 10
          },
          lonaxis:{
            range: [-180, 180],
            showgrid: true,
            tickmode: 'linear',
            dtick: 20
          }
        }
    };

    var config = {responsive: true};
    
    Plotly.newPlot(route, data, layout, config);
}

function randomColors(number) {
    finalColors = []
    for(var i=0; i < number; i++) {
        finalColors.push(Math.floor(Math.random()*16777215).toString(16));
    }

    return finalColors;
}