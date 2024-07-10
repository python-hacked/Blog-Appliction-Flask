from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from app.admin import create_admin

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import tags_bp, comments_bp, user_bp, api_bp
    app.register_blueprint(tags_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)
    create_admin(app)
    
    return app

app = create_app()
