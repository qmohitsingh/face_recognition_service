import time

from .auth import Auth

from .utils import send_error, send_success


class Route:

    def __init__(self):
        self.session = Auth()

    @staticmethod
    def register_route(register):

        @register.app.route('/')
        def hello_world():
            return send_success('Welcome to liveness detection ai')

        @register.app.route('/time')
        def get_current_time():
            return send_success({"data": {'time': time.time()}})

