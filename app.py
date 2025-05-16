from flask import Flask, render_template, redirect, url_for
import data
import mqtt

from datetime import datetime

app = Flask(__name__)

# Starte den MQTT-Client
mqtt.start()

@app.route('/')
def index():
    status = data.get_status()
    return render_template(
        'index.html',
        co2_current=status['co2_current'],
        last_update=status['last_update'],
        abs_persons=status['abs_persons'],
        last_person_update=status['last_person_update'],
        mode=status['mode'],
        airing_now=status['airing_now'],
        last_airing=status['last_airing']
    )

@app.route('/toggle_mode', methods=['POST'])
def toggle_mode():
    data.toggle_mode()
    return redirect(url_for('index'))

@app.route('/air_now', methods=['POST'])
def air_now():
    # Lüften nur, wenn nicht automatisch und aktuell nicht am Lüften
    status = data.get_status()
    if not status['airing_now'] and status['mode'] == 'manuell':
        data.set_airing_now(True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # KEIN debug=True!
    app.run(host="0.0.0.0", port=5000, debug=False)
