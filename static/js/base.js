if (parseInt(getSubredditId())) {
    runTabular();
    runBar();
    runWordCloud();
    runBubble();

}

// TABULAR DATA
async function runTabular() {
    await fetch(requestBase('/api/ajax/submissions/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            if (!body) {
                return;
            }
            data = body.data;
            data.top10submissions.forEach((el) => (el.children = data[el.submission_id]));
            render(mediaTemplate(data.top10submissions), '#submissions-content');
        })
        .finally((_) => removeOverlay('submission'));
}

// WORDS BAR CHART
async function runBar() {
    await fetch(requestBase('/api/ajax/words/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            if (!body) {
                return;
            }
            var ctx = document.getElementById('myChart');
            if (ctx) {
                ctx.getContext('2d');
            }
            var maxVal = 20;
            first20Label = body.data.bar30labels.slice(0, maxVal);
            first20Count = body.data.bar30counts.slice(0, maxVal);
            var delta = Math.floor(globalColors.length / maxVal);
            var backgroundColors = globalColors.filter((value, index, Arr) => index % delta == 0);
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: first20Label,
                    datasets: [
                        {
                            label: 'Count',
                            data: first20Count,
                            backgroundColor: backgroundColors,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        yAxes: [
                            {
                                ticks: {
                                    beginAtZero: true,
                                },
                            },
                        ],
                    },
                },
            });
        })
        .finally((_) => removeOverlay('word'));
}

// PACKED BUBBLE CHART
async function runBubble() {
    await fetch(requestBase('/api/ajax/bubble/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            if (!body || !body.data) {
                return;
            }

            bubbledata = body.data;
            var len = bubbledata['bubble500polarity'].length;
            var negative = { name: 'Negative', data: [], color: '#e74c3c' };
            var positive = { name: 'Positive', data: [], color: '#1abc9c' };
            var netural = { name: 'Netural', data: [], color: '#2c3e50' };
            for (let i = 0; i < len; i++) {
                const polarity = bubbledata['bubble500polarity'][i];
                switch (polarity) {
                    case 'Negative':
                        negative.data.push({ value: bubbledata['bubble500counts'][i], name: bubbledata['bubble500labels'][i] });
                        break;
                    case 'Positive':
                        positive.data.push({ value: bubbledata['bubble500counts'][i], name: bubbledata['bubble500labels'][i] });
                        break;
                    default:
                        netural.data.push({ value: bubbledata['bubble500counts'][i], name: bubbledata['bubble500labels'][i] });
                        break;
                }
            }

            Highcharts.chart('packed-bubbles', {
                chart: {
                    type: 'packedbubble',
                    height: '60%',
                },
                title: {
                    text: 'Top 100 Tags (Count & AVG Polarity)',
                },
                tooltip: {
                    useHTML: true,
                    pointFormat: '<a href="http://en.wikipedia.org/wiki/{point.name}" target="_blank"><b>{point.name}:</b> {point.y}</a>',
                },

                plotOptions: {
                    packedbubble: {
                        minSize: '10%',
                        maxSize: '200%',
                        zMin: 0,
                        zMax: 100,
                        layoutAlgorithm: {
                            splitSeries: false,
                            gravitationalConstant: 0.02,
                        },
                        dataLabels: {
                            enabled: true,
                            format: '{point.name}',
                            style: {
                                color: 'black',
                                textOutline: 'none',
                                fontWeight: 'normal',
                            },
                        },
                        minPointSize: 5,
                    },
                },
                series: [negative, positive, netural],
            });
        })
        .finally((_) => removeOverlay('bubble'));
}

// WORDCLOUD
async function runWordCloud() {
    await fetch(requestBase('/api/ajax/wordcloud/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            var wordCloudData = body.data.wordCloud;
            var entityCloudData = body.data.entityCloud;
            var wordsAndWeights = wordCloudData.filter(({ name }) => !stopWords.includes(name.toLowerCase())).slice(0, 250);
            var entitiesAndWeights = entityCloudData.filter(({ name }) => !stopWords.includes(name.toLowerCase())).slice(0, 250);
            var coefficientWord = 1000 / Math.sqrt(Math.max(...wordsAndWeights.map((e) => e.weight)));
            var coefficientEntity = 1000 / Math.sqrt(Math.max(...entitiesAndWeights.map((e) => e.weight)));
            wordsAndWeights.forEach((e) => (e.weight = Math.sqrt(e.weight) * coefficientWord));
            entitiesAndWeights.forEach((e) => (e.weight = Math.sqrt(e.weight) * coefficientEntity));
            Highcharts.chart('container-wordcloud', {
                series: [
                    {
                        type: 'wordcloud',
                        data: wordsAndWeights,
                        name: 'Ratio',
                    },
                ],
                title: {
                    text: '',
                },
            });

            Highcharts.chart('container-entitycloud', {
                series: [
                    {
                        type: 'wordcloud',
                        data: entitiesAndWeights,
                        name: 'Ratio',
                    },
                ],
                title: {
                    text: '',
                },
            });
        })
        .finally((_) => removeOverlay('cloud'));
}

function removeOverlay(id) {
    var overlay = document.getElementById('overlay-' + id);
    overlay.style.display = 'none';
}

  