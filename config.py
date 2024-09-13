import os
from urllib.parse import quote


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URI') or
        "mysql+pymysql://root:%s@localhost/thuetro?charset=utf8mb4"
        % quote('123456789'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or ''
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or ''
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or ''
