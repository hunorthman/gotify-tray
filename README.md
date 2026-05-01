# 🇭🇺 Gotify Desktop Tray Client (Linux / KDE Plasma)

*[English version below / Olvasd angolul](#-english-version)*

Egy pehelysúlyú, Python alapú tálcaalkalmazás (tray app), amely WebSocketen keresztül kapcsolódik a Gotify szerveredhez, és valós időben, natív Linux értesítésekként (`notify-send`) jeleníti meg a beérkező üzeneteket.

A kliens kifejezetten KDE Plasma asztali környezetre lett optimalizálva (tökéletesen fut pl. Nobara Linuxon), így hibátlanul integrálódik a rendszer értesítési központjába.

## ✨ Funkciók
* **Valós idejű értesítések:** Azonnali push üzenetek a Gotify szervertől a megnyitott WebSocket csatornán keresztül.
* **KDE Értesítési Központ integráció:** Az üzenetek nem csak felugranak, hanem be is kerülnek az értesítési előzményekbe (a harang ikon alá), így később is bármikor visszaolvashatók.
* **Dinamikus tálca ikon:** Színes/szürke állapotjelző a kapcsolat státuszáról (Online/Offline).
* **Gyors elérés:** A tálcaikonra bal gombbal kattintva azonnal megnyílik a Gotify webes felülete az alapértelmezett böngésződben.
* **Egyedi alkalmazásnév:** Az értesítések fejlécében a `Gotify-DebianServer` név jelenik meg az egyszerű parancsnév helyett.
* **Öngyógyító kapcsolat:** Hálózati szakadás, tétlenség vagy szerver újraindulás esetén a kliens automatikusan próbál újracsatlakozni.

## 🛠️ Előfeltételek
A futtatáshoz Python 3-ra és a rendszer natív értesítő szolgáltatására van szükség.

**Rendszercsomagok:**
```bash
sudo dnf install libnotify
```

**Python csomagok telepítése:**
```bash
pip install websocket-client pystray Pillow
```

## 🚀 Beállítás és Használat

1. **Fájlok előkészítése:** Klónozd a repót, vagy tedd egy mappába a `gotify-tray.py` fájlt és a hozzá tartozó `gotify-logo.png` ikont.
2. **Token és URL beállítása:** Nyisd meg a `gotify-tray.py` fájlt egy szövegszerkesztőben, és írd át a szerver URL-jét, illetve a tokenedet.
   > ⚠️ **Fontos:** A Gotify webes felületén a **Clients** (Kliensek) menüben kell új tokent generálnod. Ez egy **`C`** betűvel kezdődő token lesz! (A küldéshez használt, "A" betűs App tokenek ide nem használhatók).
3. **KDE Plasma integráció (Kötelező a haranghoz):** Ahhoz, hogy a KDE Plasma megjegyezze az értesítéseket és betegye őket az előzmények közé, futtasd le ezt a parancsot a terminálban. Ez létrehoz egy láthatatlan asztali bejegyzést, amit a KDE értesítési rendszere hivatalos alkalmazásként fog felismerni:
   ```bash
   cat <<EOF > ~/.local/share/applications/Gotify-DebianServer.desktop
   [Desktop Entry]
   Name=Gotify-DebianServer
   Type=Application
   Icon=network-server
   NoDisplay=true
   EOF
   ```

## 🔄 Automatikus indítás beállítása (Autostart)
Ahhoz, hogy a gép bekapcsolásakor a háttérben azonnal induljon a kliens:

1. Adj futtatási jogot a fájlnak a mappájában:
   ```bash
   chmod +x gotify-tray.py
   ```
2. Lépj be a **Rendszerbeállítások -> Automatikus indítás** (System Settings -> Autostart) menübe.
3. Kattints a **Szkript hozzáadása** (Add Login Script) gombra.
4. Tallózd ki a `gotify-tray.py` fájlt.

## 📝 Naplózás (Logging)
Mivel a script a háttérben fut, a beépített naplózó minden eseményt (kapcsolódás, ping, üzenet érkezése, hálózati hibák) a script mellett létrejövő `gotify-tray.log` fájlba rögzít. Ha bármi probléma adódna a kapcsolattal, ebben a fájlban másodpercre pontosan visszanézheted az eseményeket.

---

<a name="-english-version"></a>
# 🇬🇧 Gotify Desktop Tray Client (Linux / KDE Plasma)

A lightweight, Python-based tray application that connects to your Gotify server via WebSocket and displays incoming messages in real-time as native Linux notifications (`notify-send`).

The client is specifically optimized for the KDE Plasma desktop environment (runs perfectly on distros like Nobara Linux), ensuring seamless integration into the system's notification center.

## ✨ Features
* **Real-time notifications:** Instant push messages from the Gotify server through the open WebSocket channel.
* **KDE Notification Center integration:** Messages don't just pop up; they are saved in the notification history (under the bell icon), so you can read them later.
* **Dynamic tray icon:** Color/gray status indicator for connection status (Online/Offline).
* **Quick access:** Left-clicking the tray icon instantly opens the Gotify web interface in your default browser.
* **Custom application name:** The notification header displays `Gotify-DebianServer` instead of a generic command name.
* **Self-healing connection:** In case of a network drop, inactivity, or server restart, the client automatically attempts to reconnect.

## 🛠️ Prerequisites
Requires Python 3 and the system's native notification service.

**System packages:**
```bash
sudo dnf install libnotify
```

**Python packages:**
```bash
pip install websocket-client pystray Pillow
```

## 🚀 Setup and Usage

1. **Prepare files:** Clone the repo, or place the `gotify-tray.py` file and its `gotify-logo.png` icon in a folder.
2. **Set Token and URL:** Open `gotify-tray.py` in a text editor and change the server URL and your token.
   > ⚠️ **Important:** You need to generate a new token in the **Clients** menu on the Gotify web interface. This will be a token starting with the letter **`C`**! ("A" App tokens used for sending cannot be used here).
3. **KDE Plasma integration (Required for the history):** To make KDE Plasma remember the notifications and put them in the history, run this command in the terminal. This creates a hidden desktop entry that the KDE notification system will recognize as an official application:
   ```bash
   cat <<EOF > ~/.local/share/applications/Gotify-DebianServer.desktop
   [Desktop Entry]
   Name=Gotify-DebianServer
   Type=Application
   Icon=network-server
   NoDisplay=true
   EOF
   ```

## 🔄 Autostart Setup
To have the client start automatically in the background when the computer boots:

1. Grant execution rights to the file:
   ```bash
   chmod +x gotify-tray.py
   ```
2. Go to **System Settings -> Autostart**.
3. Click the **Add Login Script** button.
4. Browse and select the `gotify-tray.py` file.

## 📝 Logging
Since the script runs in the background, the built-in logger records every event (connection, ping, incoming messages, network errors) into a `gotify-tray.log` file created next to the script. If there are any connection issues, you can check this file for a precise timeline of events.
