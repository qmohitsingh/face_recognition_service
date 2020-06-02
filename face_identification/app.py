from flask import jsonify
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from config import Constants
from flask import request
import time
from gevent.pywsgi import WSGIServer
from db.mysql_lib import MySqlConncetion
from libraries.utils import base64_to_img, dump_pickle, load_pickle

from component.face_match import facial_recognition, get_face_embedding

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

obj = MySqlConncetion()

@app.route('/')
def hello_world():
    return 'Welcome to liveness detection ai'

@app.route('/time')
def get_current_time():
    obj.get_all_embeddings()
    return {'time': time.time()}

@app.route('/add/user', methods = ['GET', 'POST'])
def add_user():
    try:
        if request.method == 'GET':
            """return the information for <user_id>"""
            return jsonify(result='hello user this get api for add user')

        if request.method == 'POST':

            data = request.form
            image = data['image']
            user_id = data['user_id']

            print("data post api: ", image, user_id)

            return jsonify(result='post request successful')
    except Exception as e:
        print("Error add_user: ", e)



@app.route('/update/user', methods = ['GET', 'POST'])
def update_user():
    try:
        if request.method == 'GET':
            """return the information for <user_id>"""
            return jsonify(result='hello user this get api for add user')

        if request.method == 'POST':

            data = request.form
            image = data['image']
            user_id = data['user_id']

            print("data post api: ", image, user_id)

            return jsonify(result='post request successful')
    except Exception as e:
        print("Error add_user: ", e)


@socketio.on('connect')
def connect():
    access_token = request.args.get('access_token')
    print("token", access_token)
    print("token", access_token)


@socketio.on('update_user')

def update_user_method(data):
    try:
        print("update_user socket called")
        image = data['image']
        user_id = data['user_id']

        embeds_data = get_face_embedding(image)

        #print("embeds data: ", embeds_data)

        if embeds_data['counter'] != 1:
            emit('update_user_result',
                 {"face_found": embeds_data['counter'],
                  "message": 'Image contain zero or more than one face.',
                  "status": 400
                  })
            return

        pickle_data = dump_pickle(embeds_data['embeds'])
        #print("pickle_data data: ", pickle_data)
        obj.save_embeds_by_userid(pickle_data, user_id)

        emit('update_user_result',
             {"face_found": embeds_data['counter'],
              "message": 'Image has been uploaded.',
              "status": 400
              }
             )

    except Exception as e:
        print("Error update_user_method: ", e)
        emit('update_user_result',
             {"face_found": 0,
              "message": 'Something went wrong.',
              "status": 400
              })


@app.route('/login', methods = ['GET', 'POST'])
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

            rows = obj.login(user_name, password)

            print("rows: ", rows)

            if rows is None:
                return jsonify(status=400, message="Invalid credentials.")



            print("data post api: ", user_name, password)

            return jsonify(
                status=200,
                message="login successful",
                data={"user_id": rows[0], "user_name": rows[1], "name": rows[2]}
            )

    except Exception as e:
        print("Error add_user: ", e)
        return jsonify(status=400, message='Failed to login')

@socketio.on('facial_recognition')
def facial_recognition_method(data):
    print('facial_recognition socket called')
    input_image = data['image']
    user_id = data['user_id']

    pickled_obj = obj.get_embeds_by_userid(user_id)
    saved_user_img = load_pickle(pickled_obj)

    #print("imag pickelD: ", saved_img)
    facial_recognition(input_image, saved_user_img, user_id)


if __name__ == '__main__':
    http_server = WSGIServer((Constants.HOST, Constants.PORT), app)
    print("Sever Started: http://0.0.0.0:5001")
    http_server.serve_forever()
