from flask import jsonify
import numpy as np
import cv2
import torch
import base64
from utils.utils import compare_faces
from config import Constants
from flask_socketio import emit
from .response import succes_response, more_faces_detected, no_face_detected

import logging
import traceback

# logger configuration
logging.basicConfig(level=logging.DEBUG, filename='face_recognition.log',
                    format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

from dface import MTCNN, FaceNet

device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(device)
facenet = FaceNet(device)


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


def facial_recognition(image, user_id=0):
    try:
        frames = []
        faces = []

        encoded_data = image.split(',')[1]
        decoded_data = base64.b64decode(encoded_data)

        np_data = np.fromstring(decoded_data, np.uint8)
        colored_img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

        if colored_img is None:
            return

        height, width, channels = colored_img.shape

        print("channel: ", colored_img.shape, colored_img)

        # convert the test image to gray image as opencv face detector expects gray images
        gray_img = cv2.cvtColor(colored_img, cv2.COLOR_BGR2RGB)

        frames.append(gray_img);

        print("detecting & extracting faces.")
        result = mtcnn.detect(frames)

        for i, res in enumerate(result):
            if res is None:
                continue
            # extract faces
            boxes, probs, lands = res
            for j, box in enumerate(boxes):
                # confidence of detected face
                if probs[j] > 0.98:
                    h, w = frames[i].shape[:2]
                    x1, y1, size = get_boundingbox(box, w, h)
                    face = frames[i][y1:y1 + size, x1:x1 + size]
                    faces.append(face)

        embeds = facenet.embedding(faces)

        print("Ebedding: ", embeds)

        matched = compare_faces([embeds[0]], np.array(Constants.MOHIT), 1)

        print(matched, len(result), False if len(result) > 1 else matched)

        matched = 1 if matched else 0


        emit('facial_recognition_result',
                    {
                        'face_found': len(result),
                        'face_matched': 0 if len(result) > 1 else matched,
                        "user_id": user_id
                    })
        return


    except Exception as e:
        logger.error("error in matching faces")
        logger.error(e)
        emit('facial_recognition_result',
             {
                 'face_found': 0,
                 'face_matched': 0 ,
                 "user_id": user_id
             })
        
        logger.error(e, exc_info=True)
        raise
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        raise
