
class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_NAME = "papers"
    UPLOAD_FOLDER = 'upload/'
    MAX_CONTENT_PATH = 26214400

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    MSCS_VISION_API_KEY = '<YOUR_MSCS_VISION_API_KEY>' # For Celery worker 'mcs_ocr'

    GOOGLE_API_KEY = '<YOUR_GOOGLE_API_KEY>' # For Celery worker 'validate_address'


class DevelopmentConfig(Config):
    DEBUG = True

    SECRET_KEY = "S0m3S3cr3tK3y"

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}
