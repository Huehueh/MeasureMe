import unittest
import cv2
from sheet_checker import checkPerpendicular, checkOthogonal


class TextMath(unittest.TestCase):
    p1 = (1, 1)
    p2 = (1, 2)
    p3 = (2, 1)
    print(p1, p2, p3, checkPerpendicular(p1, p2, p3))
    print(p1, p3, p2, checkPerpendicular(p1, p2, p3))
    print(p1, p2, p3, checkPerpendicular(p1, p2, p3))
