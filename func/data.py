from datetime import datetime
import threading

# Thread-Safe Lock für Statusdaten
status_lock = threading.Lock()

status = {
    "co2_current": 420.0,
    "abs_persons": 3,
    "state_window": False,
    "mode": "auto",
    "permission_window": True,
    "remindering_notification": 30,
    "airing_now": False,
    "last_airing": None,
    "last_update": None,
    "last_person_update": None,
}

def get_status():
    with status_lock:
        print("[data.py][DEBUG] Status abgefragt:", status)
        return status.copy()

def set_co2(value):
    with status_lock:
        status["co2_current"] = float(value)
        status["last_update"] = datetime.now().strftime("%H:%M:%S")
        print(f"[data.py][DEBUG] CO2-Wert gesetzt: {status['co2_current']} ppm (Stand: {status['last_update']})")

def set_persons(value):
    with status_lock:
        status["abs_persons"] = int(value)
        status["last_person_update"] = datetime.now().strftime("%H:%M:%S")
        print(f"[data.py][DEBUG] Personenanzahl gesetzt: {status['abs_persons']} (Stand: {status['last_person_update']})")

def set_state_window(is_open):
    with status_lock:
        status["state_window"] = bool(is_open)
        print(f"[data.py][DEBUG] Fensterstatus gesetzt: {'offen' if status['state_window'] else 'geschlossen'}")

def toggle_mode():
    with status_lock:
        status["mode"] = "manuell" if status["mode"] == "auto" else "auto"
        print(f"[data.py][DEBUG] Modus umgeschaltet auf: {status['mode']}")

def set_mode(value):
    with status_lock:
        if value in ["auto", "manuell"]:
            status["mode"] = value
            print(f"[data.py][DEBUG] Modus explizit gesetzt auf: {status['mode']}")

def set_airing_now(is_airing):
    with status_lock:
        status["airing_now"] = bool(is_airing)
        if is_airing:
            status["last_airing"] = datetime.now().strftime("%H:%M:%S")
        print(f"[data.py][DEBUG] Lüften gesetzt: {status['airing_now']} (Letzte Lüftung: {status['last_airing']})")

def get_airing_now():
    with status_lock:
        print("[data.py][DEBUG] Status 'airing_now' abgefragt:", status["airing_now"])
        return status["airing_now"]

def get_mode():
    with status_lock:
        print("[data.py][DEBUG] Modus abgefragt:", status["mode"])
        return status["mode"]

def get_last_airing():
    with status_lock:
        print("[data.py][DEBUG] Letztes Lüften abgefragt:", status["last_airing"])
        return status["last_airing"]
