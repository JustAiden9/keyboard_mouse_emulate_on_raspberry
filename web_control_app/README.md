# Keyboard & Mouse Web Control App

This is a simple web app to control keyboard and mouse over the network via your Raspberry Pi Bluetooth emulator.

## Setup

1. On your Raspberry Pi, ensure the Bluetooth server is running as per the original instructions.

2. Install Flask on the Pi: `sudo pip3 install flask`

3. Copy `network_control_server.py` to your Pi and run it: `python3 network_control_server.py`

4. On your Windows machine, open `index.html` in a web browser.

5. In `app.js`, update `PI_IP` to your Raspberry Pi's IP address.

6. Use the interface to send keyboard inputs and mouse controls.

## Features

- Send text strings
- Special keys (Enter, Backspace, etc.)
- Mouse clicks and basic movement

Note: Mouse movement is relative and basic. For more advanced control, enhance the app as needed.