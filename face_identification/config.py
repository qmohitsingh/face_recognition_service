import json

with open('config.json') as config_file:
    CONFIG = json.load(config_file)


class Constants:
    HOST = CONFIG.get("HOST")
    PORT = CONFIG.get("PORT")
    DATABASE = CONFIG.get("DATABASE")
    USER_NAME = CONFIG.get("USER_NAME")
    PASSWORD = CONFIG.get("PASSWORD")
    DATABASE_HOST = CONFIG.get("DATABASE_HOST")