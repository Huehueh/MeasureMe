from imutils.perspective import four_point_transform
import cv2
import argparse
import os
from processing import *
import json
from display import threshAndEdges
from operations import seperateShapes, findA4, rescaleImage
from ruler import Ruler
from drawing import drawPoints

start = None
ruler = None

def draw_circle(event, x, y, flags, param):
    global start, ruler
    if event == cv2.EVENT_LBUTTONDOWN:        
        if start == None:
            start = (x, y)
            cv2.circle(image, start, 20, (255, 0, 0), -1)
        else:
            end = (x, y)
            cv2.circle(image, end, 20, (255, 0, 0), -1)
            cv2.line(image, start, end, (255, 0, 0), 4)

            length = ruler.measureLength(start, end)
            print(f"Zmierzono {length} mm")
            start = None



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
    use_imshow = True
    threshedImage = threshAndEdges(image)
    # shapesImage = seperateShapes(threshedImage)
    a4candidate = findA4(threshedImage, use_imshow)
    if use_imshow:        
        drawPoints(a4candidate, image, (1,1,1))
        cv2.imshow("Contours approximations", rescaleImage(25, image))
        cv2.waitKey()

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_circle)
    if a4candidate is not None:
        # drawPoints(a4candidate["corners"], image, (255, 0, 0))
        print(f"a4 candidate {a4candidate}")
        
        ruler = Ruler(a4candidate)
        warped = cv2.warpPerspective(image, ruler.transformation, (image.shape[0] * 2, image.shape[1] * 2))
        cv2.imshow("Warped", rescaleImage(25, warped))

        while(1):
            cv2.imshow(imageName, image)
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()    
    # cv2.waitKey()
