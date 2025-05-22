# ⚡ Código y Conexiones – ESP32 Sentinel-WX-Alpha

Este módulo se encarga de leer los sensores y enviar los datos a la Raspberry Pi mediante MQTT.

---

## 🧠 Sensores conectados

### 📟 ESP32 Dev Module

- Plataforma: Arduino
- Comunicación: MQTT
- Baud rate: 115200
- Biblioteca usada para el BME280: `Adafruit_BME280`

---

## 📌 Pines usados

| Sensor       | Función   | ESP32 GPIO |
|--------------|-----------|------------|
| BME280       | SDA       | GPIO 21    |
| BME280       | SCL       | GPIO 22    |
| BME280       | VCC       | 3.3V       |
| BME280       | GND       | GND        |
| MQ-135       | AOUT      | GPIO 34    |
| MQ-135       | VCC       | 3.3V       |
| MQ-135       | GND       | GND        |
| Módulo lluvia| A0        | GPIO 35    |
| Módulo lluvia| VCC       | 3.3V       |
| Módulo lluvia| GND       | GND        |

---

## 🔁 Flujo de trabajo

1. El ESP32 lee cada 5 segundos:
   - Temperatura (°C)
   - Humedad (%)
   - Presión (hPa)
   - Valor analógico del MQ135
   - Nivel de lluvia

2. Publica los datos por MQTT a `topic: estacion/datos`

---

## 📂 Archivos

- `estacion_esp32.ino`: Código Arduino que se carga en el ESP32
- `README.md`: Este archivo
- `conexiones.jpg` (opcional): Imagen del diagrama de conexiones

---

## 📝 Notas

- MQ135 necesita unos minutos de calentamiento
- El valor del sensor de lluvia se interpreta como:
  - `>3000`: Seco
  - `1000-3000`: Lluvia leve
  - `<1000`: Lluvia fuerte

---

## 📦 Requisitos para compilar

- Arduino IDE 1.8+
- Placa "ESP32 Dev Module"
- Bibliotecas:
  - `Adafruit BME280`
  - `Adafruit Unified Sensor`
  - `PubSubClient`
  - `WiFi.h`

---

