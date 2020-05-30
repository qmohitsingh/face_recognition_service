
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from config import Constants
import time
from gevent.pywsgi import WSGIServer
from face_identification.face_match import facial_recognition as FR
#from liveness_detection.d emoimport liveness


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@app.route('/')
def hello_world():
    return 'Welcome to liveness detection ai'

@app.route('/time')
def get_current_time():
    return {'time': time.time()}



# @socketio.on('catch-frame')
# def catch_frame(data):
#     detectFaceUltraLight(data)


# @socketio.on('detected_frames')
# def catch_frame(data):
#     face_recognition(data)

@socketio.on('catch-frame')
def liveness_test_socket(data):
    print('liveness_test aocke called')

@socketio.on('facial_recognition')
def facial_recognition(data):
    print('facial_recognition socket called')
    FR(data)


if __name__ == '__main__':
    http_server = WSGIServer((Constants.HOST, Constants.PORT), app)
    print("Sever Started: http://localhost:5000")
    http_server.serve_forever()
