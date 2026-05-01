# Gotify Desktop Tray Client (Linux / KDE Plasma)
Egy pehelysúlyú, Python alapú tálcaalkalmazás (tray app), amely WebSocketen keresztül kapcsolódik a Gotify szerveredhez, és valós időben, natív Linux értesítésekként (notify-send) jeleníti meg a beérkező üzeneteket.

A kliens kifejezetten KDE Plasma asztali környezetre lett optimalizálva (tökéletesen fut pl. Nobara Linuxon), így hibátlanul integrálódik a rendszer értesítési központjába.

✨ Funkciók
Valós idejű értesítések: Azonnali push üzenetek a Gotify szervertől a megnyitott WebSocket csatornán keresztül.
KDE Értesítési Központ integráció: Az üzenetek nem csak felugranak, hanem be is kerülnek az értesítési előzményekbe (a harang ikon alá), így később is bármikor visszaolvashatók.
Dinamikus tálca ikon: Zöld/szürke állapotjelző a kapcsolat státuszáról (Online/Offline).
Gyors elérés: A tálcaikonra bal gombbal kattintva azonnal megnyílik a Gotify webes felülete az alapértelmezett böngésződben.
Egyedi alkalmazásnév: Az értesítések fejlécében a Gotify-DebianServer név jelenik meg az egyszerű parancsnév helyett.
Öngyógyító kapcsolat: Hálózati szakadás, tétlenség vagy szerver újraindulás esetén a kliens automatikusan próbál újracsatlakozni.
🛠️ Előfeltételek
A futtatáshoz Python 3-ra és a rendszer natív értesítő szolgáltatására van szükség.

Rendszercsomagok:

sudo dnf install libnotify
Python csomagok telepítése:

Bash
pip install websocket-client pystray Pillow
🚀 Beállítás és Használat
Fájlok előkészítése:
Klónozd a repót, vagy tedd egy mappába a gotify-tray.py fájlt és a hozzá tartozó
gotify-logo.png ikont.

Token és URL beállítása:
Nyisd meg a gotify-tray.py fájlt egy szövegszerkesztőben, és írd át a szerver
URL-jét, illetve a tokenedet.

⚠️ Fontos: A Gotify webes felületén a Clients (Kliensek) menüben kell új tokent
generálnod. Ez egy C betűvel kezdődő token lesz! (A küldéshez használt, "A"
betűs App tokenek ide nem használhatók).

KDE Plasma integráció (Kötelező a haranghoz):
Ahhoz, hogy a KDE Plasma megjegyezze az értesítéseket és betegye őket az előzmények
közé, futtasd le ezt a parancsot a terminálban. Ez létrehoz egy láthatatlan asztali
bejegyzést, amit a KDE értesítési rendszere hivatalos alkalmazásként fog felismerni:

Bash
cat <<EOF > ~/.local/share/applications/Gotify-DebianServer.desktop
[Desktop Entry]
Name=Gotify-DebianServer
Type=Application
Icon=network-server
NoDisplay=true
EOF
🔄 Automatikus indítás beállítása (Autostart)
Ahhoz, hogy a gép bekapcsolásakor a háttérben azonnal induljon a kliens:

Adj futtatási jogot a fájlnak a mappájában: chmod +x gotify-tray.py

Lépj be a Rendszerbeállítások -> Automatikus indítás (System Settings -> Autostart) menübe.

Kattints a Szkript hozzáadása (Add Login Script) gombra.

Tallózd ki a gotify-tray.py fájlt.

📝 Naplózás (Logging)
Mivel a script a háttérben fut, a beépített naplózó minden eseményt (kapcsolódás, ping,
üzenet érkezése, hálózati hibák) a script mellett létrejövő gotify-tray.log fájlba rögzít.
Ha bármi probléma adódna a kapcsolattal, ebben a fájlban másodpercre pontosan visszanézheted
az eseményeket.
