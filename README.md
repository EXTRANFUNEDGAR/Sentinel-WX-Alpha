# 🌦️ Sentinel-WX-Alpha

**Sentinel-WX-Alpha** es una estación meteorológica completa desarrollada con:

- 📟 ESP32 + sensores (BME280, MQ-135, Raindrop)
- 🌐 Comunicación vía MQTT
- 🐍 Backend en Python con Flask + PostgreSQL
- 📊 Dashboard web en tiempo real
- 🤖 Bot de Telegram con comandos `/datos`
- 🗂️ Exportación a CSV por rango de fechas
- 🛠️ Servicios systemd para ejecución automática al iniciar

---

## 🧱 Estructura del Proyecto

```
flask_dashboard/
├── app.py                  # Servidor web Flask
├── mqtt_guardar.py         # Guarda datos de MQTT en PostgreSQL
├── bot/
│   └── telegram_bot.py     # Bot de Telegram
├── templates/
│   └── dashboard.html      # Dashboard web
├── .env                    # Variables sensibles (token, DB)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```

---

## 🚀 Requisitos

- Python 3.10+
- PostgreSQL
- Mosquitto MQTT
- Entorno virtual (`venv`)

---
## 📚 Documentación

Consulta la documentación completa y manual de instalación en:

➡️ [`docs/manual_instalacion.md`](docs/manual_instalacion.md)

Incluye pasos desde cero, configuración del ESP32, servicios, y despliegue completo.

## 🧠 Uso

### 1. Ejecutar el servidor Flask:

```bash
python3 app.py
```

### 2. Ejecutar el bot de Telegram:

```bash
python3 bot/telegram_bot.py
```

### 3. Ejecutar el guardado desde MQTT:

```bash
python3 mqtt_guardar.py
```

O usa servicios systemd para que se inicien automáticamente.

---

## 📬 Comandos disponibles en Telegram

El sistema incluye un bot de Telegram con soporte para:

| Comando     | Descripción                                                  |
|-------------|--------------------------------------------------------------|
| `/start`    | Muestra un mensaje de bienvenida.                            |
| `/datos`    | Devuelve los datos actuales de todos los sensores.           |
| `/estado`   | Muestra alertas activas junto con sus valores actuales.      |
| `/id`       | Obteber tu caht_id                                           |

---

### 🔔 Alertas automáticas

El bot revisa los sensores cada 10 segundos y enviará una alerta **solo una vez** por cada condición crítica. Se reactivará si el valor se normaliza y luego vuelve a superar el umbral.

Las condiciones actuales para activar alertas son:

- `MQ-135 > 300`  
- `Temperatura > 35 °C`  
- `Lluvia < 2000` (valor analógico del sensor Raindrop)


## 📦 Exportar datos

Desde la web puedes elegir un rango de fechas y exportar un archivo `.csv`.

---

## 📊 Dashboard en tiempo real

- Gráficas de temperatura, humedad y presión
- Alertas visuales si MQ135 o lluvia exceden límites
- Comparación de dos periodos seleccionados

---


## 🛠️ Autor

Proyecto desarrollado por [Edgar Enrique Delgado Sánchez](https://github.com/EXTRANFUNEDGAR)
 

---
