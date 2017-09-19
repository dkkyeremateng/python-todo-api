from flask import Flask

from keep.extensions import db

from keep.api.todo.views import todo
from keep.api.user.views import user


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    extentions(app)

    app.register_blueprint(todo)
    app.register_blueprint(user)

    return app


def extentions(app):
    """
    Initialize the Flask-Login extension (mutates the app passed in).

    :param app: Flask application instance
    :param user_model: Model that contains the authentication information
    :type user_model: SQLAlchemy model
    :return: None
    """

    db.init_app(app)

    return None
