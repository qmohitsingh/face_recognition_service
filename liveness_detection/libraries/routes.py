import time
from flask import request, jsonify

from .auth import Auth

from .utils import send_error, send_success


class Route:

    def __init__(self):
        self.session = Auth()


    def register_route(self, register):

        @register.app.route('/')
        def hello_world():
            return send_success('Welcome to liveness detection ai')

        @register.app.route('/time')
        def get_current_time():
            return send_success({"data": {'time': time.time()}})

        @register.app.route('/liveness', methods=['GET', 'POST'])
        def liveness_test():
            try:
                if request.method == 'GET':
                    """return the information for <user_id>"""
                    return jsonify(result='hello user this get api for facial_recognition of a user')

                if request.method == 'POST':

                    data = request.get_json()

                    is_authenticated = self.session.authentication(data['access_token'], data['source_id'])

                    if not is_authenticated:
                        return send_error({"status": 401, "message": 'Unauthorized Error.'})

                    result = register.liveness.get_liveness_result(
                        data["image"], data["source_id"], data["user_id"], data["agent_id"]
                    )

                    return send_success(result)

            except Exception as e:
                print("Error add_user: ", e)
                return send_error('Something went wrong in face recognition')

