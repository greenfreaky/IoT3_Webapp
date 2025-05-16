import paho.mqtt.client as mqtt
import ssl
import data
import json

# HiveMQ Cloud Settings
MQTT_BROKER = "31922db804d245f0857ddb0761ec6fdb.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "room_A1.02"
MQTT_PASSWORD = "HelloWorld!1"

TOPIC_CO2 = "room1/co2"
TOPIC_PERSONS = "room1/persons"
TOPIC_WINDOW = "room1/window"

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
            # Wenn payload JSON ist (z.B. '{"co2": 418.2}')
            try:
                data_json = json.loads(payload)
                co2_value = data_json.get("co2")
            except Exception:
                # Oder: payload ist nur eine Zahl (z. B. "418.2")
                co2_value = float(payload)
            if co2_value is not None:
                data.set_co2(co2_value)
        except Exception as e:
            print("[mqtt.py][ERROR] Fehler beim Setzen von CO2:", e)

    elif msg.topic == TOPIC_PERSONS:
        try:
            # Wenn payload JSON ist (z.B. '{"anzahl": 5}')
            try:
                data_json = json.loads(payload)
                persons = data_json.get("anzahl")
            except Exception:
                # Oder: payload ist nur eine Zahl (z. B. "5")
                persons = int(payload)
            if persons is not None:
                data.set_persons(persons)
        except Exception as e:
            print("[mqtt.py][ERROR] Fehler beim Setzen der Personenanzahl:", e)

    elif msg.topic == TOPIC_WINDOW:
        # Window-Payload erwartet z.B. "open" oder "closed"
        data.set_state_window(payload.strip().lower() == "open")
    else:
        print(f"[mqtt.py][WARN] Unbekanntes Topic empfangen: {msg.topic}")

# **Achtung! Der Client muss im Hintergrund laufen, wenn Flask läuft**
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

def start():
    try:
        print(f"[mqtt.py][DEBUG] Verbinde mit Broker: {MQTT_BROKER}:{MQTT_PORT} ...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("[mqtt.py][DEBUG] Verbindung zu MQTT-Broker initiiert.")
        client.loop_start()  # Nicht loop_forever, damit Flask und MQTT gleichzeitig laufen!
    except Exception as e:
        print(f"[mqtt.py][ERROR] Verbindungsaufbau zum Broker fehlgeschlagen: {e}")
