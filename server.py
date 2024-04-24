import tornado.ioloop
import tornado.web
import os
import cv2
import numpy as np
import json

from display import thresh_and_edges_headless
from operations import seperateShapes, findA4, rescaleImage
from ruler import Ruler

data_location = "server_data"


class FilePathGenerator:
    def __init__(self, name):
        self.name = name
        self.directory = self.__extract_directory()
        self.path = self.__make_path()

    def save_input_file(self, data):
        self.__save_file(self.get_input_path(), data)

    def get_input_path(self):
        return os.path.join(self.path, self.name)

    def save_meta_file(self, data):
        with open(self.get_meta_path(), 'w') as f:
            json.dump(data, f)

    def get_meta_path(self):
        return os.path.join(self.path, "metadata.json")

    def __save_file(self, filepath, data):
        if not os.path.exists(data_location):
            os.mkdir(data_location)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        with open(filepath, "wb") as f:
            f.write(data)

    def __extract_directory(self):
        directory, _ = os.path.splitext(self.name)
        return directory

    def __make_path(self):
        return os.path.join(data_location, self.directory)


class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Wyślij mi obrazek")

    def post(self):
        print("nowy obrazek!")

        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info["filename"], info["content_type"]
                body = info["body"]
                print(f'nazywa się {filename} i ma {len(body)} bajtów  content type to {content_type}')
                path_generator = FilePathGenerator(filename)
                path_generator.save_input_file(body)
                image = cv2.imdecode(np.frombuffer(body, np.uint8), cv2.IMREAD_COLOR)
                threshed_image = thresh_and_edges_headless(image)
                a4candidate = findA4(threshed_image, use_imshow=False)
                if a4candidate is None:
                    self.write({"corners": [[0, 0], [0, 0], [0, 0], [0, 0]], "id": filename})
                print(a4candidate)
                a4candidate['corners'] = [a.tolist() for a in a4candidate['corners']]
                path_generator.save_meta_file(a4candidate)
                self.write({"corners": a4candidate['corners'], "id": filename})
                return


class MeasureHandler(tornado.web.RequestHandler):
    def post(self):
        print("pomiary ")
        data = json.loads(self.request.body)
        print(data)
        if 'id' in data:
            print(f"id: {data['id']}")
        if 'coordinates' in data:
            print(f"coordinates: {data['coordinates']}")
        path_generator = FilePathGenerator(data['id'])
        data_path = path_generator.get_meta_path()
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                data = json.load(f)
                data['corners'] = [np.array(a) for a in data['corners']]
                ruler = Ruler(data)
                result = ruler.measureLength(data['coordinates'])
                self.write({"measurement": result})
                return
        # here will read file names "base" from './server_data/id' directory then
        # call measurement by coordinates to generate result
        result = 42
        self.write({"measurement": result})


def make_app():
    path_to_serve = os.path.join(os.getcwd(), data_location)
    return tornado.web.Application([
        (r"/upload", UploadHandler),
        (r"/measure", MeasureHandler),
        (r"/image/(.*)", tornado.web.StaticFileHandler, {'path': path_to_serve}),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
