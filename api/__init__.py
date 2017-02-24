from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS, cross_origin

from api.controllers import auth, files, users
from config import config

from kombu import Queue
from celery import subtask
from celery import Celery, chain
from celery.utils.log import get_task_logger

from workers.find_regions.find_regions import find_regions
from workers.debug_regions.debug_regions import debug_regions
from workers.mcs_ocr.mcs_ocr import mcs_ocr
from workers.validate_address.validate_address import validate_address

logger = get_task_logger(__name__)

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])
    CORS(app)

    # Start api/v1 Blueprint
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    api.add_resource(auth.AuthLogin, '/auth/login')
    api.add_resource(auth.AuthRegister, '/auth/register')
    api.add_resource(files.CreateList, '/files')
    api.add_resource(files.Upload, '/upload')
    api.add_resource(files.Download, '/download/<string:file_id>')
    api.add_resource(files.ViewEditDelete, '/files/<string:file_id>')
    api.add_resource(users.List, '/users')

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    # End api/v1 Blueprint

    # Celery
    celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')
    celery_app.conf.task_default_queue = 'default'
    celery_app.conf.task_queues = (
        Queue('find_regions',    routing_key='find_regions'),
        Queue('debug_regions', routing_key='debug_regions'),
        Queue('mcs_ocr',    routing_key='mcs_ocr'),
        Queue('validate_address', routing_key='validate_address')
    )
    task_default_exchange = 'tasks'
    task_default_exchange_type = 'topic'
    task_default_routing_key = 'task.default'

    return app
