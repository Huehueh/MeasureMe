import cv2


def drawA4FromThreeCorners(corners, image):
    if corners is None or len(corners) != 3:
        return
    cv2.line(image, corners[0], corners[1], (0, 255, 0), 10)
    cv2.line(image, corners[0], corners[2], (0, 255, 0), 10)


def drawPoints(points, image, color):
    for point in points:
        cv2.circle(image, point, 25, color, cv2.FILLED)