from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import functools
from config import Constants
import time
from gevent.pywsgi import WSGIServer
from libraries.auth import Auth
from libraries.event import Event
from libraries.routes import Route
from db.mysql_lib import MySql
from component.recognition.face_match import FaceMatch

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class Server:
    def __init__(self):

        self.mysql = MySql()

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        CORS(self.app)

        #self.load_model()
        self.facematch = FaceMatch()

        #self.event = Event()
        self.route = Route()

        #self.event.register_event(self)
        self.route.register_route(self)

    # def load_model(self):
    #     self.liveness.load()

    def run(self):
        http_server = WSGIServer((Constants.HOST, Constants.PORT), self.app)
        logging.info("Sever Started: http://"+Constants.HOST+":"+str(Constants.PORT))
        http_server.serve_forever()

