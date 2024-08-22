console.log('Client is running');

/**
 * WebSocket connection
 */
const ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
const ws = new WebSocket(
    ws_scheme
    + '://'
    + window.location.host
    + '/ws/game/'
   // + game_id + '/'
);

ws.onopen = function(event) {
    console.log('Connected');
};

ws.onmessage = function(event) {
    console.log('Server says: ', event.data);
};

ws.onclose = function(event) {
    console.log('Disconnected');
};

ws.onerror = function(event) {
    console.log('Error');
};

// Canvas setup
const canvas = document.getElementById('game_canvas');
const ctx = canvas.getContext('2d');

// Player position
let player = {
    x: canvas.width / 2,
    y: canvas.height / 2
};

// Players positions
let players = {};

// Draw players
function drawPlayers() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
    for (let id in players) {
        const p = players[id];
        ctx.beginPath();
        ctx.arc(p.x, p.y, 5, 0, 2 * Math.PI); // Draw a point (circle) at the player's position
        ctx.fillStyle = 'red';
        ctx.fill();
        ctx.closePath();
    }
}

// Send player position to the server
function sendPosition() {
    ws.send(JSON.stringify({
        type: 'updatePosition',
        x: player.x,
        y: player.y
    }));
}

// Update player position based on mouse movement
canvas.addEventListener('mousemove', function(event) {
    const rect = canvas.getBoundingClientRect();
    player.x = event.clientX - rect.left;
    player.y = event.clientY - rect.top;
    sendPosition();
    drawPlayers();
});

// Handle messages from the server
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'positions') {
        players = data.positions;
        drawPlayers();
    }
};

// Initial draw
drawPlayers();
