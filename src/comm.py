"""
py:module::         comm

* Filename:         comm.py
* Description:      This module contains the functions required for communication with the Arduino. "rpi_comm_setup"
                     handles the setup and the BLE connection with the Arduino. "rpi_connection_check" can be used to
                     check whether there is a connection with the Arduino. The data is sent in the "rpi_send_data"
                     function.
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
"""

# ===========================================================================================================
# ================================================= IMPORTS =================================================
# ===========================================================================================================
import simplepyble
import sys

sys.path.append('/home/hshl/smb-safety_system')

mac_address = "45:99:72:43:F3:24"
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"


# ===========================================================================================================
# ================================================ FUNCTIONS ================================================
# ===========================================================================================================
def rpi_comm_setup():
    print("RPi Bluetooth setup")
    print("Connecting…")
    adapter = simplepyble.Adapter.get_adapters()[0]
    adapter.set_callback_on_scan_start(lambda: print("Scan started."))
    adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
    adapter.set_callback_on_scan_found(
        lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))

    adapter.scan_for(2000)
    peripherals = adapter.scan_get_results()
    for peripheral in peripherals:
        if peripheral.address() == mac_address:
            arduino = peripheral
            break
    else:
        print(f"Arduino with Mac-Address {mac_address} not found!")
        return
    arduino.connect()
    arduino.write_request(SERVICE_UUID, CHARACTERISTIC_UUID, bytes([3]))
    return arduino


def rpi_connection_check(arduino):
    if arduino is not None and not arduino.is_connected():
        check = False
        arduino = rpi_comm_setup()
        print("Reconnect")
    elif arduino is None:
        check = False
        arduino = rpi_comm_setup()
        print("Connecting ...")
    else:
        check = True
    return check, arduino


def rpi_send_data(led, arduino):
    if led == "red":
        led_int = 1
    elif led == "yellow":
        led_int = 2
    elif led == "green":
        led_int = 3
    else:
        led_int = 0
    try:
        arduino.write_request(SERVICE_UUID, CHARACTERISTIC_UUID, bytes([led_int]))
    except:
        print("Failed to write to Arduino!")
    return led
