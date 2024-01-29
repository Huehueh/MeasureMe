import cv2
import numpy as np
import random
from utils import rescaleImage
import random as rng
from sheet_checker import checkIfIsA4, drawA4FromThreeCorners

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect


def my_four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (image.shape[0] * 2, image.shape[1] * 2))
    # return the warped image
    return warped


def findPolygons(image):    
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    width, height = image.shape
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    contours = np.zeros((width, height, 3),"uint8")
    cv2.drawContours(contours, cnts, -1, (0, 255, 0), 3)
    cv2.imshow("All contours", rescaleImage(25, contours))

    approxImage = np.zeros((width, height, 3),"uint8")
    for contour in cnts:
        # Perform contour approximation
        peri = cv2.arcLength(contour, True)
        if peri < 100:
            continue
        epsilon = 0.02 * peri #0.005
        approx = cv2.approxPolyDP(contour, epsilon, True)
            
        a4corners = checkIfIsA4(approx)
        if a4corners is not None:
            cv2.drawContours(approxImage, [approx], -1, (255, 0, 0), 3)
            cv2.drawContours(approxImage, [contour], -1, (0, 0, 255), 3)
            drawA4FromThreeCorners(a4corners, approxImage)
            break
    cv2.imwrite("result/polygons.png", approxImage)
    cv2.imshow("A4", rescaleImage(25, approxImage))

    return approxImage


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
