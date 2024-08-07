import os
from urllib.parse import quote


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URI') or
        "mysql+pymysql://root:%s@localhost/thuetro?charset=utf8mb4"
        % quote('0308110299Go'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True
