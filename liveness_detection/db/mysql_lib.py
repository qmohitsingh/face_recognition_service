import mysql.connector
from config import Constants
import logging
import traceback

#logger configuration
logging.basicConfig(level=logging.DEBUG, filename='face_recognition.log', format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class MySqlConncetion:
    def __init__(self):
        try:

            self.connection = mysql.connector.connect(
                user= Constants.USER_NAME,
                password= Constants.PASSWORD,
                host= Constants.HOST,
                database= Constants.DATABASE
            )

            self.cursor = self.connection.cursor()

            logger.info("created connection to mysql")
            print("Connected to mysql successfully..", self.cursor, self.connection.is_connected())

        except Exception as e:
            print("This file is running")
            logger.error("error in creating mysql connection", e)
            raise
        except:
            logger.error("uncaught exception: %s", traceback.format_exc())
            raise

    def get_embeds_by_userid(self, user_id):
        try:
            sql = "SELECT embedding FROM tb_embeddings WHERE is_deleted=%s AND user_id = %s"

            self.cursor.execute(sql, (0, user_id))
            rows = self.cursor.fetchone()
            self.connection.commit()

            #print('rows:', rows, rows[0])
            return rows[0]
        except Exception as e:
            print("Error: ", e)

    def save_embeds_by_userid(self, embeds, user_id):
        try:
            sql = "INSERT INTO tb_embeddings(user_id, embedding) " \
                  "VALUES (%s, %s) ON DUPLICATE " \
                  "KEY UPDATE embedding = %s "

            self.cursor.execute(sql, (user_id, embeds, embeds))
            self.connection.commit()

            return {"message": "success"}
        except Exception as e:
            print("Error: ", e)
            raise

    def login(self, user_name, password):
        try:

            sql = "SELECT user_id, user_name, name FROM tb_users " \
                  "WHERE user_name=%s AND password = %s AND is_deleted=%s"

            self.cursor.execute(sql, (user_name, password, 0))
            rows = self.cursor.fetchone()
            self.connection.commit()

            return rows

        except Exception as e:
            print("Error: ", e)
            raise