import os
import pymysql

class Config(object):
    SECRET_KEY = 'my_secret_key'

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@127.0.0.1/userdata'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
