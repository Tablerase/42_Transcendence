console.log('Client is running');

const ws = new WebSocket('wss://transcendence.42.fr/ws/game/');

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
}
