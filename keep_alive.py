from flask import Flask, render_template, request, jsonify
from threading import Thread
import json
import os

app = Flask(__name__)

CONFIG_PATH = 'config.json'

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {
        "usertoken": "",
        "guild_id": "",
        "channel_id": "",
        "status": "online",
        "self_mute": True,
        "self_deaf": False
    }

def save_config(data):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@app.route('/api/save', methods=['POST'])
def update_config():
    data = request.json
    save_config(data)
    return jsonify({"success": True})

def run():
    # Set use_reloader=False so it doesn't crash in a thread
    app.run(host="0.0.0.0", port=8080, use_reloader=False)

def keep_alive():
    server = Thread(target=run)
    server.daemon = True
    server.start()
