import json

with open('config.json') as config_file:
    CONFIG = json.load(config_file)


class Constants:
    HOST = CONFIG.get("HOST")
    PORT = CONFIG.get("PORT")
    DATABASE = CONFIG.get("DATABASE")
    DATABASE_HOST = CONFIG.get("DATABASE_HOST")
    USER_NAME = CONFIG.get("USER_NAME")
    PASSWORD = CONFIG.get("PASSWORD")
    SERVER_ADDRESS = CONFIG.get("SERVER_ADDRESS")
    AUTH_URL = CONFIG.get("AUTH_URL")
    ACCOUNT_URL = CONFIG.get("ACCOUNT_URL")
    ADD_ON_TYPE = CONFIG.get("ADD_ON_TYPE")
    PROTOCOL = CONFIG.get("PROTOCOL")
    GET_ADD_ONS_URL = CONFIG.get("GET_ADD_ONS_URL")
    TOOKAN_SOURCE_ID = CONFIG.get("TOOKAN_SOURCE_ID")
