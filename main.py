from imutils.perspective import four_point_transform
import cv2
import argparse
import os
from processing import *
import json
from display import threshAndEdges
from operations import seperateShapes, findA4, rescaleImage
from drawing import drawPoints



def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = os.path.join(folder, filename)
        images.append(img)
    return images


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder", required=False, help="folder")
parser.add_argument("-i", "--image", required=False, help="image file")
args = vars(parser.parse_args())

if args["folder"] is not None:
    images = load_images_from_folder(args["folder"])
elif args["image"] is not None:
    im = args["image"]
    images = [im]
else:
    images = []

measureFile = open("test/data.json")
measureData = json.load(measureFile)

for imageName in images:
    # for data in measureData["image files"]:
    #     if data["name"] == imageName:
    #         points = data["points"]
    #         size = data["size"]
    #         image = cv2.imread(imageName)
    image = cv2.imread(imageName, cv2.IMREAD_COLOR)
    if image is None:
        print("NO IMAGE")
        break
    threshedImage = threshAndEdges(image)
    # shapesImage = seperateShapes(threshedImage)
    a4candidate = findA4(threshedImage)
    if a4candidate is not None:
        drawPoints(a4candidate, image, (255, 0, 0))
        cv2.imshow("Original with A4 candidates", rescaleImage(25, image))
    cv2.waitKey()
