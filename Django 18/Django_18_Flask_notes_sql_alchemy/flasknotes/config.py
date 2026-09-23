import os

from dotenv import load_dotenv

class Config:
    load_dotenv()

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEMO_USER = os.environ.get('DEMO_USER')
    DEMO_PASSWORD = os.environ.get('DEMO_PASSWORD')