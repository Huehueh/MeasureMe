import cv2
import numpy as np
import random
from utils import rescaleImage
import random as rng
from sheet_checker import getA4Candidates, checkSize
from drawing import drawA4FromThreeCorners, drawPoints

def findAllContours(image, use_imshow):
    width, height = image.shape
    contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    print("find contours")
    if use_imshow:
        contoursImage = np.zeros((width, height, 3),"uint8")
        cv2.drawContours(contoursImage, contours, -1, (0, 255, 0), 3)
        cv2.imshow("All contours", rescaleImage(25, contoursImage))
    return contours


def approximateContour(contour):
    peri = cv2.arcLength(contour, True)
    if peri < 100:
        return None
    epsilon = 0.005 * peri #0.005
    approx = cv2.approxPolyDP(contour, epsilon, True)
    return approx


def findA4(image, use_imshow):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    width, height = image.shape
    
    cnts = findAllContours(image, use_imshow)
    a4candidates = []
    approximations = []
    for contour in cnts[0:20]:
        approx = approximateContour(contour)
        if approx is None:
            continue
        approximations.append(approx)
        
        # Check if contour is A4
        corners, contour_candidates = getA4Candidates(approx, image)
        print(f"Corners {corners}; candidates {contour_candidates}")
        if contour_candidates is not None:
            a4candidates += contour_candidates
            break

        if use_imshow:
            approxImage = np.zeros((width, height, 3),"uint8")
            cv2.drawContours(approxImage, [approx], -1, (255, 0, 0), 8)
            if corners is not None:
                drawPoints(corners, approxImage, (155, 0, 0))
            if contour_candidates is not None:
                for candidates in contour_candidates:
                    drawPoints(candidates, approxImage, (255, 200, 100))
            cv2.imshow("approx", rescaleImage(25, approxImage))
            cv2.waitKey()

    # a4candidates = sorted(a4candidates, key=lambda x: checkSize(x["corners"][0], x["corners"][1], x["corners"][2]), reverse=True)

    if len(a4candidates) > 0:
        print(f"a4 candidates {a4candidates}")
        res = a4candidates[0]
        return res
    return None


def seperateShapes(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    width, height = image.shape
    thresh = width*height/10000

    # Make seperate shapes
    ret, labels = cv2.connectedComponentsWithAlgorithm(image, 4, cv2.CV_32S, cv2.CCL_DEFAULT)
    colors = []
    for k in range(ret):
        colors.append((random.randint(0,256),random.randint(0,256),random.randint(0,256)))

    # Making histotogram of values
    values = [0] * ret
    dst = np.zeros((width, height, 3),"uint8")
    for i in range(width):
        for j in range(height):
            label = labels[i][j]
            dst[i][j] = colors[label]
            values[label]+=1
    # valuesDict = {}
    # for i in range(len(values)):
    #     valuesDict[i] = values[i]
    # valuesDict = dict(sorted(valuesDict.items(), key=lambda x: x[1], reverse=True))
    

    shapes_image = np.zeros((width, height, 3),"uint8")
    for i in range(width):
        for j in range(height):
            label = labels[i][j]
            if label > 0: #  0  is te background (I suppose)
                if values[label] > thresh: # only n shapes from dict?
                    shapes_image[i][j] = colors[label]

    
    # cv2.imshow( "all components", rescaleImage(25, dst));
    cv2.imshow( "shapes", rescaleImage(25, shapes_image));
    cv2.imwrite("result/shapes.png", shapes_image)
    
    return shapes_image
