# 🛠️ Manual de Instalación – Sentinel-WX-Alpha

Este documento describe cómo desplegar la estación meteorológica desde cero en una Raspberry Pi (o servidor Linux).

---

## 📦 Requisitos

- Raspberry Pi con Raspberry Pi OS actualizado
- Conexión a internet
- Python 3.10+
- PostgreSQL
- Mosquitto MQTT Broker
- Git

---

## 🔧 Paso 1: Instalar dependencias del sistema

```bash
sudo apt update && sudo apt install -y \
  python3 python3-pip python3-venv git \
  mosquitto mosquitto-clients \
  postgresql postgresql-contrib
```

---

## 🔧 Paso 2: Clonar el repositorio

```bash
git clone https://github.com/EXTRANFUNEDGAR/Sentinel-WX-Alpha.git
cd Sentinel-WX-Alpha
```

---

## 🔧 Paso 3: Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Paso 4: Configurar variables de entorno

Crea el archivo `.env` en la raíz:

```env
TELEGRAM_TOKEN=TU_TOKEN_DEL_BOT
```

---

## 🗃️ Paso 5: Crear base de datos PostgreSQL

```bash
sudo -u postgres psql
```

Dentro de PostgreSQL:

```sql
CREATE DATABASE estacion;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE estacion TO postgres;
\q
```

Luego crea la tabla:

```sql
\c estacion
CREATE TABLE sensores (
  timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  temperatura REAL,
  humedad REAL,
  presion REAL,
  mq135 INTEGER,
  lluvia INTEGER
);
```

---

## 🚀 Paso 6: Probar servicios manualmente

Desde la raíz del proyecto:

```bash
source venv/bin/activate
python3 mqtt_guardar.py     # Guarda datos de MQTT
python3 app.py              # Dashboard Flask
python3 bot/telegram_bot.py # Bot de Telegram
```

---

## ⚙️ Paso 7: Habilitar servicios systemd

### 1. Crea archivos de servicio en `/etc/systemd/system/`:

Ejemplo: `telegrambot.service`

```ini
[Unit]
Description=Bot de Telegram
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/Sentinel-WX-Alpha
ExecStart=/home/pi/Sentinel-WX-Alpha/venv/bin/python3 /home/pi/Sentinel-WX-Alpha/bot/telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Haz lo mismo para `app.py` y `mqtt_guardar.py`

### 2. Habilita y arranca los servicios

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegrambot
sudo systemctl enable flask_dashboard
sudo systemctl enable mqtt_guardar

sudo systemctl start telegrambot
sudo systemctl start flask_dashboard
sudo systemctl start mqtt_guardar
```

---

## 📡 Paso 8: Conectar el ESP32

Asegúrate de que el ESP32 esté conectado a la red local y que esté configurado para publicar datos a:

```
broker: <IP_LOCAL_RPI>
topic: estacion/datos
```

---

## ✅ Final

- Accede al dashboard desde navegador: `http://<IP_LOCAL_RPI>:5000`
- En Telegram: usa `/datos` con tu bot

---

