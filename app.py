from flask import Flask, render_template, redirect, url_for, request
import threading
from func import data
from func import mqtt

app = Flask(__name__)

@app.route('/')
def index():
    status = data.get_status()
    return render_template(
        "index.html",
        site_title="IoT Smart Airing Dashboard",
        co2_current=status["co2_current"],
        abs_persons=status["abs_persons"],
        mode=status["mode"],
        airing_now=status["airing_now"],
        last_airing=status["last_airing"],
        last_update=status["last_update"],
        last_person_update=status["last_person_update"],
    )

@app.route('/toggle_mode', methods=['POST'])
def toggle_mode():
    data.toggle_mode()
    return redirect(url_for('index'))

@app.route('/air_now', methods=['POST'])
def air_now():
    # Nur wenn nicht schon am Lüften und Modus manuell!
    if not data.get_airing_now() and data.get_mode() == "manuell":
        data.set_airing_now(True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Starte den MQTT-Thread als Daemon
    mqtt_thread = threading.Thread(target=mqtt.main, daemon=True)
    mqtt_thread.start()
    # Dann Flask starten
    app.run(debug=True, use_reloader=False)
