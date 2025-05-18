// static/js/dashboard_update.js

function updateStatus() {
    fetch('/api/status')
      .then(response => response.json())
      .then(data => {
          // CO2-Wert
          let co2 = data.co2_current !== null ? data.co2_current : '---';
          let co2El = document.getElementById('co2_value');
          if (co2El) co2El.textContent = co2 + " ppm";

          // CO2 Last Update
          let co2LastUpdate = data.last_update || '--:--';
          let co2LastUpdateEl = document.getElementById('co2_last_update');
          if (co2LastUpdateEl) co2LastUpdateEl.textContent = co2LastUpdate;

          // Personenanzahl
          let persons = data.abs_persons !== null ? data.abs_persons : '--';
          let personsEl = document.getElementById('person_count');
          if (personsEl) personsEl.textContent = persons;

          // Personen Last Update
          let personLastUpdate = data.last_person_update || '--:--';
          let personLastUpdateEl = document.getElementById('person_last_update');
          if (personLastUpdateEl) personLastUpdateEl.textContent = personLastUpdate;

          // Luftqualität Badge
          let q = data.airing_quality || data.air_quality; // Fallback
          let badgeEl = document.getElementById('air_quality_badge');
          if (badgeEl) {
              if (q === "good") {
                  badgeEl.innerHTML = '<span class="badge bg-success">Gut</span>';
              } else if (q === "bad") {
                  badgeEl.innerHTML = '<span class="badge bg-danger">Schlecht</span>';
              } else {
                  badgeEl.innerHTML = '<span class="badge bg-secondary"></span>';
              }
          }

          // Luftqualität Last Update
          let airQualityUpdate = data.air_quality_update || '--:--';
          let airQualityUpdateEl = document.getElementById('air_quality_update');
          if (airQualityUpdateEl) airQualityUpdateEl.textContent = airQualityUpdate;

          // Lüften: Zuletzt gelüftet (falls verwendet)
          let lastAiring = data.last_airing || '--:--';
          let lastAiringEl = document.getElementById('last_airing');
          if (lastAiringEl) lastAiringEl.textContent = lastAiring;

          // Lüften: Letztes Lüften-Update (falls verwendet)
          let lastAiringUpdate = data.last_airing_update || '--:--';
          let lastAiringUpdateEl = document.getElementById('last_airing_update');
          if (lastAiringUpdateEl) lastAiringUpdateEl.textContent = lastAiringUpdate;

      })
      .catch(error => {
          console.error('Fehler beim Laden der Statusdaten:', error);
      });
}

setInterval(updateStatus, 1000);
window.onload = updateStatus;
