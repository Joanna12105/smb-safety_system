"""
py:module::         validation

* Filename:         validation.py
* Description:      This module can be used to validate the distance calculation using the trained object detection
                     model. The images used by this module can be taken with the "image_collect.py" which stores images
                     in the "validation_imgs" folder. The module detects objects in these images, calculates the
                     distance to the camera, and compares this calculated distance with the actual distance embedded
                     in the image file names. If the difference between the calculated and actual distances is
                     within ±5 meters, the calculation is considered accurate.
                     The results of the validation process are saved in a JSON file containing information about the
                      class detected, the calculated distance, the actual distance, the object detected and
                      the validation for each image.
                        - class detected        ==      the class of the detected object
                        - calculated distance   ==      the distance calculated using the detected class
                        - actual distance       ==      the actual, measured distance
                                                         (extracted from the image filename)
                        - object detected       ==      '0' if no object was detected, '1' if an object was detected
                        - validation            ==      '0' if the difference between the calculated and the actual
                                                         distance is > than 5m, '1' if the difference is <= 5m
                     After processing the images in the "validtion_imgs" folder the module analyzes the created
                     JSON file. It counts the objects that should have been detected, the number of undetected objects,
                     the number of objects detected with incorrect distances, and the number of objects detected with
                     correct distances. These statistics are printed to the terminal for the evaluation of the distance
                     calculation using the created object detection model.
                     !Attention! The module assumes that there is exactly one car per image and that the images are
                     named according to the specific convention given in the "image_collect.py".
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
import os
import sys
import re
import json

sys.path.append('/home/hshl/smb-safety_system')
from src import main
from src import mapping
import object_detection_imgs


# ===========================================================================================================
# ================================================= CLASSES =================================================
# ===========================================================================================================
class ValidationDistanceCalculation:
    def __init__(self):
        self.focal_length = None
        self.jpg_count = None
        self.path = main.Paths().val_imgs_path
        self.file_names = None
        self.val_distance = None
        self.calc_distance = None
        self.json_path = main.Paths().json_file_path_val
        self.validation_dict = {}
        self.object_detected = None
        self.detected_class = None

        self.count_jpg_files()
        self.get_file_name()

    def count_jpg_files(self):
        count = 0
        files = os.listdir(self.path)
        for file in files:
            if file.endswith(".jpg"):
                count += 1
        self.jpg_count = count

    def get_file_name(self):
        name = []
        for file in os.listdir(self.path):
            if file.endswith(".jpg"):
                name.append(file)
        self.file_names = name

    @staticmethod
    def repl_character(input_string, char_remove, char_new):
        return input_string.replace(char_remove, char_new)

    @staticmethod
    def remove_unit(input_string):
        return re.sub(r'm.*', '', input_string)

    def check_distance(self, j):
        name = self.file_names[j]
        index_name = name.lower().find(".jpg")
        if index_name != -1:
            distance_string = name[:index_name]
        else:
            print("No .jpg")
            distance_string = "Error"
        distance = self.repl_character(distance_string, ',', '.')
        distance = self.remove_unit(distance)
        self.val_distance = float(distance)

    def fill_json_with_content(self):
        with open(self.json_path, "w") as json_file:
            json.dump(self.validation_dict, json_file, indent=4)

    def distance_calculation_imgs(self, k, fl):
        file_path = self.path + self.file_names[k]
        obj_detection = object_detection_imgs.ObjectDetectionImgs()
        width_bounding_box, class_ob = obj_detection.object_detect_img(file_path)
        self.detected_class = class_ob
        if width_bounding_box != 0:
            main_classes = main.SizeClasses()
            width_object = main_classes.class_to_size[class_ob]
            self.object_detected = 1
            self.calc_distance = (width_object * fl) / width_bounding_box
        else:
            self.object_detected = 0
            self.calc_distance = 0

    def create_validation_json(self):
        counter_ond = 0  # object not detected
        counter_odfd = 0  # object detected, false distance
        counter_odcd = 0  # object detected, correct distance
        objects_to_detect = 0
        with open(self.json_path, "r") as json_file:
            json_data = json.load(json_file)
        for file_name, dct in json_data.items():
            object_detect = dct.get("object detected")
            val_detect = dct.get("validation")
            objects_to_detect += 1
            if object_detect == 0:
                counter_ond += 1
            elif object_detect == 1 and val_detect == 0:
                counter_odfd += 1
            elif object_detect == 1 and val_detect == 1:
                counter_odcd += 1
            else:
                print("ERROR")
        print("Distances to calculate:", objects_to_detect)
        print("Objects not detected:", counter_ond)
        print("Objects detected, false distance calculated:", counter_odfd)
        print("Objects detected, correct distance calculated:", counter_odcd)


# ===========================================================================================================
# ================================================== MAIN ===================================================
# ===========================================================================================================
if __name__ == '__main__':
    val = ValidationDistanceCalculation()
    focal_length = mapping.DistanceCalc().focal_length

    for i in range(val.jpg_count):
        val.distance_calculation_imgs(i, focal_length)
        val.check_distance(i)

        if abs(val.calc_distance - val.val_distance) <= 5:
            add_to_dict = {"detected_class": val.detected_class,
                           "calculated distance": val.calc_distance,
                           "actual distance": val.val_distance,
                           "object detected": val.object_detected,
                           "validation": 1}
            val.validation_dict[val.file_names[i]] = add_to_dict
        else:
            add_to_dict = {"detected_class": val.detected_class,
                           "calculated distance": val.calc_distance,
                           "actual distance": val.val_distance,
                           "object detected": val.object_detected,
                           "validation": 0}
            val.validation_dict[val.file_names[i]] = add_to_dict

    val.fill_json_with_content()
    val.create_validation_json()
