import cv2
import math
import numpy as np
from sheet_checker import checkRatio

class Ruler:
    longerMm = 297
    shorterMm = 210
    transformation = None

    def __init__(self, a4coordinates):
        self.a4coordinates = a4coordinates
        if len(self.a4coordinates) == 3:
            self.a4coordinates.append(self.get_fourth_point(self.a4coordinates))
        self.transformation = self.my_four_point_transform(self.a4coordinates)
        src = np.array([self.a4coordinates]).astype(np.float32)
        self.a4coordinates = cv2.perspectiveTransform(src, self.transformation)

        sideA = math.dist(a4coordinates[0], a4coordinates[1])
        sideB = math.dist(a4coordinates[0], a4coordinates[2])
        if sideA > sideB:
            self.longerSide = sideA
            self.shorterSide = sideB
        else:
            self.longerSide = sideA
            self.shorterSide = sideB

        pixelsPerMm1 = self.longerSide/self.longerMm
        pixelsPerMm2 = self.shorterSide/self.shorterMm

        print("Wspolczynniki", pixelsPerMm1, pixelsPerMm2)
        self.pixelsPerMm = (pixelsPerMm1 + pixelsPerMm2) / 2

    @staticmethod
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

    @staticmethod
    def my_four_point_transform(pts):
        pts = np.array(pts)
        for point in pts:
            point[0] -= 2000
            point[1] -= 2000
        # obtain a consistent order of the points and unpack them
        # individually
        print(f"Points {pts}")
        rect = Ruler.order_points(pts)
        print(rect)
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
        transformation = cv2.getPerspectiveTransform(rect, dst)
        print("Transformation", transformation)
        return transformation


    def brute_force_get_fourth_point(self, points:[]):
        corner, a, b = points
        shift = (corner[0] - a[0], corner[1] - a[1])
        # print("Shift", shift)
        return b - shift


    def get_fourth_point(self, points):
        return self.brute_force_get_fourth_point(points)


    def measureLength(self, startPoint, endPoint):
        if self.transformation is not None:
            src = np.array([[startPoint, endPoint]]).astype(np.float32)
            transformedPoints = cv2.perspectiveTransform(src, self.transformation)
            print("TP", transformedPoints)
            [startPoint, endPoint] = transformedPoints[0]
            print(f"start {startPoint}, end {endPoint}")
        distancePixels = math.dist(startPoint, endPoint)
        distanceMm = int(distancePixels / self.pixelsPerMm)
        return distanceMm