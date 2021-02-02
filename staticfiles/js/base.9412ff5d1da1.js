if (parseInt(getSubredditId())) {
    postMethod.body = JSON.stringify({query: '', startDate: startDateVal, endDate: endDateVal, probability: (probabilityVal/100).toString(), rho: (rhoVal/100).toString()})
    runTabular();
    runBar();
    runWordCloud();
    runBubble();
    runNetwork();
}

if (getSearchText()) {
    postMethod.body = JSON.stringify({query: getSearchText(), startDate: startDateVal, endDate: endDateVal, probability: (probabilityVal/100).toString(), rho: (rhoVal/100).toString()})
    runNetworkSearch();
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
            if(data.top10submissions && data.top10submissions.length > 0){
                render(mediaTemplate(data.top10submissions), '#submissions-content');
            } else {
                renderEmptyWarning('#submissions-content')
            }
        })
        .finally((_) => removeOverlay('submission'));
}

// WORDS BAR CHART
async function runBar() {
    var ctx = document.getElementById('myChart');
    if (ctx) {
        ctx.getContext('2d');
        ctx.globalCompositeOperation='destination-over';
    }

    await fetch(requestBase('/api/ajax/words/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            if (!body || !body.data || !body.data.bar30counts || !body.data.bar30labels) {
                renderEmptyWarning('#mychart-error')
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
        })
        .finally((_) => removeOverlay('word'));
}

// WORDCLOUD
async function runWordCloud() {
    await fetch(requestBase('/api/ajax/wordcloud/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            if (!body || !body.data ) {
                renderEmptyWarning('#container-wordcloud-error')
                renderEmptyWarning('#container-entitycloud-error')
                return;
            } else if (body.data.wordCloud.length  == 0) {
                renderEmptyWarning('#container-wordcloud-error')
                return;
            } else if (body.data.entityCloud.length == 0) {
                renderEmptyWarning('#container-entitycloud-error')
                return;
            }
            console.log(body);

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

// PACKED BUBBLE CHART
async function runBubble() {
    await fetch(requestBase('/api/ajax/bubble/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => {
            if (!body || !body.data || !body.data.bubble500polarity || !body.data.bar30labels || !body.data.bubble500counts || !body.data.bubble500labels) {
                renderEmptyWarning('#packed-bubbles')
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

// NETWORK
async function runNetworkSearch() {
    await fetch(requestBase('/api/ajax/network-search/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => drawNetwork(body))
        .finally((_) => removeOverlay('network'));
}

// NETWORK
async function runNetwork() {
    await fetch(requestBase('/api/ajax/network/' + getSubredditId() + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then((body) => drawNetwork(body))
        .finally((_) => removeOverlay('network'));
}

function drawNetwork(body){
    if (!body || !body.data || body.data.network.length == 0 || body.data.networkDataset.length == 0){
        renderEmptyWarning('#container-network-chart-error')
        return;
    }
    var networkData = body.data.network;
    var dataset = body.data.networkDataset;

    var groupedNetworkData = networkData.reduce(function (r, a) {
        r[a.group_id] = r[a.group_id] || [];
        r[a.group_id].push(a.id);
        delete a.group_id;
        return r;
    }, Object.create(null));

    const groupedNetworkDataValues = Object.values(groupedNetworkData);
    const linkedData = groupedNetworkDataValues.map((ids) => linkify(ids));
    const filteredLinkedData = linkedData.filter((el) => el.length > 0);
    var edgesData = filteredLinkedData.flat();

    for (let i = 0; i < edgesData.length; i++) {
        const from = edgesData[i].from;
        const to = edgesData[i].to;
        var a = edgesData.filter((q) => q.from == from && q.to == to);
        edgesData[i].value = a.length;
        edgesData[i].title = `${a.length} occurences`;
    }

    edgesData = edgesData.filter((v, i, a) => a.findIndex((t) => t.from === v.from && t.to === v.to) === i);
    edgesData = edgesData.filter((el) => el.from != el.to); // Self targetting
    edgesData = edgesData.filter((el) => el.value > 4); // Min occurences

    arr = [];
    edgesData.forEach((el) => {
        if (arr.findIndex((x) => x.from == el.to && x.to == el.from) == -1) {
            arr.push(el);
        }
    });

    edgesData = arr;
    var onlyIds = edgesData.map((el) => el.from);
    onlyIds.push(...edgesData.map((el) => el.to));
    let uniqueIds = [...new Set(onlyIds)];
    dataset = dataset.filter((el) => uniqueIds.includes(el.id));

    // create an array with nodes
    var nodes = new vis.DataSet(dataset);
    // create an array with edges
    var edges = new vis.DataSet(edgesData);

    // create a network
    var container = document.getElementById('container-network-chart');
    var data = {
        nodes: nodes,
        edges: edges,
    };

    var options = {
        nodes: {
            shape: 'dot',
        },
        physics: {
            barnesHut: {
                gravitationalConstant: -29100,
                centralGravity: 0.85,
                springLength: 55,
                springConstant: 0.235,
                damping: 0.48,
                avoidOverlap: 1,
            },
            maxVelocity: 47,
            minVelocity: 0.75,
            solver: 'barnesHut',
        },
        edges: {
            font: {
                align: 'top',
            },
            smooth: {
                type: 'dynamic',
                forceDirection: 'horizontal',
                roundness: 0.0,
            },
        },
        layout: {
            improvedLayout: false,
        },
    };
    network = new vis.Network(container, data, options);
    network.on('stabilizationIterationsDone', function (params) {
        network.stopSimulation();
        network.setOptions({ physics: false });
    });

    network.stabilize(500);
}

function removeOverlay(id) {
    var overlay = document.getElementById('overlay-' + id);
    overlay.style.display = 'none';
}

function linkify(arr) {
    var res = [];
    for (let i = 0; i < arr.length; i++) {
        for (let j = i; j < arr.length; j++) {
            if (i != j) {
                res.push({ from: arr[i], to: arr[j] });
            }
        }
    }
    return res;
}
