from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import db, User, Blog, Category, Tag, Comment

def create_admin(app: Flask):
    admin = Admin(app, name='My Blog Admin', template_mode='bootstrap3')

    # Add administrative views here
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Blog, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Tag, db.session))
    admin.add_view(ModelView(Comment, db.session))
    
    return admin
