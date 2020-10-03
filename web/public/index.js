google.load('visualization', '1', { 'packages': ['geochart'] });
google.setOnLoadCallback(drawVisualization);
const url = 'https://api.covid19india.org/data.json';

async function drawVisualization() {
    let obj = [];
    await fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data); // Prints result from `response.json()` in getRequest
            data = data.statewise;
            data.forEach(ele => {
                obj.push({'state' : ele.state, 'confirmed':ele.confirmed})
            })
            console.log(obj)
        })
        .catch(error => console.error(error))
   
    var data = google.visualization.arrayToDataTable([
        ['State', 'Confirmed'],
        [obj[1].state, parseInt(obj[1].confirmed) ],
        [obj[2].state,obj[2].confirmed],
        [obj[3].state,obj[3].confirmed],
        [obj[4].state,obj[4].confirmed],
        [obj[5].state,obj[5].confirmed],
        [obj[6].state,obj[6].confirmed],
        [obj[7].state,obj[7].confirmed],
        [obj[8].state,obj[8].confirmed],
        [obj[9].state,obj[9].confirmed],
        [obj[10].state,obj[10].confirmed],
        [obj[11].state,obj[11].confirmed],
        [obj[12].state,obj[12].confirmed],
        [obj[13].state,obj[13].confirmed],
        [obj[14].state,obj[14].confirmed],
        [obj[15].state,obj[15].confirmed],
        [obj[16].state,obj[16].confirmed],
        [obj[17].state,obj[17].confirmed],
        [obj[18].state,obj[18].confirmed],
        [obj[19].state,obj[19].confirmed],
        [obj[20].state,obj[20].confirmed],
        [obj[21].state,obj[21].confirmed],
        [obj[22].state,obj[22].confirmed],
        [obj[23].state,obj[23].confirmed],
        [obj[24].state,obj[24].confirmed],
        [obj[25].state,obj[25].confirmed],
        [obj[26].state,obj[26].confirmed],
        [obj[27].state,obj[27].confirmed],
        [obj[28].state,obj[28].confirmed],
        [obj[29].state,obj[29].confirmed],
        [obj[30].state,obj[30].confirmed],
        [obj[31].state,obj[31].confirmed],
        [obj[32].state,obj[32].confirmed],
        [obj[33].state,obj[33].confirmed],
        [obj[34].state,obj[34].confirmed],
        [obj[35].state,obj[35].confirmed],
        [obj[36].state,obj[36].confirmed],
        [obj[37].state,obj[37].confirmed]
    ]
    )
    console.log(data)
    var opts = {
        region: 'IN',
       // displayMode: 'regions',
        resolution: 'provinces',
        colorAxis: {minValue:0,maxValue:500,colors:['#ffffff','#0000ff'] },
        width:600
    };
    var geochart = new google.visualization.GeoChart(
        document.getElementById('visualization'));
    geochart.draw(data, opts);
};