from flask import request
from flask_socketio import disconnect, emit
import functools

from .utils import send_error, send_success

from .auth import Auth


class Event:

    def __init__(self):
        self.session = Auth()

    def register_event(self, register):

        @register.socketio.on('connect')
        def connect():
            access_token = request.args.get('access_token')
            source_id = request.args.get('source_id')
            #print("token", access_token, "source_id", source_id)
            return self.session.authentication(access_token, source_id)

        def authenticated_only(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                if not self.session.get_authentication():
                    emit('liveness_test_result',
                         {
                             "liveness_flag": -1,
                             "user_id": -1,
                             "message": 'Authentication failed'
                         })
                    disconnect()
                else:
                    return f(*args, **kwargs)

            return wrapped

        @register.socketio.on('liveness_test')
        @authenticated_only
        def liveness_detection_method(data):
            try:
                print("liveness_test_result called")
                result = register.liveness.get_liveness_result(data)
                emit("liveness_test_result", result)

            except Exception as e:
                print("e", e)
                emit("liveness_test_result", {
                    "status": 400,
                    "message": 'Something went wrong in face recognition'
                })
