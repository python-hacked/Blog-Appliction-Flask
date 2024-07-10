import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Replace 'db' with 'localhost'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/blogs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key_here'
    GOOGLE_MAPS_API_KEY = 'your_google_maps_api_key_here'

