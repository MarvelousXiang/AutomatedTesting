# AutomatedTesting2020

姓名：项卓奇

学号：181250164

选题方向：移动应用自动化测试

***


## 模型分析

使用BRISK方法描述图片的特征
使用KNN和RANSAC方法对特征进行匹配
在数据库中实现控件识别


### 模型结构

建立图片描述，计算特征点和特征点周围的信息
建立匹配描述


### 运行步骤

用Tesseract可以识别格式规范的文字，主要具有以下特点：

• 使用一个标准字体（不包含手写体、草书，或者十分“花哨的”字体） 
• 虽然被复印或拍照，字体还是很清晰，没有多余的痕迹或污点 
• 排列整齐，没有歪歪斜斜的字 
• 没有超出图片范围，也没有残缺不全，或紧紧贴在图片的边缘 

pytesseract是Tesseract关于Python的接口，可以使用pip install pytesseract安装。
安装完后，就可以使用Python调用Tesseract了，不过还需要一个Python的图片处理模块，这里选择安装pillow。

使用OpenCV-python实现控件识别，首先加载必要的库
import numpy as np
import glob
import csv
import cv2

class CoverDescriptor:
    def describe(self, image):
        # 使用BRISK方法对图片进行特征提取，同类型的还有SIFT，SURF等等
        descriptor = cv2.BRISK_create()
        # 第一步是detect找到特征点，特征点信息包括关键点的位置，大小，旋转角等等
        # 第二步是计算特征点周围的特征描述子，None表示没有遮罩
        (kps, descs) = descriptor.detectAndCompute(image, None)
        # 这里的keypoint只需要坐标位置就可以了，丢弃其他性质
        kps = np.float32([kp.pt for kp in kps])
        # 返回ROI点和对应周围的环境描述子
        return (kps, descs)

### 相关参考文献

https://github.com/Duankaiwen/CenterNet
https://github.com/eriklindernoren/PyTorch-YOLOv3
https://blog.csdn.net/weixin_41685388/article/details/104039617?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-2.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-2.control
https://www.jb51.net/article/143564.htm

## 实验验证

如上所示


### 评估指标及含义

def search(self, queryKps, queryDescs):
        results = {}
        for coverPath in self.coverPaths:
            cover = cv2.imread(coverPath)
            gray = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)
            (kps, descs) = self.descriptor.describe(gray)
            # query是待查图片的特征信息，后面的是当前数据库里每一张图片的信息
            score = self.match(queryKps, queryDescs, kps, descs)
            # 把分数存入字典，字典的键固定为50个，值为对应的匹配分
            results[coverPath] = score
        if len(results) > 0:
            results = sorted([(v, k) for (k, v) in results.items() if v > 0],
                reverse = True)
        return results

### 验证结果

运行结果显示精确度和对应的json和img
loop1 precision is 68.42%: author is Michael Crichton - title is State of Fear

## 结果示例

注意这个cm是CoverMatcher，search是CoverMatcher里面的一个方法
在已有的数据库中进行匹配，返回匹配分数和匹配对象的路径，注意这里的路径表达里面有个转义字符
举例，某一个返回值是[(0.9871794871794872, '1\\1.jpg')]
results = cm.search(queryKps, queryDescs)


## 个人感想

![](http://212.64.68.219:9090/autotest.jpg)

我明白为什么软件测试工程师的薪资既能排在软件工程师的第一梯队，相关人才却又可以如此紧缺了。
