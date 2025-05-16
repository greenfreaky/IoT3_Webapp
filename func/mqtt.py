import paho.mqtt.client as mqtt
import ssl
from data import set_co2, set_persons, set_state_window

# HiveMQ Cloud Settings
MQTT_BROKER = "31922db804d245f0857ddb0761ec6fdb.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "room_A1.02"
MQTT_PASSWORD = "HelloWorld!1"

TOPIC_CO2 = "raum1/co2"
TOPIC_PERSONS = "raum1/persons"
TOPIC_WINDOW = "raum1/window"

def on_connect(client, userdata, flags, rc):
    print(f"[mqtt.py][DEBUG] on_connect aufgerufen mit rc={rc}")
    if rc == 0:
        print("[mqtt.py][DEBUG] Verbindung zu MQTT-Broker erfolgreich!")
        client.subscribe(TOPIC_CO2)
        client.subscribe(TOPIC_PERSONS)
        client.subscribe(TOPIC_WINDOW)
        print(f"[mqtt.py][DEBUG] Subscribed zu Topics: {TOPIC_CO2}, {TOPIC_PERSONS}, {TOPIC_WINDOW}")
    else:
        print(f"[mqtt.py][ERROR] Verbindung fehlgeschlagen! Return Code: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    print(f"[mqtt.py][DEBUG] Nachricht empfangen - Topic: {msg.topic}, Payload: {payload}")
    if msg.topic == TOPIC_CO2:
        try:
            set_co2(float(payload))
        except Exception as e:
            print("[mqtt.py][ERROR] Fehler beim Setzen von CO2:", e)
    elif msg.topic == TOPIC_PERSONS:
        try:
            set_persons(int(payload))
        except Exception as e:
            print("[mqtt.py][ERROR] Fehler beim Setzen der Personenanzahl:", e)
    elif msg.topic == TOPIC_WINDOW:
        set_state_window(payload.strip().lower() == "open")
    else:
        print(f"[mqtt.py][WARN] Unbekanntes Topic empfangen: {msg.topic}")

def main():
    print("[mqtt.py][DEBUG] MQTT-Client wird erstellt...")
    client = mqtt.Client()
    print("[mqtt.py][DEBUG] Benutzername/Passwort werden gesetzt...")
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    print("[mqtt.py][DEBUG] TLS wird konfiguriert...")
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_message = on_message
    print(f"[mqtt.py][DEBUG] Verbinde mit Broker: {MQTT_BROKER}:{MQTT_PORT} ...")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("[mqtt.py][DEBUG] Verbindung zu MQTT-Broker initiiert.")
    except Exception as e:
        print(f"[mqtt.py][ERROR] Verbindungsaufbau zum Broker fehlgeschlagen: {e}")
        return
    print("[mqtt.py][DEBUG] Starte Netzwerk-Loop (loop_forever)...")
    client.loop_forever()