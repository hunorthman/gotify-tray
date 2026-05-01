#!/usr/bin/env python3
import time
import threading
import json
import os
import subprocess
import websocket
import ssl
import logging
import webbrowser
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- BEÁLLÍTÁSOK ---
GOTIFY_URL = "IDE ÍRD A GOTIFY SERVER CÍMÉT"
CLIENT_TOKEN = "IDE ÍRD VAGY MÁSOLD BE A TOKENT"
LOG_FILE = os.path.join(SCRIPT_DIR, "gotify-tray.log")
# -------------------

# Naplózás beállítása (konzol helyett fájlba megy, időbélyeggel)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO, # Átírhatod DEBUG-ra, ha még több infót akarsz látni
    format='%(asctime)s - %(levelname)s - %(message)s'
)

websocket.enableTrace(False)

status = "Kapcsolódás..."
current_display_state = None
icon = None

def create_image(status_type):
    try:
        icon_path = os.path.join(SCRIPT_DIR, "gotify-logo.png")
        img = Image.open(icon_path).convert("RGBA")
        if status_type == "offline":
            return img.convert("L").convert("RGBA")
        return img
    except Exception as e:
        logging.error(f"Kép betöltési hiba: {e}")
        image = Image.new('RGBA', (22, 22), (0, 0, 0, 0))
        color = "red" if status_type == "offline" else "green"
        ImageDraw.Draw(image).ellipse((2, 2, 20, 20), fill=color)
        return image

def update_status(new_status, color_key):
    global status, current_display_state

    if current_display_state == color_key and status == new_status:
        return

    status = new_status
    current_display_state = color_key

    if icon:
        icon.icon = create_image(color_key)
        icon.title = f"Gotify: {status}"
        icon.menu = Menu(
            MenuItem(f"Állapot: {status}", None, enabled=False),
            MenuItem("Gotify megnyitása", open_web, default=True),
            MenuItem("Kilépés", on_quit)
        )

def on_message(ws, message):
    msg = json.loads(message)
    title = msg.get('title', 'Gotify')
    body = msg.get('message', '')

    logging.info(f"Új üzenet érkezett: {title}")

    subprocess.run([
        'notify-send',
        '-u', 'normal',
        '-a', 'Gotify-Server',
        '-h', 'string:desktop-entry:Gotify-Server',
        title,
        body,
        '-i', 'network-server'
    ])

def on_open(ws):
    logging.info("--- SIKERES KAPCSOLÓDÁS A STREAMHEZ ---")
    update_status("Online", "online")

def on_error(ws, error):
    logging.error(f"--- HIBA TÖRTÉNT: {error} ---")

def on_close(ws, close_status_code, close_msg):
    logging.warning(f"--- KAPCSOLAT LEZÁRVA: Kód: {close_status_code}, Üzenet: {close_msg} ---")
    update_status("Offline", "offline")

def run_websocket():
    while True:
        try:
            logging.info(f"Próbálkozás: wss://{GOTIFY_URL} ...")
            ws_url = f"wss://{GOTIFY_URL}/stream?token={CLIENT_TOKEN}"

            header = [
                "User-Agent: Mozilla/5.0 (X11; Linux x86_64) Gotify-Tray-Client"
            ]

            ws = websocket.WebSocketApp(
                ws_url,
                header=header,
                on_message=on_message,
                on_open=on_open,
                on_error=on_error,
                on_close=on_close
            )

            ws.run_forever(
                ping_interval=30,
                ping_timeout=10,
                sslopt={"cert_reqs": ssl.CERT_NONE}
            )
        except Exception as e:
            logging.error(f"Kivétel a futás során: {e}")

        logging.info("Újrapróbálkozás 10 másodperc múlva...")
        update_status("Offline", "offline")
        time.sleep(10)

def open_web(icon, item):
    logging.info("Gotify webes felület megnyitása...")
    webbrowser.open(f"https://{GOTIFY_URL}")

def on_quit(icon, item):
    logging.info("Kilépés a programból...")
    icon.stop()
    os._exit(0)

logging.info("=========================================")
logging.info("Gotify Tray Client indítása...")

icon = Icon("Gotify", create_image("offline"), title="Gotify: Indítás...", menu=Menu(
    MenuItem(f"Állapot: {status}", None, enabled=False),
    MenuItem("Kilépés", on_quit)
))

threading.Thread(target=run_websocket, daemon=True).start()
icon.run()
