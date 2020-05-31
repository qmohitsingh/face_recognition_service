
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from config import Constants
import time
from gevent.pywsgi import WSGIServer


from liveness import LivenessDetection

obj = LivenessDetection()
obj.load()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@app.route('/')
def hello_world():
    return 'Welcome to liveness detection ai'

@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@socketio.on('liveness_test')
def livness_detection_method(data):
    print('livness_detection_method scoket called')
    obj.liveness_detection(data)


if __name__ == '__main__':
    http_server = WSGIServer((Constants.HOST, Constants.PORT), app)
    print("Sever Started: http://localhost:5000")
    http_server.serve_forever()
