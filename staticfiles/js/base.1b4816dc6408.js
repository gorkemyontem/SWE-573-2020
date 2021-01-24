var ctx = document.getElementById('myChart');
if (ctx) ctx.getContext('2d');
// # SentenceAnalysis.objects.all().filter(subreddit_id=subreddit.subreddit_id)
// # nouns = self.flattenNouns(SentenceAnalysis.objects.all().filter(subreddit_id=subreddit.subreddit_id).values_list('noun_phrases', flat=True))
// # "http://'+lang+'.wikipedia.org/wiki/'+data.annotations[i].title+'" '+
if (parseInt(getSubredditId())) {
    fetch(requestBase('/api/ajax/words/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            if (!body) {
                return;
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
            removeOverlay();
        });
}

if (parseInt(getSubredditId())) {
    fetch(requestBase('/api/ajax/bubble/' + getSubredditId() + '/'), postMethod)
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
        });
}

// path('api/ajax/submissions/<int:pk>/', DataSubmissions.as_view(), name = "data_submissions"),
// path('api/ajax/comments/<int:pk>/<int:submission_id>', DataComments.as_view(), name = "data_comments"),
if (parseInt(getSubredditId())) {
    fetch(requestBase('/api/ajax/submissions/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            if (!body) {
                return;
            }
            console.log(body);
        });
}
// if (parseInt(getSubredditId())) {
//     fetch(requestBase('/api/ajax/submissions/' + getSubredditId() + '/'), postMethod)
//         .then((res) => responseToJson(res))
//         .then((body) => {
//             if (!body) {
//                 return;
//             }
//             console.log(body);
//         });
// }

function removeOverlay() {
    var overlay = document.getElementById('overlay');
    console.log(overlay);
    overlay.style.display = 'none';
}
