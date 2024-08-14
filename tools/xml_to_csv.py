"""
py:module::         xml_to_csv

* Filename:         xml_to_csv.py
* Description:      Script to convert information stored in .xml files to a .csv file. The .xml files contain all
                     annotation information per image and are formatted in the Pascal VOC format. In the .csv file
                     each row contains the information per bounding box.
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
import xml.etree.ElementTree as ET
import csv
import os

# ===========================================================================================================
# ================================================= "MAIN" ==================================================
# ===========================================================================================================
path_folder = "/content/images/"
csv_filename = "org_imgs_bb.csv"

with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(['Folder', 'Filename', 'Path', 'Source', 'Width', 'Height', 'Depth', 'Segmented',
                     'Object Name', 'Object Pose', 'Object Truncated', 'Object Difficult', 'Bounding Box'])

    for object_detection_file in os.listdir(path_folder):
        if not object_detection_file.endswith(".xml"):
            continue

        path_file = os.path.join(path_folder, object_detection_file)
        tree = ET.parse(path_file)
        root = tree.getroot()

        folder = root.find('folder').text
        filename = root.find('filename').text
        path = root.find('path').text
        source_root = root.find('source')
        source = source_root.find('database').text
        size = root.find('size')
        width = size.find('width').text
        height = size.find('height').text
        depth = size.find('depth').text
        segmented = root.find('segmented').text

        for obj in root.findall('object'):
            name = obj.find('name').text
            pose = obj.find('pose').text
            truncated = obj.find('truncated').text
            difficult = obj.find('difficult').text
            bndbox = obj.find('bndbox')
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            xmax = bndbox.find('xmax').text
            ymax = bndbox.find('ymax').text

            bbox = f'[{xmin}, {ymin}, {xmax}, {ymax}]'

            writer.writerow([folder, filename, path, source, width, height, depth, segmented,
                             name, pose, truncated, difficult, bbox])
