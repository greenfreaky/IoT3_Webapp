// static/js/dashboard_update.js

/**
 * @typedef {Object} StatusData
 * @property {number|null} co2_current
 * @property {string} last_update
 * @property {number|null} abs_persons
 * @property {string} last_person_update
 * @property {string} [airing_quality]
 * @property {string} [air_quality]
 * @property {string} air_quality_update
 * @property {string} last_airing
 * @property {string} last_airing_update
 * @property {string} mode
 */

const DEFAULTS = {
    co2: '---',
    time: '--:--',
    persons: '--'
};

function setTextById(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

function updateCardClass(card, classesToRemove, classesToAdd) {
    if (card) {
        card.classList.remove(...classesToRemove);
        card.classList.add(...classesToAdd);
    }
}

async function updateStatus() {
    const response = await fetch('/api/status');
    if (response.ok) {
        /** @type {StatusData} */
        const data = await response.json();

        // CO2-Wert
        setTextById('co2_value', (data.co2_current ?? DEFAULTS.co2) + " ppm");
        setTextById('co2_last_update', data.last_update ?? DEFAULTS.time);

        // Personenanzahl
        setTextById('person_count', data.abs_persons ?? DEFAULTS.persons);
        setTextById('person_last_update', data.last_person_update ?? DEFAULTS.time);

        // Luftqualität Badge
        const airQuality = data.airing_quality ?? data.air_quality;
        const airQualityCard = document.getElementById('air_quality_card');
        updateCardClass(
            airQualityCard,
            ['bg-success', 'bg-danger', 'text-white', 'text-dark'],
            airQuality === "good"
                ? ['bg-success', 'text-white']
                : airQuality === "bad"
                    ? ['bg-danger', 'text-white']
                    : []
        );
        setTextById('air_quality_update', data.air_quality_update ?? DEFAULTS.time);

        // Lüften
        setTextById('last_airing', data.last_airing ?? DEFAULTS.time);
        setTextById('last_airing_update', data.last_airing_update ?? DEFAULTS.time);

        // Modus-Kachel
        const mode = data.mode;
        const modeCard = document.getElementById('mode_card');
        updateCardClass(
            modeCard,
            ['bg-success', 'bg-info', 'bg-purple', 'text-white', 'text-dark'],
            mode === "auto"
                ? ['bg-info', 'text-light']
                : mode === "manuell"
                    ? ['bg-purple', 'text-light']
                    : []
        );
        setTextById('mode_value', mode === "auto" ? "Automatik" : "Manuell");

    } else {
        // Hier kein throw/catch, sondern direkte Fehlerbehandlung:
        console.error('Fehler beim Laden der Statusdaten:', response.status, response.statusText);
    }
}

// Regelmäßiges Update alle Sekunde
setInterval(updateStatus, 1000);
// Initiales Update sofort ausführen
updateStatus();
