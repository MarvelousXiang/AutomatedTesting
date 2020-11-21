import cv2
import os
import re
import subprocess
import confidence


class Stage2Demo:
    def getXiangSu(self):
        from PIL import Image
        img = Image.open(r"C:\Users\10072\Desktop\自动化测试大作业\Data\img\1.jpg")
        img_array = img.load()
        print(img.size)

    def _get_screen_size(self):
        return "1920x1080"

    def test(self):
        sizes = self._get_screen_size()
        print('sizes', sizes)
        imgsr = cv2.imread(r"C:\Users\10072\Desktop\自动化测试大作业\Data\img\2.jpg")
        imgtm = cv2.imread(r"C:\Users\10072\Desktop\自动化测试大作业\Data\img\3.jpg")
        # 获取图片的高和宽
        imgtmh1 = imgtm.shape[0]
        imgtmw1 = imgtm.shape[1]

        imgtmh2 = imgsr.shape[0]
        imgtmw2 = imgsr.shape[1]
        # print(imgtmh2)
        # print(imgtmh2, imgtmw2)

        res = cv2.matchTemplate(imgsr, imgtm, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        img = cv2.rectangle(imgsr, max_loc, (max_loc[0] + imgtmw1, max_loc[1] + imgtmh1), (0, 0, 255), 2)

        cv2.imshow('Image', img)
        cv2.waitKey(0)
        exit(1)
        print((max_loc[0] + imgtmw1), (max_loc[1] + imgtmh1))
        heights = float(sizes[1]) / imgtmh2
        widths = float(sizes[0]) / imgtmw2
        print((max_loc[0] + imgtmw1) * heights, (max_loc[1] + imgtmh1) * widths)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def matchImg(self, imgobj):
        # imgsrc=原始图像，imgobj=待查找的图片
        import aircv as ac

        imsrc = ac.imread(self)
        imobj = ac.imread(imgobj)

        match_result = ac.find_template(imsrc, imobj,
                                        confidence)
        # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)),
        # 'result': (422.0, 400.0)}
        if match_result is not None:
            match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽

        return match_result

    def get_screenxy_from_bmp(self, main_bmp, son_bmp):

        # 获取指定控件的坐标->(x,y,width,height)
        from PIL import Image

        img_main = Image.open(main_bmp)
        img_son = Image.open(son_bmp)
        datas_a = list(img_main.getdata())
        datas_b = list(img_son.getdata())

        for i, item in enumerate(datas_a):
            if datas_b[0] == item and datas_a[i + 1] == datas_b[1]:
                yx = divmod(i, img_main.size[0])
                main_start_pos = yx[1] + yx[0] * img_main.size[0]

                match_test = True
                for n in range(img_son.size[1]):
                    main_pos = main_start_pos + n * img_main.size[0]
                    son_pos = n * img_son.size[0]

                    if datas_b[son_pos:son_pos + img_son.size[0]] != datas_a[main_pos:main_pos + img_son.size[0]]:
                        match_test = False
                        break
                if match_test:
                    return yx[1], yx[0], img_son.size[0], img_son.size[1]
        return False


import aircv as ac
import cv2

imsrc = ac.imread(r'C:\Users\10072\Desktop\自动化测试大作业\Data\img\1.jpg')  # 原始图像
imsch = ac.imread(r':\Users\10072\Desktop\自动化测试大作业\Data\img\1.jpg')  # 查找的部分

match_result = ac.find_template(imsrc, imsch)
res1 = match_result['result']
shape = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽

import appium

if match_result is not None:
    res2 = match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽

    x, y = res1
    shape_x, shape_y = tuple(map(int, shape))
    photo_position_x = 500
    photo_position_y = 300
    position_x, position_y = int(photo_position_x + (1080 / shape_x * x)), int(photo_position_y + (1920 / shape_y * y))
