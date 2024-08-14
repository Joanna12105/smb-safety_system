"""
py:module::         object_detection

* Filename:         object_detection.py
* Description:      This module is used for object detection. In addition to the object detection, the "object_detect"
                     function controls/ initiates the distance calculation, the sending of data and regularly checks
                     the BLE connection to the Arduino by calling the corresponding functions. If the function was
                     called with the request to save the data, it also starts this process here by calling the
                     corresponding function.
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
import numpy as np
import cv2
from time import sleep
import time

sys.path.append('/home/hshl/smb-safety_system')
from src import camera
from src import mapping
from src import comm
from src import main

from tflite_runtime.interpreter import Interpreter
from tflite_runtime.interpreter import load_delegate


# ===========================================================================================================
# ================================================= CLASSES =================================================
# ===========================================================================================================
class ObjectDetection:
    def __init__(self):
        print("Object Detection initialization started!")
        self.cam = camera.CameraOD()
        self.stopped = False
        self.MODEL_NAME = "/home/hshl/smb-safety_system/config/tensorflow/custom_model_lite/"
        self.GRAPH_NAME = "edgetpu.tflite"
        self.LABELMAP_NAME = "labelmap.txt"
        self.CWD_PATH = os.getcwd()
        self.PATH_TO_TFLITE = os.path.join(self.CWD_PATH, self.MODEL_NAME, self.GRAPH_NAME)
        self.PATH_TO_LABELS = os.path.join(self.CWD_PATH, self.MODEL_NAME, self.LABELMAP_NAME)
        self.min_conf_threshold = 0.5
        self.resW = self.cam.width_picam
        self.resH = self.cam.height_picam
        self.imW = int(self.resW)
        self.imH = int(self.resH)

        with open(self.PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        self.interpreter = Interpreter(model_path=self.PATH_TO_TFLITE,
                                       experimental_delegates=[load_delegate('libedgetpu.so.1.0')])

        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

        self.boxes_idx, self.classes_idx, self.scores_idx = 1, 3, 0

    @staticmethod
    def millis():
        return int(time.monotonic() * 1000)

    def object_detect(self, data_saver, arduino):
        frame = None
        distance_to_show = None
        led_val = None
        sleep(0.5)
        shortest_distance_list = []
        frame_counter = 0
        start_time = self.millis()
        while not self.stopped:
            if frame_counter < 10:
                frame_counter += 1
                distances_in_frame = []
                frame1 = self.cam.usable_frame
                frame = frame1.copy()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
                input_data = np.expand_dims(frame_resized, axis=0)

                self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
                self.interpreter.invoke()

                boxes = self.interpreter.get_tensor(self.output_details[self.boxes_idx]['index'])[0]
                classes = self.interpreter.get_tensor(self.output_details[self.classes_idx]['index'])[0]
                scores = self.interpreter.get_tensor(self.output_details[self.scores_idx]['index'])[0]

                for i in range(len(scores)):
                    if (scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0):
                        ymin = int(max(1, (boxes[i][0] * self.imH)))
                        xmin = int(max(1, (boxes[i][1] * self.imW)))
                        ymax = int(min(self.imH, (boxes[i][2] * self.imH)))
                        xmax = int(min(self.imW, (boxes[i][3] * self.imW)))
                        wbb = self.width_bounding_box(xmin, xmax)

                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (252, 15, 192), 2)

                        object_name = self.labels[int(classes[i])]
                        cob = object_name
                        distance_calculated = mapping.DistanceCalc().distance_calculation(wbb, cob)
                        distances_in_frame.append(distance_calculated)
                        label = '%s: %d%%, Distance: %dm' % (object_name, int(scores[i] * 100), distance_calculated)
                        label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                        label_ymin = max(ymin, label_size[1] + 10)
                        cv2.rectangle(frame, (xmin, label_ymin - label_size[1] - 10),
                                      (xmin + label_size[0], label_ymin + base_line - 10), (255, 255, 255),
                                      cv2.FILLED)
                        cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                                    2)
                if distances_in_frame:
                    shortest_distance = mapping.DistanceCalc().find_shortest_distance_in_frame(distances_in_frame)
                    shortest_distance_list.append(shortest_distance)
                else:
                    shortest_distance_list.append(2000)

                cv2.imshow('Object detector', frame)
                cv2.waitKey(1)
            else:
                distance_to_show, led_val = mapping.DistanceCalc().summarized_distance(shortest_distance_list, arduino)
                frame_counter = 0
                shortest_distance_list = []

            current_time = self.millis()
            if (current_time - start_time) >= 5000:
                _, arduino = comm.rpi_connection_check(arduino)
                start_time = self.millis()
                if data_saver:
                    main.DataCollected().save_data(frame, distance_to_show, led_val)

        self.stop_object_detection()

    @staticmethod
    def width_bounding_box(x_min, x_max):
        width_bb = x_max - x_min
        return width_bb

    def stop_object_detection(self):
        print("Stopped Object Detection")
        self.cam.stop_camera()
        cv2.destroyAllWindows()
        self.stopped = True
