from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Globally accessible library
db = SQLAlchemy()


def create_app():
	"""Initialize the core application."""
	flask_app = Flask(__name__, instance_relative_config=False)
	flask_app.config.from_object('config.Config')

	# Initialize Plugins
	db.init_app(flask_app)

	with flask_app.app_context():
		migrate = Migrate(flask_app, db)

		db.create_all()
		return flask_app
