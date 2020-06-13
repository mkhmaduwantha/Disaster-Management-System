from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from emas.config import Config
from flask_admin import Admin
from flask_cors import CORS
from sqlalchemy import create_engine
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


admin = Admin()


def create_app(config_class=Config):
    app = Flask(__name__)
    cors = CORS(app, supports_credentials=True)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        # db.create_all()

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    admin.init_app(app)

    from emas.users.routes import users
    # from emas.main.routes import main
    from emas.home.routes import home
    from emas.errors.handlers import errors
    from emas.map.routes import my_map

    app.register_blueprint(users)
    # app.register_blueprint(main)
    app.register_blueprint(home)
    app.register_blueprint(errors)
    app.register_blueprint(my_map)
    db.create_all(app=app)


    return app
