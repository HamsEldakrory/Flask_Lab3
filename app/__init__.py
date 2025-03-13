import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate
from flask_login import LoginManager
db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()
login_manager.login_view='auth.login'

def create_app(environment):
    app=Flask(__name__)
    app.config.from_object(config.get(environment or 'development'))
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.init_app(app)
    from . import models
    migrate.init_app(app,db)
    register_blueprints(app)
    login_manager.init_app(app)
    return app

def register_blueprints(application):
    from .main.routes import main_blueprint
    from .auth.routes import auth_blueprint
    application.register_blueprint(main_blueprint)
    application.register_blueprint(auth_blueprint)
    