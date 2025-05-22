#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SDA_PIN 21
#define SCL_PIN 22

#define MQ135_PIN 34
#define RAIN_PIN 35

const char* ssid = "*********";          // <-- Cambia esto
const char* password = "**********";  // <-- Cambia esto

const char* mqtt_server = "**.**.**.**"; // <-- Cambia esto
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_BME280 bme;

unsigned long lastMsg = 0;
char msg[256];

void conectarWiFi() {
  delay(10);
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado");
  Serial.println(WiFi.localIP());
}

void conectarMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando al broker MQTT...");
    if (client.connect("ESP32Estacion")) {
      Serial.println("conectado ✅");
    } else {
      Serial.print("falló ❌, rc=");
      Serial.print(client.state());
      Serial.println(" intentando de nuevo en 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  // Conexión WiFi primero
  conectarWiFi();

  // MQTT
  client.setServer(mqtt_server, mqtt_port);

  // I2C después del WiFi
  Wire.begin(SDA_PIN, SCL_PIN);

  // Sensor BME280
  Serial.println("Inicializando BME280...");
  if (!bme.begin(0x76)) {
    Serial.println("❌ No se detectó el BME280");
    while (1);
  }

  pinMode(MQ135_PIN, INPUT);
  pinMode(RAIN_PIN, INPUT);
}


void loop() {
  if (!client.connected()) {
    conectarMQTT();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 5000) {  // cada 5 segundos
    lastMsg = now;

    float temp = bme.readTemperature();
    float hum = bme.readHumidity();
    float pres = bme.readPressure() / 100.0F;
    int gas = analogRead(MQ135_PIN);
    int lluvia = analogRead(RAIN_PIN);

    snprintf(msg, sizeof(msg),
      "{\"temperatura\":%.2f,\"humedad\":%.2f,\"presion\":%.2f,\"mq135\":%d,\"lluvia\":%d}",
      temp, hum, pres, gas, lluvia);

    Serial.println("Enviando:");
    Serial.println(msg);

    client.publish("sensores/estacion", msg);
  }
}
