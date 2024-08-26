console.log('Client is running');

// Get room_name from the DOM
const room_name = document.getElementById('room_name').textContent;
console.log('Room name:', room_name);

/**
 * WebSocket connection
 */
const ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
const ws_url = ws_scheme
    + '://'
    + window.location.host
    + '/'
    + 'ws/test/'
    + room_name
    + '/';

const ws = new WebSocket(ws_url);
console.log('Path:', window.location.pathname);
console.log('WebSocket path:', ws_url);

ws.onopen = function(event) {
    console.log('Connected');
};

ws.onmessage = function(event) {
    console.log('Server says: ', event.data);
};

ws.onclose = function(event) {
    console.log('Disconnected');
    console.log('Code:', event.code, getStatusCodeString(event.code));
    console.log('Reason:', event.reason);
};

ws.onerror = function(event) {
    console.log('Error: ', event);
};

/**
 * Websocket Status Codes
 * */
let specificStatusCodeMappings = {
    '1000': 'Normal Closure',
    '1001': 'Going Away',
    '1002': 'Protocol Error',
    '1003': 'Unsupported Data',
    '1004': '(For future)',
    '1005': 'No Status Received',
    '1006': 'Abnormal Closure',
    '1007': 'Invalid frame payload data',
    '1008': 'Policy Violation',
    '1009': 'Message too big',
    '1010': 'Missing Extension',
    '1011': 'Internal Error',
    '1012': 'Service Restart',
    '1013': 'Try Again Later',
    '1014': 'Bad Gateway',
    '1015': 'TLS Handshake'
};

function getStatusCodeString(code) {
    if (code >= 0 && code <= 999) {
        return '(Unused)';
    } else if (code >= 1016) {
        if (code <= 1999) {
            return '(For WebSocket standard)';
        } else if (code <= 2999) {
            return '(For WebSocket extensions)';
        } else if (code <= 3999) {
            return '(For libraries and frameworks)';
        } else if (code <= 4999) {
            return '(For applications)';
        }
    }
    if (typeof(specificStatusCodeMappings[code]) !== 'undefined') {
        return specificStatusCodeMappings[code];
    }
    return '(Unknown)';
}