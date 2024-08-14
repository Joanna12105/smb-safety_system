"""
py:module::         csv_to_xml

* Filename:         csv_to_xml.py
* Description:      Script to convert information stored in a .csv file, in which each row represents information per
                     bounding box, to .xml files that contain all annotation information per image. The .xml files
                     are formatted in the Pascal VOC format.
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
import csv
import xml.etree.ElementTree as ET
from collections import defaultdict
from xml.dom import minidom

# ===========================================================================================================
# ================================================= "MAIN" ==================================================
# ===========================================================================================================
csv_path = "/content/org_imgs_bb.csv"

with open(csv_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    get_filenames = defaultdict(list)
    for row in csv_reader:
        get_filenames[row['Filename']].append(row)

for xml_file, rows in get_filenames.items():
    root = ET.Element('annotation')

    folder = ET.SubElement(root, 'folder')
    folder.text = rows[0]['Folder']

    filename = ET.SubElement(root, 'filename')
    filename.text = rows[0]['Filename']

    path = ET.SubElement(root, 'path')
    path.text = rows[0]['Path']

    source = ET.SubElement(root, 'source')
    database = ET.SubElement(source, 'database')
    database.text = rows[0]['Source']

    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    width.text = rows[0]['Width']
    height = ET.SubElement(size, 'height')
    height.text = rows[0]['Height']
    depth = ET.SubElement(size, 'depth')
    depth.text = rows[0]['Depth']

    segmented = ET.SubElement(root, 'segmented')
    segmented.text = rows[0]['Segmented']

    for row in rows:
        obj = ET.SubElement(root, 'object')

        name = ET.SubElement(obj, 'name')
        name.text = row['Object Name']

        pose = ET.SubElement(obj, 'pose')
        pose.text = row['Object Pose']

        truncated = ET.SubElement(obj, 'truncated')
        truncated.text = row['Object Truncated']

        difficult = ET.SubElement(obj, 'difficult')
        difficult.text = row['Object Difficult']

        bbox_str = row['Bounding Box']
        bbox_vals = bbox_str.strip('[]').split(',')

        bndbox = ET.SubElement(obj, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = bbox_vals[0].strip()
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = bbox_vals[1].strip()
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = bbox_vals[2].strip()
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = bbox_vals[3].strip()

    xml_str = ET.tostring(root, encoding='utf-8')
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="\t")
    xml_lines = xml_str.splitlines()
    xml_str = '\n'.join(line for line in xml_lines if line.strip() and not line.strip().startswith('<?xml'))

    cut_name = xml_file[:-4]
    output_file = f'{cut_name}.xml'
    save_path = "/content/images/" + output_file
    with open(save_path, "w") as file:
        file.write(xml_str)
    print(f'Written: {output_file}')
