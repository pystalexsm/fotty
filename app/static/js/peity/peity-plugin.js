jQuery(function () {
    'use strict';
    jQuery("span.pie").peity("pie", {
        fill: ['#3F51B5', '#d7d7d7', '#ffffff']
    })

    jQuery(".line").peity("line", {
        fill: '#3F51B5',
        stroke: '#169c81',
    })

    jQuery(".bar").peity("bar", {
        fill: ["#3F51B5", "#d7d7d7"]
    })

    jQuery(".bar_dashboard").peity("bar", {
        fill: ["#1ab394", "#d7d7d7"],
        width: 100
    })

    var updatingChart = jQuery(".updating-chart").peity("line", {fill: '#3F51B5', stroke: '#169c81', width: 64})

    setInterval(function () {
        var random = Math.round(Math.random() * 10)
        var values = updatingChart.text().split(",")
        values.shift()
        values.push(random)

        updatingChart
                .text(values.join(","))
                .change()
    }, 1000);

});
