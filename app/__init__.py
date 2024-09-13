from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import cloudinary

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = 'a_very_secret_key'
csrf = CSRFProtect(app)

# Initialize Flask-Admin with Bootswatch theme (pull from github new version)


cloudinary.config(cloud_name=app.config.get("CLOUDINARY_CLOUD_NAME"),
                  api_key=app.config.get("CLOUDINARY_API_KEY"),
                  api_secret=app.config.get("CLOUDINARY_API_SECRET"))

from app import routes, models, admin_config, errors