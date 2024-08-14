"""
py:module::         mapping

* Filename:         mapping.py
* Description:      This module contains the "DistanceCalc" class. It can be used to calculate the distance between an
                     object and the camera using object detection. This class also has functions for finding the
                     shortest distance in a single frame and for combining distances from several camera frames and
                     grouping them using their average and standard deviation. In the "map_distance_to_leds" function,
                     the determined distance is converted to one of the three LED colors.
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
import sys
import numpy as np

sys.path.append('/home/hshl/smb-safety_system')
from src import main
from src import comm


# ===========================================================================================================
# ================================================= CLASSES =================================================
# ===========================================================================================================
class DistanceCalc:
    def __init__(self):
        self.focal_length = None

        self.get_focal_length()

    def get_focal_length(self):
        with open(main.Paths().json_file_path_DINA4, "r") as json_file:
            json_data = json.load(json_file)
        if "calibration image" in json_data:
            self.focal_length = json_data["calibration image"].get("focal length")

    def distance_calculation(self, width_bounding_box, class_object):
        main_classes = main.SizeClasses()
        width_object = main_classes.class_to_size[class_object]
        distance_object = (width_object * self.focal_length) / width_bounding_box
        return distance_object

    @staticmethod
    def find_shortest_distance_in_frame(distances):
        return min(distances)

    def summarized_distance(self, distances, arduino):
        distances_sorted = []
        distances_stdev = np.std(distances)
        distances_avg = np.mean(distances)
        for i in range(len(distances)):
            if distances[i] <= (distances_avg - distances_stdev) or distances[i] <= (distances_avg + distances_stdev):
                distances_sorted.append(distances[i])
        distance_to_show = np.mean(distances_sorted)
        led_val = self.map_distance_to_leds(distance_to_show, arduino)
        return distance_to_show, led_val

    @staticmethod
    def map_distance_to_leds(dist_to_map, arduino):
        if dist_to_map < 25:
            led_on = "red"
        elif 25 <= dist_to_map < 50:
            led_on = "yellow"
        else:
            led_on = "green"
        led_value = comm.rpi_send_data(led_on, arduino)
        return led_value
