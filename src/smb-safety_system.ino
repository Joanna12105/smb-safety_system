/*
* Filename:         smb-safety_system.ino
* Description:      This Arduino program enables the communication between the Raspberry Pi and the Arduino.
                     It sets up the BLE communication on the Arduino side and controls the LEDs based on the
                     connection status and the data received from the Raspberry Pi.
* Author:           Joanna Rieger
* Bachelor thesis:  "Untersuchungen zum Einsatz von KI und Computer Vision für ein Fahrradassistenzsystem am Beispiel
                      eines rückwärtigen Abstands- und Annäherungswarners"
* E-Mail:           joanna.rieger@stud.hshl.de
* Project Sources:
    * Source:           https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi
    * Source:           https://colab.research.google.com/github/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/Train_TFLite2_Object_Detction_Model.ipynb
    * Source:           https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
    * Source:           https://www.welt.de/motor/news/article244937978/Jedes-Jahr-ein-Zentimeter-mehr-Laengenwachstum-bei-Pkw.html#:~:text=Zwischen%202000%20und%202022%20ist,von%20einem%20Zentimeter%20pro%20Jahr.
    * Source:           https://www.ardalpha.de/wissen/geschichte/kulturgeschichte/din-a4-din-normen-100-jahre-100.html#:~:text=Die%20wohl%20bekannteste%20DIN%2DNorm%20ist%20die%20DIN%20EN%20ISO,noch%20in%20den%20Drucker%20legen.
    * Source:           https://jashuang1983.wordpress.com/rpi4-ble-with-arduino-nano-33/
    * Source:           https://docs.arduino.cc/tutorials/nano-33-ble-sense/bluetooth/
    * Source:           https://github.com/OpenBluetoothToolbox/SimpleBLE/blob/main/examples/simplepyble/write.py
    * Source:           https://blog.finxter.com/5-best-ways-to-convert-python-csv-to-xml-using-elementtree/
    * Source:           https://stackoverflow.com/questions/15679467/parse-all-the-xml-files-in-a-directory-one-by-one-using-elementtree
    * Source:           https://chatgpt.com/
*/


// ===========================================================================================================
// ================================================= INCLUDE =================================================
// ===========================================================================================================
#include <ArduinoBLE.h>


// ===========================================================================================================
// ================================================ VARIABLES ================================================
// ===========================================================================================================
#define SERVICE_UUID "12345678-1234-5678-1234-56789abcdef0"
#define CHARACTERISTIC_UUID "12345678-1234-5678-1234-56789abcdef1"

BLEService bleService(SERVICE_UUID);
BLEIntCharacteristic led_characteristic(CHARACTERISTIC_UUID, BLERead | BLEWrite);

int ledPin[] = { 3, 4, 5 };
int pins = sizeof(ledPin) / sizeof(ledPin[0]);

unsigned char debug_usb = 0;


// ===========================================================================================================
// ================================================== SETUP ==================================================
// ===========================================================================================================
void setup() {
  delay(2000);
  led_setup();
  start_led_blink();

  Serial.begin(9600);
  if (Serial) {
    debug_usb = 1;
  }
  if (debug_usb) Serial.println("Started");

  if (!BLE.begin()) {
    if (debug_usb) Serial.println("starting BLE failed!");
    while (1)
      ;
  }

  ble_setup();
}


// ===========================================================================================================
// =================================================== LOOP ==================================================
// ===========================================================================================================
void loop() {
  waiting_for_connection_led_blink();

  BLEDevice central = BLE.central();

  if (central) {
    if (debug_usb) Serial.print("Connected to central MAC: ");
    if (debug_usb) Serial.println(central.address());

    digitalWrite(LED_BUILTIN, HIGH);

    while (central.connected()) {
      delay(100);
    }

    digitalWrite(LED_BUILTIN, LOW);
    if (debug_usb) Serial.print("Disconnected from central MAC: ");
    if (debug_usb) Serial.println(central.address());
  }
  delay(1000);
}


// ===========================================================================================================
// ================================================ FUNCTIONS ================================================
// ===========================================================================================================

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void ble_setup() {
  BLE.setLocalName("SMB_Arduino");
  BLE.setAdvertisedService(bleService);

  bleService.addCharacteristic(led_characteristic);
  BLE.addService(bleService);

  led_characteristic.setValue(0);
  led_characteristic.setEventHandler(BLEWritten, on_write_callback);
  BLE.advertise();

  if (debug_usb) Serial.print("Peripheral device MAC: ");
  if (debug_usb) Serial.println(BLE.address());
  if (debug_usb) Serial.println("Waiting for connections…");
}

void on_write_callback(BLEDevice central, BLECharacteristic characteristic) {
  int value = led_characteristic.value() & 15;
  switch (value) {
    case 1:
      if (debug_usb) Serial.println("Red LED on");
      digitalWrite(ledPin[0], LOW);
      digitalWrite(ledPin[1], LOW);
      digitalWrite(ledPin[2], HIGH);
      break;
    case 2:
      if (debug_usb) Serial.println("Yellow LED on");
      digitalWrite(ledPin[0], LOW);
      digitalWrite(ledPin[1], HIGH);
      digitalWrite(ledPin[2], LOW);
      break;
    case 3:
      if (debug_usb) Serial.println("Green LED on");
      digitalWrite(ledPin[0], HIGH);
      digitalWrite(ledPin[1], LOW);
      digitalWrite(ledPin[2], LOW);
      break;
    case 0:
      if (debug_usb) Serial.println("LEDs off");
      digitalWrite(ledPin[0], LOW);
      digitalWrite(ledPin[1], LOW);
      digitalWrite(ledPin[2], LOW);
      break;
    default:
      if (debug_usb) Serial.print("Unknown characteristic value received: ");
      if (debug_usb) Serial.println(value);
      digitalWrite(ledPin[0], HIGH);
      digitalWrite(ledPin[1], HIGH);
      digitalWrite(ledPin[2], HIGH);
  }
}

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void led_setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  for (int i = 0; i < pins; i++) {
    pinMode(ledPin[i], OUTPUT);
  }
}

void start_led_blink() {
  for (int i = 0; i < 10; i++) {
    for (int i = 0; i < pins; i++) {
      digitalWrite(ledPin[i], HIGH);
    }
    delay(100);
    for (int i = 0; i < pins; i++) {
      digitalWrite(ledPin[i], LOW);
    }
    delay(100);
  }
}

void waiting_for_connection_led_blink() {
  for (int i = 0; i < pins; i++) {
    digitalWrite(ledPin[i], HIGH);
  }
  delay(50);
  for (int i = 0; i < pins; i++) {
    digitalWrite(ledPin[i], LOW);
  }
  delay(50);
}