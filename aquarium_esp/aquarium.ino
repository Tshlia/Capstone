#include <WiFi.h>
#include <PubSubClient.h>
#include <NewPing.h>

// Pin Ultrasonik (HC-SR04)
#define TRIGGER_PIN  2  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     4  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
  
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

// Pin pH Sensor (Analog)
const int pHpin = 34;   // GPIO34 (Analog ADC1_CH6)

// Variabel Kalibrasi pH (Sesuaikan dengan sensor Anda!)
float pHOffset = 0.0;   // Offset kalibrasi
float pHLinear = 1.0;   // Faktor linear (contoh: 3.5 * voltage + offset)

// Pin TDS Sensor
const int TDSpin = 35;

// Variabel Kalibrasi TDS
float TDSScale = 0.5;

// Konfigurasi WiFi
const char* ssid = "Rahasia";
const char* password = "kepoamatdah";

// Konfigurasi MQTT Broker (EMQX)
const char* mqtt_server = "broker.emqx.io"; // atau alamat IP broker EMQX Anda
const int mqtt_port = 1883;
const char* mqtt_user = ""; // kosongkan jika tidak ada autentikasi
const char* mqtt_pass = ""; // kosongkan jika tidak ada autentikasi
const char* mqtt_client_id = "esp32-aquarium-monitoring"; // ID unik untuk client

// Topik MQTT
const char* topic_distance = "sensor/ultrasonic/distance";
const char* topic_ph = "sensor/ph/value";
const char* topic_tds = "watermonitor/sensor/tds";
const char* topic_status = "watermonitor/status";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);  // Tambahan penting
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}



// void setup_wifi() {
//   delay(10);
//   Serial.println();
//   Serial.print("Connecting to ");
//   Serial.println(ssid);

//   WiFi.begin(ssid, password);

//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }

//   Serial.println("");
//   Serial.println("WiFi connected");
//   Serial.println("IP address: ");
//   Serial.println(WiFi.localIP());
// }

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    // Attempt to connect
    if (client.connect(mqtt_client_id, mqtt_user, mqtt_pass)) {
      Serial.println("connected");
      client.publish(topic_status, "ESP32 connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  // pH Sensor tidak perlu pinMode karena analog
  
  // Setup WiFi dan MQTT
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // ===== BACA SENSOR ULTRASONIK =====
  float distance = sonar.ping_cm();  // Konversi ke cm
  
  // ===== BACA SENSOR pH =====
  int pHraw = analogRead(pHpin);
  float voltage = pHraw * (3.3 / 4095.0);  // ESP32 ADC 12-bit (0-4095)
  float pHValue = 7.0 - ((voltage - 2.5) / 0.18);  // Rumus contoh (kalibrasi!)
  
  // === 3. READ TDS SENSOR ===
  int TDSraw = analogRead(TDSpin);
  float TDSvoltage = TDSraw * (3.3 / 4095.0);
  float TDSvalue = (133.42*pow(TDSvoltage,3) - 255.86*pow(TDSvoltage,2) + 857.39*TDSvoltage) * TDSScale;

  // ===== TAMPILKAN HASIL =====
  Serial.print("Jarak: ");
  Serial.print(distance);
  Serial.print(" cm | pH: ");
  Serial.print(pHValue, 2);
  Serial.print(" | TDS: ");
  Serial.print(TDSvalue, 2);
  Serial.println(" ppm");
  
  // ===== KIRIM DATA KE MQTT BROKER =====
  char payload[50];
  
  // Publish distance
  dtostrf(distance, 6, 2, payload);
  client.publish(topic_distance, payload);
  
  // Publish pH
  dtostrf(pHValue, 6, 2, payload);
  client.publish(topic_ph, payload);
  
  // Publish TDS
  dtostrf(TDSvalue, 6, 2, payload);
  client.publish(topic_tds, payload);

  delay(1000);  // Delay 1 detik
}