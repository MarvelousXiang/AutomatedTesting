import numpy as np
import os
import json
import io
import PIL.Image
import chardet


def shapes_to_label(json_file_path, savaFileName):
    list_path = os.listdir(json_file_path)
    file_handle = open(savaFileName, mode='w')
    for i in range(0, len(list_path)):
        path = os.path.join(json_file_path, list_path[i])
        if os.path.isfile(path):
            data = json.load(open(path))
            for shape in data['activity']:
                label_name = shape['bounds']
                file_handle.write(label_name)
                polygons = shape['rel-bounds']
                for m in range(len(polygons)):
                    for n in range(len(polygons[m])):
                        file_handle.write(str(polygons[m][n]))
                        file_handle.write(",")
                    file_handle.write("\n")
    file_handle.close()


shapes_to_label("C:/Users/10072/Desktop/自动化测试大作业/Data/json/",
                r"C:\Users\10072\Desktop\自动化测试大作业\Result\阶段1\result.txt")
