from flask import request, jsonify
from component.users.user import User
import sys

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
            logging.info('Hello world! Welcome to Face recognition detection ai')
            return 'Welcome to Face recognition detection ai'

        @register.app.route('/face/match', methods=['GET', 'POST'])
        def facial_recognition():
            try:
                if request.method == 'GET':
                    """return the information for <user_id>"""
                    return jsonify(result='hello user this get api for facial_recognition of a user')

                if request.method == 'POST':
                    logging.info('facial_recognition')

                    data = request.get_json()

                    #is_authenticated = self.session.authentication(data['access_token'], data['source_id'])

                    #if not is_authenticated:
                    #    return send_error({"status": 401, "message": 'Unauthorized Error.'})

                    result = register.facematch.facial_recognition_method(register.mysql, data["image"], data["source_id"], data["user_id"], data["agent_id"])

                    return send_success(result)

            except Exception as e:
                logging.debug("Something went wrong in face recognition: ", e)
                return send_error('Something went wrong in face recognition')

        @register.app.route('/add/user', methods=['GET', 'POST'])
        def add_user():
            try:
                if request.method == 'GET':
                    """return the information for <user_id>"""
                    return jsonify(result='hello user this get api for add user')

                if request.method == 'POST':
                    logging.info('add_user')

                    data = request.get_json()

                    is_authenticated = self.session.authentication(data['access_token'], data['source_id'])

                    if not is_authenticated:
                        return send_error({"status": 401, "message": 'Unauthorized Error.'})

                    result = User.add_user(register.mysql, register.facematch, data["image"], data["source_id"], data["user_id"], data["agent_id"])

                    return send_success(result)
            except Exception as e:
                logging.debug("Error add_user api: ", e)
                return send_error()

        # @register.app.route('/update/user', methods=['GET', 'POST'])
        # def update_user():
        #     try:
        #         if request.method == 'GET':
        #             """return the information for <user_id>"""
        #             return jsonify(result='hello user this get api for add user')
        #
        #         if request.method == 'POST':
        #             data = request.form
        #             image = data['image']
        #             user_id = data['user_id']
        #
        #             print("data post api: ", image, user_id)
        #
        #             return jsonify(result='post request successful')
        #     except Exception as e:
        #         print("Error add_user: ", e)

        @register.app.route('/login', methods=['GET', 'POST'])
        def login():
            try:
                if request.method == 'GET':
                    """return the information for <user_id>"""
                    return jsonify(result='login api...')

                if request.method == 'POST':

                    data = request.form
                    user_name = data['user_name']
                    password = data['password']

                    logging.info("data post api: ", user_name, password)

                    result = User.user_login(register.mysql, user_name, password)

                    return send_success(result)

            except Exception as e:
                logging.debug("Error add_user: ", e)
                return send_error(dict(message='Failed to login'))

