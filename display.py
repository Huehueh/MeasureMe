import cv2
import numpy as np
# from shi_tomasi import goodFeaturesToTrack_Demo
from utils import rescaleImage
from operations import seperateShapes

result_image = "threshold and edges"
canny_window = "canny"
thr_window = "threshold"

scale_percent = 25 # percent of original size

def nothing(x): 
    pass

def threshAndEdges(image):
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow(result_image)
    cv2.namedWindow(canny_window)
    cv2.namedWindow(thr_window)

    cv2.createTrackbar("blur kernel size", result_image, 3, 7, nothing)
    cv2.setTrackbarMin("blur kernel size", result_image, 3)

    cv2.createTrackbar("threshold", thr_window, 150, 255, nothing)

    cv2.createTrackbar("canny thr1", canny_window, 5, 255, nothing)
    cv2.createTrackbar("canny thr2", canny_window, 52, 255, nothing)

    # key=0
    while(True):
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break        

        blurSize = cv2.getTrackbarPos("blur kernel size", result_image) 
        blurSize = 2*blurSize+1
        blur_image = cv2.GaussianBlur(gray_image, (blurSize, blurSize), 0)

        threshold = cv2.getTrackbarPos("threshold", thr_window) 
        # threshold = 100
        # _, thresholdedImage = cv2.threshold(blur_image, threshold, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, thresholdedImage = cv2.threshold(blur_image, threshold, 255, cv2.THRESH_BINARY)
        # cv2.createButton('do_threshold', lambda , [40, 50], 1, 0)

        thr1 = cv2.getTrackbarPos("canny thr1", canny_window)
        thr2 = cv2.getTrackbarPos("canny thr2", canny_window)
        contoursImage = cv2.Canny(blur_image, thr1, thr2)
        
        dilate_size = 1
        element = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (2 * dilate_size + 1, 2 * dilate_size + 1),
            (dilate_size, dilate_size),
        )
        contoursImage = cv2.dilate(contoursImage, element, iterations=3)
        contoursImage = 255 - contoursImage

        added = cv2.bitwise_and(thresholdedImage, contoursImage)
 
        cv2.imshow(result_image, rescaleImage(scale_percent, added))
        cv2.imshow(thr_window, rescaleImage(scale_percent, thresholdedImage))
        cv2.imshow(canny_window, rescaleImage(scale_percent, contoursImage))

    cv2.destroyAllWindows()
    cv2.imwrite("result/added.png", added)
    return added