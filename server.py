import tornado.ioloop
import tornado.web
import os

data_location = "server_data"

class MeasureHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Wyślij mi obrazek")

    def post(self):
        print("no elo")
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info["filename"], info["content_type"]
                body = info["body"]
                print(
                    'POST "%s" "%s" %d bytes', filename, content_type, len(body)
                )
                self.__save_file(filename, body)
        self.write({"corners": [[10, 20], [30, 40], [50, 60], [70, 80]]})

    def __make_path(self, name):
        return os.path.join(data_location, name)

    def __save_file(self, name, data):
        # extract timestamp of taking picture and use it as identificator
        if not os.path.exists(data_location):
            os.mkdir(data_location)
        base_image_path = self.__make_path(name)
        with open(base_image_path, "wb") as f:
            f.write(data)

def make_app():
    return tornado.web.Application([
        (r"/upload", MeasureHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
