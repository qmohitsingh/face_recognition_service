from flask import request, jsonify
from flask_socketio import disconnect, emit
import functools
from component.users.user import User

from .auth import Auth


class Event:

    def __init__(self):
        self.session = Auth()

    def register_event(self, register):

        @register.socketio.on('connect')
        def connect():
            access_token = request.args.get('access_token')
            source_id = request.args.get('source_id')

            print("token", access_token, "source_id", source_id)

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

        @register.socketio.on('facial_recognition')
        @authenticated_only
        def facial_recognition_method(data):
            try:

                result = register.facematch.facial_recognition_method_by_socket(register.mysql, data["image"], data["user_id"])

                emit("facial_recognition_result", result)

            except Exception as e:
                    print("Error facial_recognition_method: ", e)
                    emit("facial_recognition_result", {
                        "status": 400,
                        "message": 'Something went wrong in face recognition'
                    })

        @register.socketio.on('update_user')
        @authenticated_only
        def add_user(data):
            try:
                print("add user mtho called")

                result = User.add_user_by_socket(register.mysql, register.facematch, data["image"], data["source_id"], data["user_id"], data["agent_id"])

                emit("update_user_result", result)

            except Exception as e:
                print("Error add_user: ", e)
                emit("update_user_result", {
                    "status": 400,
                    "message": 'Something went wrong while adding user'
                })


