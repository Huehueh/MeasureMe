import cv2
import numpy as np
import random
from utils import rescaleImage
import random as rng
from sheet_checker import checkIfIsA4, checkSize
from drawing import drawA4FromThreeCorners, drawPoints


def findAllContours(image, use_imshow):
    width, height = image.shape
    contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
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


def findA4(image, file_saver=None):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    cnts = findAllContours(image, file_saver is None)
    print(f"Found {len(cnts)} contours on image")
    a4candidates = []
    approximations = []
    for contour in cnts:        
        approx = approximateContour(contour)
        if approx is None:
            continue
        approximations.append(approx)
        
        # Check if contour is A4
        a4corners_data = checkIfIsA4(approx, image)
        if a4corners_data is not None:
            a4candidates.append(a4corners_data)
    print(len(a4candidates), "candidates")
    # drawing contour approximations
    width, height = image.shape
    approxImage = np.zeros((width, height, 3),"uint8")
    cv2.drawContours(approxImage, approximations, -1, (255, 0, 0), 8)
    if file_saver is None:
        cv2.imshow("Contours approximations", rescaleImage(25, approxImage))
    else:
        file_saver.save("Contours_approximations", approxImage)

    if len(a4candidates) > 0:
        # drawing potential A4 corners
        a4candidates = sorted(a4candidates, key=lambda x: checkSize(x["corners"][0], x["corners"][1], x["corners"][2]), reverse=True)
        # coloredImage = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # for points in a4candidates:
        #     drawA4FromThreeCorners(points["corners"], coloredImage)

        return a4candidates[0]
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
