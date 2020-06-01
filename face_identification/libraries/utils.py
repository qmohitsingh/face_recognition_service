import numpy as np
import pickle
import base64
import cv2
import codecs

# Euclidean Distance Caculator
def face_distance(face_encodings, face_to_compare):
    """
    Given a list of face encodings, compare them to a known face encoding and get a euclidean distance
    for each comparison face. The distance tells you how similar the faces are.

    :param faces: List of face encodings to compare
    :param face_to_compare: A face encoding to compare against
    :return: A numpy ndarray with the distance for each face in the same order as the 'faces' array
    """
    distance = np.linalg.norm(face_encodings - face_to_compare, axis=1)
    print("distance: ", distance, distance[0] < 1)
    return distance[0]



def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    """
    Compare a list of face encodings against a candidate encoding to see if they match.

    :param known_face_encodings: known face encodings
    :param face_encoding_to_check: A single face encoding to compare against the list
    :param tolerance: How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance.
    :return: A list of True/False values indicating which known_face_encodings match the face encoding to check
    """
    return face_distance(known_face_encodings, face_encoding_to_check) <= tolerance

# Euclidean Distance Caculator
def dist(a, b, ax=1):
    result =  np.linalg.norm(a - b, axis=ax)
    print("distance: ", result)
    print('[0.73910816 :', result[0] < 1)
    return result[0] < 1


def dump_pickle(embed):
    return codecs.encode(pickle.dumps(embed), "base64").decode()

def load_pickle(embed):
    return pickle.loads(codecs.decode(embed.encode(), "base64"))


def base64_to_img(image):
    encoded_data = image.split(',')[1]
    decoded_data = base64.b64decode(encoded_data)

    np_data = np.fromstring(decoded_data, np.uint8)
    return cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)