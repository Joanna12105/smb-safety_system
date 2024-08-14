"""
py:module::         cal_val_DINA4

* Filename:         cal_val_DINA4.py
* Description:      This module is used to "calibrate" the camera setup by determining and validating the focal length.
                     The process to compute the focal length does not involve actual camera calibration.
                     To simplify the description of what this module does, the term "calibration" is used.

                     Using the module "image_collect_DINA4.py" three images of a DINA4 paper with different, but known,
                     distances to the camera were taken. One of these images is used for the "calibration" - the
                     determination of the focal length. The following formula is used:
                        focal length = (width of the object in the image * known distance) / actual width of the object

                     The other two images are used to validate the calculated focal length by computing the distance
                     from the object to the camera using the formula:
                        distance = (actual width of the object * focal length) / width of the object in the image

                     The calculated results are saved in a JSON file. The user can review this file to
                     compare the calculated distances with the known (measured) distances, thereby validating and
                     documenting the computed focal length for future use.

                     Other modules within this project will use the focal length saved in the JSON file, that is
                     produced by this module.

                     A DINA4 paper is used for "calibrating" the focal length because its width is standardized,
                     ensuring high accuracy for the value of the "actual width of the object". Additionally, it is
                     relatively easy to find a high-contrast background to the white paper, which helps with accurately
                     determining the bounding boxes. Another reason to use a DINA4 paper for the "calibration" process
                     is the rectangular shape of the paper which matches the shape of the bounding boxes,
                     improving the accuracy of the value for "width of the object in the image".
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
import os
import sys
import numpy as np
import imutils
import cv2

sys.path.append('/home/hshl/smb-safety_system')
from src import main


# ===========================================================================================================
# ================================================= CLASSES =================================================
# ===========================================================================================================
class Calibration:
    def __init__(self):
        self.calibration_dict = {}
        self.images_path = main.Paths().cal_val_imgs_path
        self.cal_file_name = "2m_DINA4.jpg"
        self.json_path = main.Paths().json_file_path_DINA4
        self.file_name = []
        self.jpg_count = None

        self.get_file_name()
        self.count_jpg_files()

    def fill_json_with_content(self):
        with open(self.json_path, "w") as json_file:
            json.dump(self.calibration_dict, json_file, indent=4)

    def get_file_name(self):
        for file in os.listdir(self.images_path):
            if file.endswith(".jpg") and file != self.cal_file_name:
                self.file_name.append(file)

    def count_jpg_files(self):
        count = 0
        files = os.listdir(self.images_path)
        for file in files:
            if file.endswith(".jpg") and file != self.cal_file_name:
                count += 1
        self.jpg_count = count


# ===========================================================================================================
# ================================================ FUNCTIONS ================================================
# ===========================================================================================================
def find_marker(image_to_mark):
    gray = cv2.cvtColor(image_to_mark, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    return cv2.minAreaRect(c)


def distance_to_camera(known_width, focal_length, per_width):
    return (known_width * focal_length) / per_width


# ===========================================================================================================
# ================================================== MAIN ===================================================
# ===========================================================================================================
if __name__ == '__main__':
    cal = Calibration()
    KNOWN_DISTANCE = 2.0
    KNOWN_WIDTH = 0.297
    cal_image_path = cal.images_path + cal.cal_file_name
    print(cal_image_path)
    image = cv2.imread(cal_image_path)
    marker = find_marker(image)
    box = cv2.boxPoints(marker)
    box = np.intp(box)
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv2.imshow("image", image)
    cv2.waitKey(5000)
    focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
    focal_length_dict = {"image used": cal_image_path,
                         "focal length": focalLength,
                         "known distance object": KNOWN_DISTANCE,
                         "known width object": KNOWN_WIDTH}
    cal.calibration_dict["calibration image"] = focal_length_dict

    for i in range(cal.jpg_count):
        val_image_path = cal.images_path + cal.file_name[i]
        print(val_image_path)
        image = cv2.imread(val_image_path)
        marker = find_marker(image)
        meter = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
        box = cv2.boxPoints(marker)
        box = np.intp(box)
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.putText(image, "%.2fm" % meter,
                    (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                    2.0, (0, 255, 0), 3)
        cv2.imshow("image", image)
        cv2.waitKey(3000)
        add_to_dict = {"width Bounding Box": marker[1][0],
                       "distance Object": meter,
                       "width Object": KNOWN_WIDTH,
                       "focal length": focalLength}
        cal.calibration_dict[cal.file_name[i]] = add_to_dict

    cal.fill_json_with_content()
