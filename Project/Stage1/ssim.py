def average(img):
    average = 0.0
    for i in range(28):
        for j in range(28):
            average += img[i][j]
    return average/(28*28)

def deviation(img, average):
    deviation = 0.0
    for i in range(28):
        for j in range(28):
            deviation += (img[i][j] - average) * (img[i][j] - average)
    return (deviation/(28*28 - 1))**0.5

def assit_function(img1, average1, img2, average2):
    deviation = 0.0
    for i in range(28):
        for j in range(28):
            deviation += (img1[i][j] - average1) * (img2[i][j] - average2)
    return deviation/(28*28 - 1)

def SSIM(img1 ,img2):
    K1 = 0.01
    K2 = 0.03
    L = 255
    C1 = (K1/L)*(K1/L)
    C2 = (K2/L)*(K2/L)
    C3 = C2/2
    average1 = average(img1)
    average2 = average(img2)

    L = (2*average1*average2 + C1)/(average1*average1 + average2*average2 + C1)

    deviation1 = deviation(img1, average1)
    deviation2 = deviation(img2, average2)

    C = (2 * deviation1 * deviation2 + C2) / (deviation1 * deviation1 + deviation2 * deviation2 + C2)

    deviation12 = assit_function(img1,average1,img2,average2)

    S = (deviation12 + C3)/(deviation1*deviation2 + C3)

    # print(L,":",C,":",S,":",L*C*S)
    return L*C*S