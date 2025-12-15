#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Arduino.h>

BLEServer *pServer = NULL;
BLECharacteristic *pCharacteristic = NULL;

#define SERVICE_UUID        "12345678-1234-1234-1234-123456789012"
#define CHARACTERISTIC_UUID "87654321-4321-4321-4321-210987654321"

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
  // Do nothing here
}