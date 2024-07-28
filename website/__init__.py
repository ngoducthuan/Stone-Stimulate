import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from math import floor, ceil
import math

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = 'stone.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'callmestone'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = 'website/static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'php'}
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    db.init_app(app)
    migrate.init_app(app, db)

    from .backend.views import views
    from .backend.auth import auth
    from .backend.notes import note
    from .backend.manage import manage
    from .backend.stored_xss import stored_xss
    from .backend.dom_xss import dom_xss

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(note, url_prefix="/")
    app.register_blueprint(manage, url_prefix="/")
    app.register_blueprint(stored_xss, url_prefix="/")
    app.register_blueprint(dom_xss, url_prefix="/")
    from .backend.models import User, Note

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        try:
            return User.query.get((int(id)))
        except ValueError:
            print("Error")  # Handle case where id cannot be converted to integer
    #Declare floor and ceil to filter in page stored_xss website page
    @app.template_filter('floor')
    def floor_filter(value):
        return math.floor(value)

    @app.template_filter('ceil')
    def ceil_filter(value):
        return math.ceil(value)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # db.create_all(app=app1)
        # print("Created Database!")
        with app.app_context():
            db.create_all()
        print("Created Database!")