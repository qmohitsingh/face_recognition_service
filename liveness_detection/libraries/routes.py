import time
from flask import request, jsonify

from .auth import Auth

from .utils import send_error, send_success

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Route:

    def __init__(self):
        self.session = Auth()


    def register_route(self, register):

        @register.app.route('/')
        def hello_world():
            logging.info('Welcome to liveness detection ai')
            return send_success('Welcome to liveness detection ai')

        @register.app.route('/time')
        def get_current_time():
            logging.info({"data": {'time': time.time()}})
            return send_success({"data": {'time': time.time()}})

        @register.app.route('/liveness', methods=['GET', 'POST'])
        def liveness_test():
            try:
                if request.method == 'GET':
                    """return the information for <user_id>"""
                    return jsonify(result='hello user this get api for facial_recognition of a user')

                if request.method == 'POST':
                    logging.info('liveness_test method called')
                    data = request.get_json()

                    #is_authenticated = self.session.authentication(data['access_token'], data['source_id'])

                    #if not is_authenticated:
                    #    logging.debug({"status": 401, "message": 'Unauthorized Error.'})
                    #    return send_error({"status": 401, "message": 'Unauthorized Error.'})

                    result = register.liveness.get_liveness_result(
                        data["image"], data["source_id"], data["user_id"], data["agent_id"]
                    )
                    return send_success(result)

            except Exception as e:
                logging.debug("Something went wrong in face recognition: ")
                return send_error('Something went wrong in face recognition', e)

