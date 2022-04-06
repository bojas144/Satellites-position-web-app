function skyPlot(el, az, id, hour) {
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
        mode: "markers",
        name: 'GPS ' + (az[hour].length).toString(),
        r: el[hour],
        theta: az[hour],
        text: id_str[hour],
        textposition: top,
        marker: {
            color: "#212529",
            symbol: "circle",
            size: 8
        }
        }
    ]

    var layout = {
        title: {
            text: 'Skyplot',
            font: {
                family: 'Titillium Web',
                size: 24
            },
            xref: 'paper',
            x: 0.05,
        },
        showlegend: true,
        autosize: false,
        width: 650,
        height: 380,
        margin: {
            l: 10,
            r: 10,
            b: 40,
            t: 40,
            pad: 4
        },
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
        }
    }

    Plotly.newPlot('tester', data, layout)
}