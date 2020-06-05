import mysql.connector
from config import Constants
import logging
import traceback

# # logger configuration
# logging.basicConfig(level=logging.DEBUG, filename='face_recognition.log',
#                     format='%(asctime)s %(levelname)s:%(message)s')
# logger = logging.getLogger(__name__)


class MySql:
    def __init__(self):
        try:

            self.connection = mysql.connector.connect(
                user=Constants.USER_NAME,
                password=Constants.PASSWORD,
                host=Constants.DATABASE_HOST,
                database=Constants.DATABASE,
                connection_timeout=86400
            )

            self.cursor = self.connection.cursor()

            #logger.info("created connection to mysql")
            print("Connected to mysql successfully..", self.cursor, self.connection.is_connected())

        except Exception as e:
            print("This file is running", e)
            #logger.error("error in creating mysql connection", e)
            raise

    def get_embeds_by_userid(self, source_id, user_id, agent_id):
        try:
            sql = "SELECT embedding FROM tb_face_embeddings " \
                  "WHERE is_deleted=%s AND source_id = %s AND user_id = %s AND agent_id = %s"

            self.cursor.execute(sql, (0, source_id, user_id, agent_id))
            rows = self.cursor.fetchone()
            self.connection.commit()

            # print('rows:', rows, rows[0])
            return rows[0]
        except Exception as e:
            print("Error: ", e)
            raise

    def save_embeds_by_userid(self, source_id, user_id, agent_id, embedding):
        try:
            # sql = "INSERT INTO tb_face_embeddings(source_id, user_id, agent_id, embedding) " \
            #       "VALUES (%s, %s,%s, %s) "
            #
            # self.cursor.execute(sql, (source_id, user_id, agent_id, embedding))

            sql = "INSERT INTO tb_face_embeddings(source_id, user_id, agent_id, embedding) " \
                  "VALUES (%s, %s,%s, %s) ON DUPLICATE KEY UPDATE embedding = %s;"

            self.cursor.execute(sql, (source_id, user_id, agent_id, embedding, embedding))
            self.connection.commit()

            return {"message": "Image has been uploaded."}
        except Exception as e:
            print("Error save_embeds_by_userid: ", e)
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
            print("Error login: ", e)
            raise
