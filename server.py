import tornado.ioloop
import tornado.web
import os
import cv2
import numpy as np

data_location = "server_data"
base_url = "upload"


class ImageWaiter(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path: str) -> str:
        if not url_path or url_path.endswith('/'):
            url_path = url_path + base_url
        return url_path


class MeasureHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Wyślij mi obrazek")

    def post(self):
        print("no elo")
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info["filename"], info["content_type"]
                body = info["body"]
                print('POST "%s" "%s" %d bytes', filename, content_type, len(body))
                self.__save_file(filename, body)
                image = cv2.imdecode(np.frombuffer(body, np.uint8), cv2.IMREAD_COLOR)

        self.write({"corners": [[10, 20], [30, 40], [50, 60], [70, 80]]})

    def __make_base_path(self, name):
        base_name, _ = os.path.splitext(name)
        return os.path.join(data_location, base_name)

    def __save_file(self, name, data):
        # extract timestamp of taking picture and use it as identificator
        if not os.path.exists(data_location):
            os.mkdir(data_location)
        base_image_path = self.__make_base_path(name)
        if not os.path.exists(base_image_path):
            os.mkdir(base_image_path)
        image_path = os.path.join(base_image_path, name)
        with open(image_path, "wb") as f:
            f.write(data)


def make_app():
    path_to_serve = os.path.join(os.getcwd(), data_location)
    return tornado.web.Application([
        (r"/"+base_url, MeasureHandler),
        (r"/image/(.*)", ImageWaiter, {'path': path_to_serve}),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
