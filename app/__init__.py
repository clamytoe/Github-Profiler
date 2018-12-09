import webbrowser
from time import localtime, strftime

import requests
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Local imports
from config import app_config

# Variables initialization
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.app = app
    db.init_app(app)

    # import models
    from app.models import  Accounts, Repos, Gists

    # initialize the database
    db.create_all()

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run()
