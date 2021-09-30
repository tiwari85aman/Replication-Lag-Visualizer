var charts = []
function resizeCharts() {
    for (let index = 0; index < charts.length; index++) {
        const chart = charts[index];
        chart.resize();
    }
}

function setHostName(hostname) {
    hostname = hostname || "";
    $('#host_url').text(hostname);
}



function createMarkLine() {
    return {
        symbol: "none",
        label: {
            formatter: params => `Run #${params.dataIndex + 1}`
        },
        lineStyle: {color: "#5b6f66"},
        data: stats_history["markers"],
    }
}

function update_stats_charts(stats_history){
    if(stats_history["time"].length > 0){
        rpsChart.chart.setOption({
            xAxis: {data: stats_history["time"]},
            series: [
                {data: stats_history["size"]},
            ]
        });


    }
}

// init charts
var rpsChart = new LocustLineChart($(".charts-container"), "Lag vs Time", ["Lag"], "reqs/s", ['#00ca5a']);

charts.push(rpsChart);
update_stats_charts({"time":[], "size":[]})


function updateStats() {
    $.get('./stats', function (report) {
        window.report = report;
        try{
            stats_history = report
            console.log(stats_history)
            update_stats_charts(stats_history);
        } catch(i){
            console.debug(i);
        }
    }).always(function() {
        setTimeout(updateStats, 2000);
    });
}
updateStats();


