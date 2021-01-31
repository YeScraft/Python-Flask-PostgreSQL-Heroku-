from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bs = Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = 'authorization'
login_manager.login_message = 'Please get authorization..'
login_manager.login_message_category = "warning"


from app import routes, models, forms

migrate = Migrate(app, db)
