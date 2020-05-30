import mysql.connector
from config import Constants
import logging
import traceback

#logger configuration
logging.basicConfig(level=logging.DEBUG, filename='face_recognition.log', format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        try:

            self.connection = mysql.connector.connect(
                user= Constants.USER_NAME,
                password= Constants.PASSWORD,
                host= Constants.HOST,
                database= Constants.DATABASE)

            self.cursor = self.connection.cursor()

            logger.info("created connection to mysql")

        except Exception as e:
            print("This file is running")
            logger.error("error in creating mysql connection", e)
            raise
        except:
            logger.error("uncaught exception: %s", traceback.format_exc())
            raise
        finally:
            self.cursor.close()
            self.connection.close()
