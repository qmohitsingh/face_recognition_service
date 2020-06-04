from flask import jsonify
import numpy as np
import cv2
import torch
import base64
from libraries.utils import compare_faces, base64_to_img, dump_pickle, load_pickle
from config import Constants
from flask_socketio import emit
from .response import succes_response, more_faces_detected, no_face_detected

import logging
import traceback

# logger configuration
# logging.basicConfig(level=logging.DEBUG, filename='face_recognition.log',
#                     format='%(asctime)s %(levelname)s:%(message)s')
# logger = logging.getLogger(__name__)

from dface import MTCNN, FaceNet


class FaceMatch:

    def __init__(self):
        print("Loading Facenet model...")
        print("Loading mtcnn model...")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.mtcnn = MTCNN(self.device)
        self.facenet = FaceNet(self.device)
        print("Loading Facenet model done...")
        print("Loading mtcnn model done...")

    @staticmethod
    def get_boundingbox(box, w, h, scale=1.2):
        x1, y1, x2, y2 = box
        size = int(max(x2 - x1, y2 - y1) * scale)
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
        if size > w or size > h:
            size = int(max(x2 - x1, y2 - y1))
        x1 = max(int(center_x - size // 2), 0)
        y1 = max(int(center_y - size // 2), 0)
        size = min(w - x1, size)
        size = min(h - y1, size)
        return x1, y1, size

    def facial_recognition(self, image, saved_img, user_id=0):
        try:
            frames = []
            faces = []
            counter = 0

            encoded_data = image.split(',')[1]
            decoded_data = base64.b64decode(encoded_data)

            np_data = np.fromstring(decoded_data, np.uint8)
            colored_img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

            if colored_img is None:
                return

            height, width, channels = colored_img.shape

            # print("channel: ", colored_img.shape, colored_img)

            # convert the test image to gray image as opencv face detector expects gray images
            gray_img = cv2.cvtColor(colored_img, cv2.COLOR_BGR2RGB)

            frames.append(gray_img);

            print("detecting & extracting faces.")
            result = self.mtcnn.detect(frames)

            #print("list: ", result)

            for i, res in enumerate(result):
                if res is None:
                    continue
                # extract faces
                boxes, probs, lands = res
                for j, box in enumerate(boxes):
                    counter = counter + 1
                    # confidence of detected face
                    if probs[j] > 0.98:
                        h, w = frames[i].shape[:2]
                        x1, y1, size = self.get_boundingbox(box, w, h)
                        face = frames[i][y1:y1 + size, x1:x1 + size]
                        faces.append(face)

            # print("counter: ",counter)
            embeds = self.facenet.embedding(faces)

            # print("Ebedding: ", embeds)

            # print('compare embeds 1: ', embeds[0])
            # print('compare embeds 2: ', np.array(Constants.MOHIT))

            matched = compare_faces([embeds[0]], saved_img, 1)

            # print(matched, len(result), False if len(result) > 1 else matched)

            matched = 1 if matched else 0

            return {
                'data':
                    {
                        'face_found': len(result),
                        'face_matched': 0 if len(result) > 1 else matched,
                        "user_id": user_id,
                        "message": "success"
                    }
            }

        except Exception as e:
            print("Error facial_recognition: ", e)
            raise

    def get_face_embedding(self, image):
        try:
            frames = []
            faces = []
            counter = 0

            encoded_data = image.split(',')[1]
            decoded_data = base64.b64decode(encoded_data)

            np_data = np.fromstring(decoded_data, np.uint8)
            colored_img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

            if colored_img is None:
                return

            # convert the test image to gray image as opencv face detector expects gray images
            gray_img = cv2.cvtColor(colored_img, cv2.COLOR_BGR2RGB)

            frames.append(gray_img);

            print("detecting & extracting faces.")
            result = self.mtcnn.detect(frames)

            for i, res in enumerate(result):
                if res is None:
                    continue
                # extract faces
                boxes, probs, lands = res
                for j, box in enumerate(boxes):
                    counter = counter + 1
                    # confidence of detected face
                    if probs[j] > 0.98:
                        h, w = frames[i].shape[:2]
                        x1, y1, size = self.get_boundingbox(box, w, h)
                        face = frames[i][y1:y1 + size, x1:x1 + size]
                        faces.append(face)

            embeds = [] if counter > 1 else self.facenet.embedding(faces)

            if len(embeds) is 0:
                raise

            return {"embeds": embeds[0], "counter": counter}

        except Exception as e:
            print("Error get_face_embedding: ", e)
            raise

    def facial_recognition_method(self, mysql, input_image, source_id, user_id, agent_id):
        try:
            print('facial_recognition method called')

            pickled_obj = mysql.get_embeds_by_userid(source_id, user_id, agent_id)
            saved_user_img = load_pickle(pickled_obj)

            # print("imag pickelD: ", saved_img)
            return self.facial_recognition(input_image, saved_user_img, user_id)

        except Exception as e:
            print("Error facial_recognition_method: ", e)
            raise

    def facial_recognition_method_by_socket(self, mysql, input_image, source_id, user_id, agent_id):
        try:
            print('facial_recognition method called')

            pickled_obj = mysql.get_embeds_by_userid(source_id, user_id, agent_id)
            saved_user_img = load_pickle(pickled_obj)

            # print("imag pickelD: ", saved_img)
            result = self.facial_recognition(input_image, saved_user_img, user_id)

            return {
                "status": 200,
                "face_found": result['data']['face_found'],
                "face_matched": result['data']['face_matched'],
                "message": result['data']['message']
            }

        except Exception as e:
            print("Error facial_recognition_method: ", e)
            return {
                "status": 400,
                "message": 'Something went wrong in face recognition'
            }
