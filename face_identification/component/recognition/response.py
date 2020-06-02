def succes_response(face_found, face_matched):
    result = {
        "statusCode": 200,
        "face_found_in_image": face_found,
        "face_matched": face_matched
    }

    return result


def no_face_detected():
    result = {
                "statusCode": 200,
                "message": "No face detected found."
            }

    return result


def more_faces_detected():
    result = {
                "statusCode": 200,
                "message": "more than one face detected."
            }

    return result
