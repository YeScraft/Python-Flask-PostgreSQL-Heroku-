import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY') or os.environ.get('SECRET_KEY')

