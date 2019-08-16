from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from linkshorten.utils import Convert
from linkshorten.config import Config
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode, b64decode

def convert_to_base62(value):
	result = Convert(value)
	return result.toBase62()

def convert_to_base10(value):
	result = Convert(value)
	return result.toBase10()

def base64decode(value):
	return b64decode(value).decode('utf-8')

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class = Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	from linkshorten.users.routes import users
	from linkshorten.main.routes import main
	from linkshorten.errors.handlers import errors 
	app.register_blueprint(users)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	app.jinja_env.filters['tobase62'] = convert_to_base62
	app.jinja_env.filters['tobase10'] = convert_to_base10
	app.jinja_env.filters['b64decode'] = base64decode
	app.jinja_env.filters['b64encode'] = b64encode
	
	return app