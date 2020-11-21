import numpy as np
import glob
import csv
import cv2


class CoverDescriptor:
    def describe(self, image):
        descriptor = cv2.BRISK_create()
        (kps, descs) = descriptor.detectAndCompute(image, None)
        kps = np.float32([kp.pt for kp in kps])
        return (kps, descs)


class CoverMatcher:
    def __init__(self, descriptor, coverPaths, ratio=0.7, minMatches=40,
                 useHamming=True):
        self.descriptor = descriptor
        self.coverPaths = coverPaths
        self.ratio = ratio
        self.minMatches = minMatches
        self.distanceMethod = "BruteForce"
        if useHamming:
            self.distanceMethod += "-Hamming"

    def search(self, queryKps, queryDescs):
        # initialize the dictionary of results
        results = {}

        # loop over the screen cover images
        for coverPath in self.coverPaths:
            cover = cv2.imread(coverPath)
            gray = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)
            (kps, descs) = self.descriptor.describe(gray)

            # query是待查图片的特征信息，后面的是当前数据库里每一张图片的信息
            score = self.match(queryKps, queryDescs, kps, descs)
            # 把分数存入字典，字典的键固定为50个，值为对应的匹配分
            results[coverPath] = score

        # if matches were found, sort them
        if len(results) > 0:
            results = sorted([(v, k) for (k, v) in results.items() if v > 0],
                             reverse=True)
        return results

    def match(self, kpsA, featuresA, kpsB, featuresB):
        # 新建一个描述匹配的对象，方法是BruteForce-Hamming
        matcher = cv2.DescriptorMatcher_create(self.distanceMethod)
        # 对两幅图片的特征描述做knn近邻匹配
        rawMatches = matcher.knnMatch(featuresB, featuresA, 2)
        matches = []

        for m in rawMatches:
            if len(m) == 2 and m[0].distance < m[1].distance * self.ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        # check to see if there are enough matches to process
        if len(matches) > self.minMatches:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i] for (i, _) in matches])
            ptsB = np.float32([kpsB[j] for (_, j) in matches])

            # compute the homography between the two sets of points
            # and compute the ratio of matched points
            (_, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, 4.0)

            # return the ratio of the number of matched keypoints
            # to the total number of keypoints
            return float(status.sum()) / status.size

        # no matches were found
        return -1.0

    # 封面图片的路径


coverPath = "covers"
# 待查询照片的路径
queryPath = "queries/query01.png"
queryPath = "queries/query02.png"
queryPath = "queries/query03.png"
queryPath = "queries/query04.png"
# queryPath = "queries/query05.png"

screenDatabasePath = "screens.csv"
screenDatabase = {}
for screen in csv.reader(open(screenDatabasePath)):
    screenDatabase[screen[0]] = screen[1:]


cd = CoverDescriptor()
# 封面匹配需要指定距离度量方法，例如Hamming
cm = CoverMatcher(cd, glob.glob(coverPath + "/*.png"), ratio=0.7, minMatches=40)

# 加载查询图像
queryImage = cv2.imread(queryPath)
# 降噪，转换成灰度图
gray = cv2.cvtColor(queryImage, cv2.COLOR_BGR2GRAY)
# 提取关键点和描述子
(queryKps, queryDescs) = cd.describe(gray)

# 注意这个cm是CoverMatcher，search是CoverMatcher里面的一个方法
# 在已有的数据库中进行匹配，返回匹配分数和匹配对象的路径，注意这里的路径表达里面有个转义字符
results = cm.search(queryKps, queryDescs)

# 显示出待查询的封面
cv2.imshow("query", queryImage)

# 如果在数据库里没有找到书的封面
if len(results) == 0:
    print("cannot find a match for that cover in databse!")
    cv2.waitKey(0)
else:
    # results的格式是[(0.9871794871794872, '路径\\文件名')]
    for i, (score, coverPath) in enumerate(results):
        # rfind和find不同，rfind找出最右边的字符
        # 在字典中查询coverPath对应的值，首先需要提取'路径\\文件名'中的'文件名'，注意这里需要使用转义反斜杠
        # 也可以这样使用coverPath.split('||')[-1]
        (author, title) = screenDatabase[coverPath[coverPath.rfind("\\") + 1:]]
        # (author,title) = screenDatabase[coverPath.split("\\")[-1]]

        # 打印输出结果，百分比保留2位小数点
        print("loop{} precision is {:.2f}%: author is {} - title is {}".format(i + 1, score * 100, author, title))
        # 这个coverPath是对应数据库文件里的图片
        result = cv2.imread(coverPath)
        cv2.imshow("results", result)
        cv2.waitKey(0)
cv2.destroyAllWindows()        
