
from main.server import Server


if __name__ == '__main__':
    # http_server = WSGIServer((Constants.HOST, Constants.PORT), app)
    # print("Sever Started: http://localhost:5000")
    # http_server.serve_forever()
    service = Server();
    service.run()
