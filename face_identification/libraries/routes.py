from flask import request, jsonify
from component.users.user import User

from .auth import Auth


class Route:

    def __init__(self):
        self.session = Auth()

    def register_route(self, register):

        @register.app.route('/')
        def hello_world():
            return 'Welcome to liveness detection ai'

        @register.app.route('/face/match', methods=['GET', 'POST'])
        def facial_recognition():
            try:
                if request.method == 'GET':
                    """return the information for <user_id>"""
                    return jsonify(result='hello user this get api for facial_recognition of a user')

                if request.method == 'POST':
                    data = request.form

                    is_authenticated = self.session.authentication(data['access_token'], data['source_id'])

                    if not is_authenticated:
                        return jsonify(status=401, message='Unauthorized Error.')

                    return register.facematch.facial_recognition_method(register.mysql, data["image"], data["user_id"])

            except Exception as e:
                print("Error add_user: ", e)
                return jsonify(
                    status=400,
                    message='Something went wrong in face recognition'
                )

        @register.app.route('/add/user', methods=['GET', 'POST'])
        def add_user():
            try:
                if request.method == 'GET':
                    """return the information for <user_id>"""
                    return jsonify(result='hello user this get api for add user')

                if request.method == 'POST':
                    data = request.form

                    is_authenticated = self.session.authentication(data['access_token'], data['source_id'])

                    if not is_authenticated:
                        return jsonify(status=401, message='Unauthorized Error.')

                    return User.add_user(register.mysql, register.facematch, data["image"], data["source_id"], data["user_id"], data["agent_id"])

            except Exception as e:
                print("Error add_user: ", e)
                return jsonify(
                    status=400,
                    message='Something went wrong in face recognition'
                )

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

                    print("data post api: ", user_name, password)

                    return User.user_login(register.mysql, user_name, password)

            except Exception as e:
                print("Error add_user: ", e)
                return jsonify(status=400, message='Failed to login')

