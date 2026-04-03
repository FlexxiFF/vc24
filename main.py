import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive, load_config

def joiner(token, status, guild_id, channel_id, self_mute, self_deaf):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    auth = {"op": 2,"d": {"token": token,"properties": {"$os": "Windows 10","$browser": "Google Chrome","$device": "Windows"},"presence": {"status": status,"afk": False}},"s": None,"t": None}
    vc = {"op": 4,"d": {"guild_id": guild_id,"channel_id": channel_id,"self_mute": self_mute,"self_deaf": self_deaf}}
    ws.send(json.dumps(auth))
    ws.send(json.dumps(vc))
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1,"d": None}))

def run_joiner():
    os.system("cls" if os.name == "nt" else "clear")
    print("Discord Bot Background Process Started.")
    print("Open http://localhost:8080 to configure settings!")
    print("--------------------------------------------------")
    
    while True:
        config = load_config()
        token = config.get("usertoken", "")
        
        if not token:
            print(f"[{time.strftime('%X')}] [INFO] Waiting for Web Dashboard configuration.")
            print("Please add your Token at http://localhost:8080")
            time.sleep(10)
            continue
            
        headers = {"Authorization": token, "Content-Type": "application/json"}
        validate = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        
        if validate.status_code != 200:
            print(f"[{time.strftime('%X')}] [ERROR] Token is invalid. Please update it at http://localhost:8080")
            time.sleep(10)
            continue
            
        userinfo = validate.json()
        username = userinfo.get("username", "Unknown")
        discriminator = userinfo.get("discriminator", "0000")
        
        print(f"[{time.strftime('%X')}] Logged in as {username}#{discriminator}. Generating Heartbeat...")
        
        try:
            joiner(
                token,
                config.get("status", "online"),
                config.get("guild_id", ""),
                config.get("channel_id", ""),
                config.get("self_mute", True),
                config.get("self_deaf", False)
            )
        except Exception as e:
            print(f"[{time.strftime('%X')}] [WARNING] WebSocket Connection Failed: {e}")
            
        time.sleep(30)

if __name__ == "__main__":
    keep_alive()
    run_joiner()
