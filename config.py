class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_NAME = "papers"
    UPLOAD_FOLDER = '../papers_mod/upload/'
    MAX_CONTENT_PATH = 26214400

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "S0m3S3cr3tK3y"

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}
