import cv2
from operations import my_four_point_transform
from sheet_checker import checkIfIsA4
import math
import numpy as np


def doImageProcessing(image):
    dst = cv2.Canny(image, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)

    cv2.imwrite("temp/Standard Hough Line Transform.jpg", cdst)
    cv2.imwrite("temp/Probabilistic Line Transform.jpg", cdstP)

    # Load image, grayscale, Gaussian blur, Otsu's threshold
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur = cv2.GaussianBlur(gray, (7, 7), 0)
    # # eq = cv2.equalizeHist(blur)
    # cv2.imwrite("temp/blur.png", blur)
    # # thresh = cv2.threshold(blur, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY)[1]
    # cv2.imwrite("temp/thresh.png", thresh)
    # adThresh = cv2.adaptiveThreshold(
    #     blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    # )
    # cv2.imwrite("temp/adThresh.png", adThresh)
    # canny = cv2.Canny(blur, 100, 200)
    # cv2.imwrite("temp/canny.png", canny)
    # img_neg = 255 - canny
    # # Show the image
    # cv2.imwrite("temp/negative.png", img_neg)
    # # erosion_size = 1
    # # element = cv2.getStructuringElement(
    # #     cv2.MORPH_ELLIPSE,
    # #     (2 * erosion_size + 1, 2 * erosion_size + 1),
    # #     (erosion_size, erosion_size),
    # # )
    # # img_neg = cv2.erode(img_neg, element, iterations=3)
    # # # img_neg = cv2.dilate(img_neg, (10, 10), iterations=3)
    # cv2.imwrite("temp/negative_dilate.png", img_neg)

    # added = cv2.bitwise_and(thresh, img_neg)
    # erosion_size = 1
    # element = cv2.getStructuringElement(
    #     cv2.MORPH_ELLIPSE,
    #     (2 * erosion_size + 1, 2 * erosion_size + 1),
    #     (erosion_size, erosion_size),
    # )
    # added = cv2.erode(added, element, iterations=3)
    # # added = cv2.dilate(added, element, iterations=3)
    # cv2.imwrite("temp/added.png", added)

    # # Find contours and sort for largest contour
    # cnts = cv2.findContours(added, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # contours = image.copy()
    # approxImage = image.copy()
    # cornersImage = image.copy()
    # cv2.drawContours(contours, cnts, -1, (0, 255, 0), 3)
    # cv2.imwrite("temp/contours.png", contours)

    # for contour in cnts:
    #     # Perform contour approximation- no
    #     # print("Contour", contour)

    #     peri = cv2.arcLength(contour, True)
    #     if peri < 100:
    #         continue
    #     approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    #     #     cv2.drawContours(image, [contour], -1, (0, 255, 0), 3)
    #     cv2.drawContours(approxImage, [approx], -1, (255, 0, 0), 3)

    #     corners = checkIfIsA4(approx)
    #     if corners is not None:
    #         # for p in corners:
    #         # cv2.circle(image, p, 10, (255, 100, 100), 2)
    #         cv2.line(cornersImage, corners[0], corners[1], (0, 255, 0), 2)
    #         cv2.line(cornersImage, corners[0], corners[2], (0, 255, 0), 2)

    #         longer_edge = max(
    #             math.dist(corners[0], corners[1]), math.dist(corners[0], corners[2])
    #         )  # 297
    #         p1 = (762, 766)
    #         p2 = (1590, 669)
    #         cv2.line(cornersImage, p1, p2, (0, 255, 255), 2)
    #         x = math.dist(p1, p2) * 29.7 / longer_edge
    #         print(f"Dlugosc ubranka to {x} cm")

    #     # warped = my_four_point_transform(image, approx.reshape(4, 2))
    #     # cv2.imwrite("temp/warped.png", warped)
    #     # break

    # cv2.imwrite("temp/approxImage.png", approxImage)
    # cv2.imwrite("temp/cornersImage.png", cornersImage)

    # # for i in range(len(approx)):
    # #     print(approx[i])
    # #     if i < len(approx) - 1:
    # #         res = cv2.norm(approx[i + 1] - approx[i])
    # #     else:
    # #         res = cv2.norm(approx[i] - approx[0])
    # #     # print("Len", res)
