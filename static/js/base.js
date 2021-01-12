var ctx = document.getElementById('myChart').getContext('2d');

var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3, 5, 2, 3, 1],
            backgroundColor: [
                '#8e44ad',
                '#9b59b6',
                '#c0392b',
                '#e74c3c',
                '#2980b9',
                '#3498db',
                '#16a085',
                '#1abc9c',
                '#27ae60',
                '#2ecc71'
            ],
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
