var csrftokenTag = document.querySelector('[name=csrfmiddlewaretoken]');
if (csrftokenTag) var csrftoken = csrftokenTag.value;

var requestBase = (url) =>
    new Request(url, {
        headers: {
            'X-CSRFToken': csrftoken,
            Accept: 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        },
    });

var responseToJson = (response) => {
    return response.json();
};

var postMethod = { method: 'POST', mode: 'same-origin' };
var getMethod = { method: 'GET', mode: 'same-origin' };

var getSubredditId = () => {
    var parts = window.location.pathname.split('/');
    var lastSegment = parts.pop() || parts.pop();
    return lastSegment;
};

var globalColors = [
    '#FF0000',
    '#FF0a00',
    '#FF1400',
    '#FF1e00',
    '#FF2800',
    '#FF3200',
    '#FF3c00',
    '#FF4600',
    '#FF5000',
    '#FF5a00',
    '#FF6400',
    '#FF6e00',
    '#FF7800',
    '#FF8200',
    '#FF8c00',
    '#FF9600',
    '#FFa000',
    '#FFaa00',
    '#FFb400',
    '#FFbe00',
    '#FFc800',
    '#FFd200',
    '#FFdc00',
    '#FFe600',
    '#FFf000',
    '#FFfa00',
    '#fdff00',
    '#d7ff00',
    '#b0ff00',
    '#8aff00',
    '#65ff00',
    '#3eff00',
    '#17ff00',
    '#00ff10',
    '#00ff36',
    '#00ff5c',
    '#00ff83',
    '#00ffa8',
    '#00ffd0',
    '#00fff4',
    '#00e4ff',
    '#00d4ff',
    '#00c4ff',
    '#00b4ff',
    '#00a4ff',
    '#0094ff',
    '#0084ff',
    '#0074ff',
    '#0064ff',
    '#0054ff',
    '#0044ff',
    '#0032ff',
    '#0022ff',
    '#0012ff',
    '#0002ff',
    '#0000ff',
    '#0100ff',
    '#0200ff',
    '#0300ff',
    '#0400ff',
];
