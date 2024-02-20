import cv2
import math
import numpy as np
from sheet_checker import checkRatio
from transform import my_four_point_transform

class Ruler:
    longerMm = 297
    shorterMm = 210
    transformation = None

    def __init__(self, a4coordinates:[], transformation = None):
        if transformation is not None:
            if len(a4coordinates) < 3:
                raise ValueError('A4 should have at least three coordinates')
            elif len(a4coordinates) == 3:
                # print(a4coordinates)
                fourth = self.get_fourth_point(a4coordinates)
                print(f"fourth point: {fourth}")
                a4coordinates.append(fourth)
                # print(a4coordinates)
            self.transformation = transformation
            src = np.array([a4coordinates]).astype(np.float32)
            self.a4coordinates = cv2.perspectiveTransform(src, self.transformation)
        else:
            if len(a4coordinates) != 3:
                raise ValueError('A4 should have three coordinates')
            self.a4coordinates = a4coordinates
        
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