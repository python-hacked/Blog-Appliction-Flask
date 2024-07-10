import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://posygres:12345@db/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
