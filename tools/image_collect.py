"""
py:module::         image_collect

* Filename:         image_collect.py
* Description:      This Python module is used to start the 'Raspberry Pi Camera Module 3' as a webcam. By following
                     the terminal instructions, individual frames from the webcam feed can be captured and saved.
                     These frames are stored in the 'validation_imgs' folder as images that can be named individually in
                     the terminal.

                     The "validation.py" will use these images to compare the calculated distance from the cars to the
                     camera to the actual distance of the cars to the camera, using object detection to identify the
                     cars and the formula:
                        distance = (actual width of the object * focal length) / width of the object in the image
                     to calculate the distance between the camera and the car.

                     The validation module expects the file name to be "distance(in meter)m_something_individual.jpg"
                     e.g. "20,5m_Fiat_1.jpg".
                     !Attention! When images are saved in the same folder with the same name the old picture will be
                     overwritten.
                     It is important to name the file as expected since the validation module will use the file name to
                     extract the actual distance between the car and the camera, by replacing a "," with a "." and by
                     cutting of every character after a "m" and the "m" itself.
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
    path = main.Paths().val_imgs_path
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
