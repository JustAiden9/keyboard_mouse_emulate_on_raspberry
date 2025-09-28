#!/usr/bin/python3

import os
import sys
import dbus
import dbus.service
import dbus.mainloop.glib
import time
from flask import Flask, request, jsonify
import keymap

app = Flask(__name__)

class BTKClient:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object('org.thanhle.btkbservice', '/org/thanhle/btkbservice')
        self.iface = dbus.Interface(self.btkservice, 'org.thanhle.btkbservice')

    def send_keys(self, modifier_byte, keys):
        self.iface.send_keys(modifier_byte, keys)

    def send_mouse(self, modifier_byte, keys):
        self.iface.send_mouse(modifier_byte, keys)

client = BTKClient()

@app.route('/send_string', methods=['POST'])
def send_string():
    data = request.get_json()
    string_to_send = data.get('string', '')
    if not string_to_send:
        return jsonify({'error': 'No string provided'}), 400

    # Reuse logic from send_string.py
    KEY_DOWN_TIME = 0.01
    KEY_DELAY = 0.01

    state = [
        0xA1,  # this is an input report
        0x01,  # Usage report = Keyboard
        [0, 0, 0, 0, 0, 0, 0, 0],  # Modifiers
        0x00,  # Vendor reserved
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00  # keys
    ]

    scancodes = {
        "-": "KEY_MINUS",
        "=": "KEY_EQUAL",
        ";": "KEY_SEMICOLON",
        "'": "KEY_APOSTROPHE",
        "`": "KEY_GRAVE",
        "\\": "KEY_BACKSLASH",
        ",": "KEY_COMMA",
        ".": "KEY_DOT",
        "/": "KEY_SLASH",
        " ": "KEY_SPACE",
    }

    for c in string_to_send:
        cu = c.upper()
        modifiers = [0, 0, 0, 0, 0, 0, 0, 0]
        if cu in scancodes:
            scantablekey = scancodes[cu]
            if scantablekey.islower():
                modifiers[6] = 1  # Left Shift
                scantablekey = scantablekey.upper()
        else:
            if c.isupper():
                modifiers[6] = 1
            scantablekey = "KEY_" + cu

        try:
            scancode = keymap.keytable[scantablekey]
        except KeyError:
            print("character not found in keytable:", c)
            continue
        else:
            # send key down
            state[2] = modifiers
            state[4] = scancode
            bin_str = "".join(str(bit) for bit in state[2])
            client.send_keys(int(bin_str, 2), state[4:10])
            time.sleep(KEY_DOWN_TIME)
            # send key up
            state[4] = 0
            client.send_keys(int(bin_str, 2), state[4:10])
            time.sleep(KEY_DELAY)

    return jsonify({'status': 'sent'})

@app.route('/send_key', methods=['POST'])
def send_key():
    data = request.get_json()
    key_name = data.get('key', '')
    if not key_name:
        return jsonify({'error': 'No key provided'}), 400

    try:
        scancode = keymap.keytable[key_name]
    except KeyError:
        return jsonify({'error': 'Key not found'}), 400

    modifiers = [0, 0, 0, 0, 0, 0, 0, 0]
    bin_str = "00000000"
    # send key down
    client.send_keys(int(bin_str, 2), [scancode, 0, 0, 0, 0, 0])
    time.sleep(0.01)
    # send key up
    client.send_keys(int(bin_str, 2), [0, 0, 0, 0, 0, 0])

    return jsonify({'status': 'sent'})

@app.route('/send_mouse_click', methods=['POST'])
def send_mouse_click():
    data = request.get_json()
    button = data.get('button', 0)  # 1 for left, 2 for right, etc.
    try:
        button = int(button)
    except:
        button = 0

    client.send_mouse(0, bytes([button, 0, 0, 0]))
    time.sleep(0.01)
    client.send_mouse(0, bytes([0, 0, 0, 0]))  # release

    return jsonify({'status': 'clicked'})

@app.route('/send_mouse_move', methods=['POST'])
def send_mouse_move():
    data = request.get_json()
    dx = data.get('dx', 0)
    dy = data.get('dy', 0)
    try:
        dx = int(dx)
        dy = int(dy)
    except:
        dx = dy = 0

    client.send_mouse(0, bytes([0, dx, dy, 0]))

    return jsonify({'status': 'moved'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)