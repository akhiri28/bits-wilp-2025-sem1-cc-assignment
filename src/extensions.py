# Set up Flask extensions here

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()  # create the database object for use in the app

from flask_login import LoginManager
login_manager = LoginManager()

from flask_migrate import Migrate
migrate = Migrate()
