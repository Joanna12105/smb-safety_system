"""
py:module::         image_collect_test_od

* Filename:         image_collect_test_od.py
* Description:      This module can be used to validate the object detection and the distance calculation in a
                     real-world scenario. It operates similarly to the "main.py" module.
                     The difference being that the variable "to_save" is set to "True". This setting enables the
                     "object_detection" module to call the "save_data" function to save webcam frames with the plotted
                     bounding boxes and the calculated distances for each bounding box. The data is also appended to a
                     JSON file for later review. The data saving occurs every 5 seconds.
                     !Attention! The program will not run if a file named "picamera_test.json" already exists in the
                     camera directory before the program starts.
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
import sys

sys.path.append('/home/hshl/smb-safety_system')
from src import object_detection
from src import comm

# ===========================================================================================================
# ================================================== MAIN ===================================================
# ===========================================================================================================
if __name__ == '__main__':
    to_save = True
    arduino = comm.rpi_comm_setup()
    check, arduino = comm.rpi_connection_check(arduino)
    while not check:
        check, arduino = comm.rpi_connection_check(arduino)
    ob = object_detection.ObjectDetection()
    ob.object_detect(to_save, arduino)
