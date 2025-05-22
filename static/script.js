
const tempLabels = [], humLabels = [], presLabels = [];
const tempData = [], humData = [], presData = [];

const chartTemp = new Chart(document.getElementById('chartTemp').getContext('2d'), {
    type: 'line',
    data: {
        labels: tempLabels,
        datasets: [{
            label: 'Temperatura (°C)',
            data: tempData,
            borderColor: 'red',
            tension: 0.3,
            fill: true
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                type: 'time',
                time: { unit: 'minute', displayFormats: { minute: 'HH:mm' } }
            }
        }
    }
});

const chartHum = new Chart(document.getElementById('chartHum').getContext('2d'), {
    type: 'line',
    data: {
        labels: humLabels,
        datasets: [{
            label: 'Humedad (%)',
            data: humData,
            borderColor: 'blue',
            tension: 0.3,
            fill: true
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                type: 'time',
                time: { unit: 'minute', displayFormats: { minute: 'HH:mm' } }
            }
        }
    }
});

const chartPres = new Chart(document.getElementById('chartPres').getContext('2d'), {
    type: 'line',
    data: {
        labels: presLabels,
        datasets: [{
            label: 'Presión (hPa)',
            data: presData,
            borderColor: 'green',
            tension: 0.3,
            fill: true
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                type: 'time',
                time: { unit: 'minute', displayFormats: { minute: 'HH:mm' } }
            }
        }
    }
});

function aplicarAlertas(data) {
    document.getElementById("card-temp").classList.toggle("alert", data.temperatura > 35);
    document.getElementById("card-mq").classList.toggle("alert", data.mq135 > 1000);
    document.getElementById("card-lluvia").classList.toggle("alert", data.lluvia < 1000);
}

async function actualizarDatos() {
    const res = await fetch('/api/datos');
    const data = await res.json();
    if (!data.timestamp) return;

    document.getElementById("timestamp").textContent = data.timestamp;
    document.getElementById("temp").textContent = data.temperatura;
    document.getElementById("hum").textContent = data.humedad;
    document.getElementById("pres").textContent = data.presion;
    document.getElementById("mq").textContent = data.mq135;
    document.getElementById("lluvia").textContent = data.lluvia;

    document.getElementById("min-temp").textContent = data.min_max.temperatura[0];
    document.getElementById("max-temp").textContent = data.min_max.temperatura[1];
    document.getElementById("min-hum").textContent = data.min_max.humedad[0];
    document.getElementById("max-hum").textContent = data.min_max.humedad[1];
    document.getElementById("min-pres").textContent = data.min_max.presion[0];
    document.getElementById("max-pres").textContent = data.min_max.presion[1];
    document.getElementById("min-mq").textContent = data.min_max.mq135[0];
    document.getElementById("max-mq").textContent = data.min_max.mq135[1];
    document.getElementById("min-lluvia").textContent = data.min_max.lluvia[0];
    document.getElementById("max-lluvia").textContent = data.min_max.lluvia[1];

    aplicarAlertas(data);

    const t = data.timestamp;

    tempLabels.push(t);
    humLabels.push(t);
    presLabels.push(t);

    tempData.push(data.temperatura);
    humData.push(data.humedad);
    presData.push(data.presion);

    const limite = 60;
    if (tempLabels.length > limite) {
        tempLabels.shift(); tempData.shift();
        humLabels.shift(); humData.shift();
        presLabels.shift(); presData.shift();
    }

    chartTemp.update();
    chartHum.update();
    chartPres.update();
}

setInterval(actualizarDatos, 5000);
actualizarDatos();

document.getElementById("comparador").addEventListener("submit", async function (e) {
    e.preventDefault();

    const desde1 = e.target.desde1.value;
    const hasta1 = e.target.hasta1.value;
    const desde2 = e.target.desde2.value;
    const hasta2 = e.target.hasta2.value;

    const [r1, r2] = await Promise.all([
        fetch(`/api/datos?desde=${desde1}&hasta=${hasta1}`).then(res => res.json()),
        fetch(`/api/datos?desde=${desde2}&hasta=${hasta2}`).then(res => res.json())
    ]);

    const prom = arr => arr.length ? (arr.reduce((a, b) => a + b) / arr.length).toFixed(2) : 'N/A';

    const prom1 = {
        temp: prom(r1.map(d => d.temperatura)),
        hum: prom(r1.map(d => d.humedad)),
        pres: prom(r1.map(d => d.presion))
    };

    const prom2 = {
        temp: prom(r2.map(d => d.temperatura)),
        hum: prom(r2.map(d => d.humedad)),
        pres: prom(r2.map(d => d.presion))
    };

    document.getElementById("resultado-comparacion").innerHTML = `
    <h4>📊 Resultados comparativos</h4>
    <table style="margin:auto; border-collapse: collapse;">
      <tr><th></th><th>Periodo 1</th><th>Periodo 2</th></tr>
      <tr><td>Temperatura</td><td>${prom1.temp}</td><td>${prom2.temp}</td></tr>
      <tr><td>Humedad</td><td>${prom1.hum}</td><td>${prom2.hum}</td></tr>
      <tr><td>Presión</td><td>${prom1.pres}</td><td>${prom2.pres}</td></tr>
    </table>
  `;
});

function mostrarComparacion() {
    const seccion = document.getElementById("seccion-comparacion");
    seccion.style.display = (seccion.style.display === "none") ? "block" : "none";
}

function mostrarComparacion() {
    const seccion = document.getElementById("seccion-comparacion");
    const boton = document.getElementById("boton-comparar");
    const visible = seccion.style.display === "block";

    seccion.style.display = visible ? "none" : "block";
    boton.textContent = visible ? "📊 Comparar dos fechas" : "🔽 Ocultar comparación";
}

document.getElementById("comparador").addEventListener("submit", async function (e) {
    e.preventDefault();

    const desde1 = e.target.desde1.value;
    const hasta1 = e.target.hasta1.value;
    const desde2 = e.target.desde2.value;
    const hasta2 = e.target.hasta2.value;

    const [r1, r2] = await Promise.all([
        fetch(`/api/datos?desde=${desde1}&hasta=${hasta1}`).then(res => res.json()),
        fetch(`/api/datos?desde=${desde2}&hasta=${hasta2}`).then(res => res.json())
    ]);

    const prom = arr => arr.length ? (arr.reduce((a, b) => a + b) / arr.length).toFixed(2) : 'N/A';

    const prom1 = {
        temp: prom(r1.map(d => d.temperatura)),
        hum: prom(r1.map(d => d.humedad)),
        pres: prom(r1.map(d => d.presion))
    };

    const prom2 = {
        temp: prom(r2.map(d => d.temperatura)),
        hum: prom(r2.map(d => d.humedad)),
        pres: prom(r2.map(d => d.presion))
    };

    document.getElementById("resultado-comparacion").innerHTML = `
      <h4>📊 Resultados comparativos</h4>
      <table style="margin:auto; border-collapse: collapse;">
        <tr><th></th><th>Periodo 1</th><th>Periodo 2</th></tr>
        <tr><td>Temperatura</td><td>${prom1.temp}</td><td>${prom2.temp}</td></tr>
        <tr><td>Humedad</td><td>${prom1.hum}</td><td>${prom2.hum}</td></tr>
        <tr><td>Presión</td><td>${prom1.pres}</td><td>${prom2.pres}</td></tr>
      </table>
    `;
});
