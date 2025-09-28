const PI_IP = '192.168.1.100'; // Replace with your Raspberry Pi's IP address
const PORT = 5000;

async function sendRequest(endpoint, data) {
    try {
        const response = await fetch(`http://${PI_IP}:${PORT}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        console.log(result);
    } catch (error) {
        console.error('Error:', error);
    }
}

function sendString() {
    const text = document.getElementById('textInput').value;
    sendRequest('/send_string', { string: text });
}

function sendKey(key) {
    sendRequest('/send_key', { key: key });
}

function sendMouseClick(button) {
    sendRequest('/send_mouse_click', { button: button });
}

function sendMouseMove(dx, dy) {
    sendRequest('/send_mouse_move', { dx: dx, dy: dy });
}