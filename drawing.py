import cv2
from typing import List

def drawA4FromThreeCorners(corners, image):
    if corners is None or len(corners) != 3:
        return
    cv2.line(image, corners[0], corners[1], (0, 255, 0), 10)
    cv2.line(image, corners[0], corners[2], (0, 255, 0), 10)


def drawPoints(a4: List[List], image, color):
    for point in a4:
        cv2.circle(image, (point[0], point[1]), 25, color, cv2.FILLED)
        