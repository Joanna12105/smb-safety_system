"""
py:module::         image_collect_train_od

* Filename:         image_collect_train_od.py
* Description:      This Python module starts the 'Raspberry Pi Camera Module 3' as a webcam and saves images from the
                     live webcam feed at 5-second intervals. The captured images are stored in the "train_imgs"
                     directory.
                     This script was created for data collection purposes, specifically to gather training
                     data for the AI model. The training process for the AI model used in this project was conducted
                     using a Colab notebook created by Evan Juras.
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
import time
from time import sleep
from datetime import datetime
import cv2
import sys

sys.path.append('/home/hshl/smb-safety_system')
from src import camera
from src import main


# ===========================================================================================================
# ================================================ FUNCTIONS ================================================
# ===========================================================================================================
def take_picture(img):
    path = main.Paths().train_imgs_path
    timestamp = int(time.time())
    format_timestamp = datetime.fromtimestamp(timestamp)
    readable_timestamp = format_timestamp.strftime('%Y-%m-%d_%H-%M-%S')
    img_name = f"{readable_timestamp}.jpg"
    cv2.imwrite(str(path) + str(img_name), img)
    print("> Image saved as {} to {}!".format(img_name, path))


def millis():
    return int(time.monotonic() * 1000)


# ===========================================================================================================
# ================================================== MAIN ===================================================
# ===========================================================================================================
if __name__ == '__main__':
    cam = camera.CameraClass()
    start_time = millis()

    while True:
        try:
            image = cam.get_image()
            sleep(0.1)
            current_time = millis()
            if (current_time - start_time) >= 5000:
                take_picture(image)
                start_time = millis()
        except KeyboardInterrupt:
            cam.stop_camera()
            break
