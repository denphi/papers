from flask import Flask, Blueprint
from flask_restful import Api

from api.controllers import auth, files, users
from config import config

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])

    # Start api/v1 Blueprint
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    api.add_resource(auth.AuthLogin, '/auth/login')
    api.add_resource(auth.AuthRegister, '/auth/register')
    api.add_resource(files.CreateList, '/files')
    api.add_resource(files.ViewEditDelete, '/files/<string:file_id>')
    api.add_resource(users.List, '/users')

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    # End api/v1 Blueprint

    return app
