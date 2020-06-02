from flask import request
from flask_socketio import disconnect, emit
import functools
import time

from .auth import Auth


class Event:

    def __init__(self):
        self.session = Auth()

    def register_event(self, register):

        @register.app.route('/')
        def hello_world():
            return 'Welcome to liveness detection ai'

        @register.app.route('/time')
        def get_current_time():
            return {'time': time.time()}

        @register.socketio.on('connect')
        def connect():
            access_token = request.args.get('access_token')
            source_id = request.args.get('source_id')
            print("token", access_token, "source_id", source_id)
            is_authenticate = self.session.authentication(access_token, source_id)
            return is_authenticate

        def authenticated_only(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                if not self.session.get_authentication():
                    emit('liveness_test_result',
                         {"liveness_flag": -1, "user_id": -1, "message": 'Authentication failed'})
                    disconnect()
                else:
                    return f(*args, **kwargs)

            return wrapped

        @register.socketio.on('liveness_test')
        @authenticated_only
        def livness_detection_method(data):
            print('livness_detection_method scoket called')
            register.liveness.liveness_detection(data)