import requests
import os
import argparse


def fix_name(input_string):
    remove_punctuation_map = dict((ord(char), None) for char in '*?:"<>|')
    result = input_string.translate(remove_punctuation_map)
    if not result.lower().endswith('.jpg'):
        result += ".jpg"
    return result


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder",  help="folder", default="download")
parser.add_argument("-a", "--address", help="image file", default='https://plac.dynu.net')

args = vars(parser.parse_args())
address = args['address']
target_path = args['folder']

try:
    request_images = requests.get(address+'/upload')
    list_images = request_images.json()
    print(f'Found {len(list_images)} images!')
    count = 0
    for directory, files in list_images.items():
        for file in files:
            if directory in file:
                path_on_server = address+'/image/'+directory+'/'+file
                image_path = fix_name(os.path.join(target_path, file))
                if os.path.exists(image_path):
                    print("Already downloaded", path_on_server)
                    continue
                print(path_on_server)
                count += 1
                request_image = requests.get(path_on_server)
                if not os.path.exists(target_path):
                    os.mkdir(target_path)
                with open(image_path, 'wb') as f:
                    f.write(request_image.content)
    print(f"Downloaded {count} new images!")
except:
    print("Couldn't get list of images")