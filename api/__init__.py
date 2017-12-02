# api/__init__.py
from flask import Flask
api = Flask(__name__)

# register your blueprints here
from api.routes.main import *
api.register_blueprint(simple)