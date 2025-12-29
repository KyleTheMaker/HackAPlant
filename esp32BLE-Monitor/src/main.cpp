#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Arduino.h>

BLEServer *pServer = NULL;
BLECharacteristic *pCharacteristic = NULL;

#define SERVICE_UUID        "12345678-1234-1234-1234-123456789012"
#define CHARACTERISTIC_UUID "87654321-4321-4321-4321-210987654321"

const int thermPin = 32;
int thermValue;
float r1 = 10000;
float convLog, conversion, tempK, tempC;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

void setup() {
  Serial.begin(115200);
  
  // Initialize BLE
  BLEDevice::init("Hack-A-Plant-Monitor");
  pServer = BLEDevice::createServer();
  
  // Create a BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);
  
  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ |
                      BLECharacteristic::PROPERTY_WRITE
                    );
  
  // Start the service
  pService->start();
  
  // Start advertising
  pServer->getAdvertising()->start();
  Serial.println("BLE server is now advertising");
}

void loop() {
    //test Thermistor Readings
    thermValue = analogRead(thermPin);
    conversion = r1 * (4095.0 / (float)thermValue - 1.0);
    convLog = log(conversion);
    tempK = (1.0 / (c1 + c2*convLog + c3*convLog*convLog*convLog));
    tempC = tempK - 273.15;
    Serial.print("pin val: ");
    Serial.println(thermValue);
    Serial.print("Resistor Value: ");
    Serial.println(conversion);
    Serial.print("Temp Kelvin: ");
    Serial.println(tempK);
    Serial.print("Temp Celsius: ");
    Serial.println(tempC);

    delay(1500);
  // Do nothing here
}