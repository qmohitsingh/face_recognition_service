from flask import Flask, request
from flask_socketio import SocketIO, disconnect, emit
from flask_cors import CORS
import functools
from config import Constants
import time
from gevent.pywsgi import WSGIServer
from libraries.auth import Auth
from libraries.event import Event
from libraries.routes import Route

from component.liveness import LivenessDetection


class Server:
    def __init__(self):

        self.liveness = LivenessDetection()

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        CORS(self.app)

        self.load_model()

        self.event = Event()
        self.route = Route()

        self.event.register_event(self)
        self.route.register_route(self)


    def load_model(self):
        self.liveness.load()

    def run(self):
        http_server = WSGIServer((Constants.HOST, Constants.PORT), self.app)
        print("Sever Started: http://"+Constants.HOST+":"+str(Constants.PORT))
        http_server.serve_forever()

