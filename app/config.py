import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False       # Enables auto committing
    SQLALCHEMY_TRACK_MODIFICATIONS = False      # For before requests
    FLASKY_MAIL_SUBJECT_PREFIX = ''
    FLASKY_MAIL_SENDER = 'Waasle Team <mail-noreply@waasle.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

    @staticmethod
    def init_app(app): 
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.zoho.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mail-noreply@waasle.com'        #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'noreplywaasle'                        #os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              "mysql+pymysql://root:mysql@127.0.0.1:3306/waasle"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              "mysql+pymysql://root:mysql@127.0.0.1:3306/buy"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              "mysql+pymysql://root:mysql@127.0.0.1:3306/buy"


config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}
