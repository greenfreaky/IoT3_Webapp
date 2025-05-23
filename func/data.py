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
    "reminder_notification": 30,
    "airing_now": False,
    "last_airing": None,
    "last_update": None,
    "last_person_update": None,
    "air_quality": None,
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
        status["mode"] = "manuel" if status["mode"] == "auto" else "auto"
        print(f"[data.py][DEBUG] Modus umgeschaltet auf: {status['mode']}")

def set_mode(value):
    with status_lock:
        if value in ["auto", "manuel"]:
            status["mode"] = value
            print(f"[data.py][DEBUG] Modus explizit gesetzt auf: {status['mode']}")

def set_airing_now(is_airing):
    with status_lock:
        status["airing_now"] = bool(is_airing)
        if is_airing:
            status["last_airing_update"] = datetime.now().strftime("%H:%M:%S")
        print(f"[data.py][DEBUG] Lüften gesetzt: {status['airing_now']} (Letzte Lüftung: {status['last_airing']})")

def set_air_quality(value):
    with status_lock:
        status["air_quality"] = value
        status["air_quality_update"] = datetime.now().strftime("%H:%M:%S")
        print(f"[data.py][DEBUG] Luftqualität gesetzt: {status['air_quality']} (Stand: {status['air_quality_update']})")

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

def get_air_quality():
    with status_lock:
        print("[data.py][DEBUG] Luftqualität abgefragt:", status["air_quality"])
        return status["air_quality"]
