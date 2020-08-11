from flask import jsonify
from libraries.utils import compare_faces, base64_to_img, dump_pickle, load_pickle

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class User:

    @staticmethod
    def add_user(mysql, facematch, image, source_id, user_id, agent_id):
        try:

            embeds_data = facematch.get_face_embedding(image)

            pickle_data = dump_pickle(embeds_data['embeds'])
            # print("pickle_data data: ", pickle_data)
            mysql.save_embeds_by_userid(source_id, user_id, agent_id, pickle_data)

            return dict(data=dict(face_found=embeds_data['counter']), message='Image has been uploaded.')

        except Exception as e:
            logging.debug("Error add_user: ", e)
            raise

    @staticmethod
    def user_login(mysql, user_name, password):
        try:
            rows = mysql.login(user_name, password)

            logging.info("rows: ", rows)

            if rows is None:
                return {'message': "Invalid credentials."}

            logging.info("data post api: ", user_name, password)

            return dict(message="login successful", data=dict(user_id=rows[0], user_name=rows[1], name=rows[2]))
        except Exception as e:
            logging.debug("Error login: ", e)
            raise

    @staticmethod
    def add_user_by_socket(mysql, facematch, image, source_id, user_id, agent_id):
        try:
            embeds_data = facematch.get_face_embedding(image)

            pickle_data = dump_pickle(embeds_data['embeds'])
            logging.info("pickle_data data: ", pickle_data)
            mysql.save_embeds_by_userid(source_id, user_id, agent_id, pickle_data)

            return {
                "face_found": embeds_data['counter'],
                "message": 'Image has been uploaded.',
                "status": 200
            }

        except Exception as e:
            logging.debug("Error add_user: ", e)
            return {
                "status": 400,
                "message": 'Something went wrong.',
                "face_found": 0

            }