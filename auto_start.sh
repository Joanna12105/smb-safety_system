#!/bin/bash

# * Filename:         auto_start.sh
# * Description:      This shell script is executed when the Raspberry Pi boots up. It sets up the necessary
#                      environment variables to run graphical applications and Python modules, then launches
#                      the main application. Alternatively the applications "image_collect_train_od.py" or
#                      "image_collect_test_od.py" can be launched depending on which lines are uncommented in the
#                      script.
# * Author:           Joanna Rieger
# * Bachelor thesis:  "Untersuchungen zum Einsatz von KI und Computer Vision für ein Fahrradassistenzsystem am Beispiel
#                       eines rückwärtigen Abstands- und Annäherungswarners"
# * E-Mail:           joanna.rieger@stud.hshl.de
# * Project Sources:
#     * Source:           https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi
#     * Source:           https://colab.research.google.com/github/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/Train_TFLite2_Object_Detction_Model.ipynb
#     * Source:           https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
#     * Source:           https://www.welt.de/motor/news/article244937978/Jedes-Jahr-ein-Zentimeter-mehr-Laengenwachstum-bei-Pkw.html#:~:text=Zwischen%202000%20und%202022%20ist,von%20einem%20Zentimeter%20pro%20Jahr.
#     * Source:           https://www.ardalpha.de/wissen/geschichte/kulturgeschichte/din-a4-din-normen-100-jahre-100.html#:~:text=Die%20wohl%20bekannteste%20DIN%2DNorm%20ist%20die%20DIN%20EN%20ISO,noch%20in%20den%20Drucker%20legen.
#     * Source:           https://jashuang1983.wordpress.com/rpi4-ble-with-arduino-nano-33/
#     * Source:           https://docs.arduino.cc/tutorials/nano-33-ble-sense/bluetooth/
#     * Source:           https://github.com/OpenBluetoothToolbox/SimpleBLE/blob/main/examples/simplepyble/write.py
#     * Source:           https://blog.finxter.com/5-best-ways-to-convert-python-csv-to-xml-using-elementtree/
#     * Source:           https://stackoverflow.com/questions/15679467/parse-all-the-xml-files-in-a-directory-one-by-one-using-elementtree
#     * Source:           https://chatgpt.com/

export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
export XAUTHORITY=/home/hshl/.Xauthority

export PYTHONPATH=/home/hshl/.local/lib/python3.9/site-packages:$PYTHONPATH

# /usr/bin/python3.9 /home/hshl/smb-safety_system/tools/image_collect_train_od.py >> /home/hshl/startup.log 2>&1
# /usr/bin/python3.9 /home/hshl/smb-safety_system/tools/image_collect_test_od.py >> /home/hshl/startup.log 2>&1
 /usr/bin/python3.9 /home/hshl/smb-safety_system/src/main.py >> /home/hshl/startup.log 2>&1

