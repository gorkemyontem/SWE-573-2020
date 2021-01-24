var buttons = document.getElementsByTagName("button")
for (var i = 0; i < buttons.length; i++) {
    var btn = buttons[i];
    btn.addEventListener('click', function (event) {
        if (!event.target.matches('.btn-api-call')) return;
        event.preventDefault(); 
        fetch(requestBase('/api/ajax/stats/' + event.target.id + '/'), postMethod)
        .then((res) => responseToJson(res))
        .then(data => {
            console.log(data);
        })

    }, false);
    
}
