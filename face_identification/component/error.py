def unauthorized_error():
    return {"status_code": 401,"success": False, "message": "unauthorized error"}


def unknown_error():
    return {"status_code": 405, "success": False, "message": "some error occurred"}
