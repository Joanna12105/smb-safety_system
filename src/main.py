"""
py:module::         main

* Filename:         main.py
* Description:      This is the main module of the project. It saves the important paths in the "Paths" class and makes
                     them globally available for every other module. It contains the "SizeClasses" class, in which the
                     values for the object size required for the distance calculation are stored.
                     The "DataCollected" class contains the "save_data" function, which can be used to save camera
                     frames with the information on the calculated distance and LED color associated with the frame.
                     It also saves a JSON file with information about the image name, the filtered distance
                     and the LED data send to the Arduino.
                     The "main" of the "main.py" module starts the normal program. The saving of data is disabled
                     and the BLE connection establishment and object detection are initiated.
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
import json
import os.path
from datetime import time
import time
from datetime import datetime
import cv2
import sys

sys.path.append('/home/hshl/smb-safety_system')
from src import object_detection
from src import comm


# ===========================================================================================================
# ================================================= CLASSES =================================================
# ===========================================================================================================
class Paths:
    def __init__(self):
        self.val_imgs_path = "/home/hshl/smb-safety_system/tools/validation_imgs/"
        self.cal_val_imgs_path = "/home/hshl/smb-safety_system/tools/cal_val_DINA4_imgs/"
        self.train_imgs_path = "/home/hshl/smb-safety_system/tools/train_imgs/"
        self.json_file_path_val = "/home/hshl/smb-safety_system/config/camera/picamera_val.json"
        self.json_file_path_DINA4 = "/home/hshl/smb-safety_system/config/camera/picamera_DINA4.json"
        self.test_imgs_path = "/home/hshl/smb-safety_system/tools/test_imgs/"
        self.json_file_path_test = "/home/hshl/smb-safety_system/config/camera/picamera_test.json"


class SizeClasses:
    def __init__(self):
        self.class_to_size = {
            "full_front_view_car": 1.81,
            "covered_front_view_car": 0.905,
            "side_view_car": 4.36,
            "covered_side_view_car": 2.18
        }


class DataCollected:
    def __init__(self):
        pass

    @staticmethod
    def save_data(frame_to_save, distance_filtered, led_data_send):
        path = Paths().test_imgs_path
        timestamp = int(time.time())
        format_timestamp = datetime.fromtimestamp(timestamp)
        readable_timestamp = format_timestamp.strftime('%Y-%m-%d_%H-%M-%S')
        img_name = f"{readable_timestamp}.jpg"
        cv2.imwrite(str(path) + str(img_name), frame_to_save)
        print("> Image saved as {} to {}!".format(img_name, path))
        test_dict = {"image name": img_name,
                     "distance filtered": distance_filtered,
                     "LED data send to Arduino": led_data_send}
        if not os.path.exists(Paths().json_file_path_test):
            with open(Paths().json_file_path_test, "w") as json_file:
                json.dump([test_dict], json_file, indent=4)
        else:
            with open(Paths().json_file_path_test, "r") as json_file:
                data_to_remain = json.load(json_file)
            data_to_remain.append(test_dict)
            with open(Paths().json_file_path_test, "w") as new_json_file:
                json.dump(data_to_remain, new_json_file, indent=4)


# ===========================================================================================================
# ================================================== MAIN ===================================================
# ===========================================================================================================
if __name__ == '__main__':
    to_save = False
    arduino = comm.rpi_comm_setup()
    check, arduino = comm.rpi_connection_check(arduino)
    while not check:
        check, arduino = comm.rpi_connection_check(arduino)
    ob = object_detection.ObjectDetection()
    ob.object_detect(to_save, arduino)
