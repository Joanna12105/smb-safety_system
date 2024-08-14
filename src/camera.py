"""
py:module::         camera

* Filename:         camera.py
* Description:      This module contains two classes "CameraClass" starts the camera and outputs the camera frames
                     without object detection. The "CameraOD" class starts the camera, but does not output the camera
                     data so that it can still be changed by the object detection before output.
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
# export DISPLAY=:0
# export QT_QPA_PLATFORM=xcb


# ===========================================================================================================
# ================================================= IMPORTS =================================================
# ===========================================================================================================
import threading
from copy import deepcopy
from threading import Thread
import cv2
from picamera2 import Picamera2


# ===========================================================================================================
# ================================================= CLASSES =================================================
# ===========================================================================================================
class CameraClass:
    def __init__(self):
        self.last_frame = None
        self.stopped = False

        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.start()
        self.config = self.picam2.preview_configuration
        self.width_picam = self.config.main.size[0]
        self.height_picam = self.config.main.size[1]
        self.img_lock = threading.Lock()
        Thread(target=self.camera).start()

    def camera(self):
        print("Funktion to read camera images started!")

        while True:
            if self.stopped:
                print("stop")
                self.picam2.stop()
                return
            self.last_frame = self.picam2.capture_array()
            self.camera_display()

    def get_image(self):
        with self.img_lock:
            return deepcopy(self.last_frame)

    def camera_display(self):
        cv2.imshow('CAMERA', self.get_image())
        cv2.waitKey(1)

    def stop_camera(self):
        self.stopped = True
        print("Camera stopped")


class CameraOD:
    def __init__(self):
        self.last_frame = None
        self.stopped = False

        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.start()
        self.config = self.picam2.preview_configuration
        self.width_picam = self.config.main.size[0]
        self.height_picam = self.config.main.size[1]
        self.usable_frame = None
        self.img_lock = threading.Lock()
        Thread(target=self.camera).start()

    def camera(self):
        print("Funktion to read camera images for Object Detection started!")

        while True:
            if self.stopped:
                print("stop")
                self.picam2.stop()
                return
            self.last_frame = self.picam2.capture_array()
            self.usable_frame = self.get_image()

    def get_image(self):
        with self.img_lock:
            return deepcopy(self.last_frame)

    def stop_camera(self):
        self.stopped = True
        print("Camera stopped")
