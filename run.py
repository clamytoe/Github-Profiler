#!/usr/bin/env python3
import os

# local imports
from app import create_app

config_name = os.environ.get('FLASK_CONFIG', 'development')

app =  create_app(config_name)

if __name__ == "__main__":
    app.run()

