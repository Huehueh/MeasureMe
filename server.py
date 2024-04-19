import tornado.ioloop
import tornado.web
import os
import cv2
import numpy as np
import json

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
                self.write({"corners": [[10, 20], [30, 40], [50, 60], [70, 80]], "id": filename})
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
