
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from config import Constants
import time
from gevent.pywsgi import WSGIServer


from component.face_match import facial_recognition



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@app.route('/')
def hello_world():
    return 'Welcome to liveness detection ai'

@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@socketio.on('hello owrk')
def liveness_test_socket(data):
    print('liveness_test aocke called', data)

@socketio.on('facial_recognition')
def facial_recognition_method(data):
    print('facial_recognition socket called')
    facial_recognition(data)


if __name__ == '__main__':
    http_server = WSGIServer((Constants.HOST, Constants.PORT), app)
    print("Sever Started: http://localhost:5001")
    http_server.serve_forever()
