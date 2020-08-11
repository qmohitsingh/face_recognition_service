import requests
from config import Constants

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Auth:
    def __init__(self):
        self.isAuthenticated = True

    def authentication(self, access_token, source_id):

        try:

            if int(source_id) is Constants.TOOKAN_SOURCE_ID:
                return self.verify_authentication_tookan(access_token)

            return False

        except Exception as error:
            logging.debug("set_authentication(Auth Class): ", error)
            return False

    def verify_authentication_tookan(self, access_token):
        try:
            payload = {'access_token': access_token}

            url = Constants.AUTH_URL + Constants.GET_ADD_ONS_URL

            response = requests.post(url, data=payload).json()

            #print("response: ", response)

            if response["status"] is 101:
                logging.info("Session expired. please login again.")

            if response['status'] != 200:
                return self.isAuthenticated

            for add_on in response["data"]["add_ons"]:

                self.isAuthenticated = False

                if add_on["add_on_type"] is Constants.ADD_ON_TYPE:
                    self.isAuthenticated = True
                    break

            return self.isAuthenticated
        except Exception as error:
            logging.debug("set_authentication(Auth Class): ", error)
            return False

    def get_authentication(self):
        return self.isAuthenticated
