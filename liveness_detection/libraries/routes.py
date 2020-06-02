import time

from .auth import Auth


class Route:

    def __init__(self):
        self.session = Auth()

    @staticmethod
    def register_route(register):

        @register.app.route('/')
        def hello_world():
            return 'Welcome to liveness detection ai'

        @register.app.route('/time')
        def get_current_time():
            return {'time': time.time()}

