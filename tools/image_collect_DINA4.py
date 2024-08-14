"""
py:module::         image_collect_DINA4

* Filename:         image_collect_DINA4.py
* Description:      This Python module is used to start the 'Raspberry Pi Camera Module 3' as a webcam. By following
                     the terminal instructions, individual frames from the webcam feed can be captured and saved.
                     These frames are stored in the 'cal_val_DINA4_imgs' folder as images that can be named
                     individually in the terminal.

                     The "cal_val_DINA4.py" will use these images to compute and validate the focal length of the camera
                     used.
                     !Attention! When images are saved in the same folder with the same name the old picture will be
                     overwritten.
                     The "cal_val_DINA4.py" is set to use an image called "2m_DINA4.jpg" to compute the focal length.
                     It is therefore using 2.0 meters as the known distance for the distance calculation. The useful
                     naming of the other images with the measured distances can be helpful for validating the computed
                     focal length using the created JSON file created by the "cal_val_DINA4.py" module.
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
from time import sleep
import threading
import cv2
import sys

sys.path.append('/home/hshl/smb-safety_system')
from src import camera
from src import main


# ===========================================================================================================
# ================================================ FUNCTIONS ================================================
# ===========================================================================================================
def get_user_input():
    path = main.Paths().cal_val_imgs_path
    while True:
        user_input = input("\nEnter 's' to save the last frame captured! Entered: ")
        if user_input.lower() == 's':
            print("\tSaving last frame:")
            img_name = "{}.jpg".format(name_file())
            cv2.imwrite(str(path) + str(img_name), image)
            print("\t> The image was saved as {} to {}!".format(img_name, path))
        else:
            print("\t!!!Invalid input. Please enter 's' to save images!!!")


def name_file():
    return input(
        "\t> Enter the file name.\n\t   Examples: 1,5m or 2m\n\t\t> Entered: ")


# ===========================================================================================================
# ================================================== MAIN ===================================================
# ===========================================================================================================
if __name__ == '__main__':
    cam = camera.CameraClass()

    input_thread = threading.Thread(target=get_user_input)
    input_thread.start()

    while True:
        try:
            image = cam.get_image()
            sleep(0.1)
        except KeyboardInterrupt:
            print("Interrupt")
            input_thread.join()
            cam.stop_camera()
            break
