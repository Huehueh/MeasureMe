from imutils.perspective import four_point_transform
import cv2
import argparse
import os
from processing import doImageProcessing


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder", required=False, help="folder")
parser.add_argument("-i", "--image", required=False, help="image file")
args = vars(parser.parse_args())

if args["folder"] is not None:
    images = load_images_from_folder(args["folder"])
elif args["image"] is not None:
    print(args["image"])
    im = cv2.imread(args["image"])
    images = [im]
else:
    images = []

for image in images:
    doImageProcessing(image)
