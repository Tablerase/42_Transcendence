// var ctx = document.getElementById('winLossChart').getContext('2d');
// var winLossChart = new Chart(ctx, {
//   type: 'doughnut',
//   data: {
//     labels: ['Wins', 'Losses'],
//     datasets: [{
//       data: [{{ win_percentage }}, {{ loss_percentage }}],
//       backgroundColor: ['#4caf50', '#f44336'],
//       borderWidth: 1
//     }]
//   },
//   options: {
//     responsive: true,
//     maintainAspectRatio: false,
//     cutoutPercentage: 70,
//     plugins: {
//       legend: {
//         display: true,
//       }
//     }
//   }
// });