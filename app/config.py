import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "71a3fc447e89f4eb4abf1edb7124387f223d529969e6f43b243d92219e38584bbe95b6c2f6d8b8c17adda013be09160c"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False       # Enables auto committing
    SQLALCHEMY_TRACK_MODIFICATIONS = False      # For before requests
    FLASKY_MAIL_SUBJECT_PREFIX = ''
    FLASKY_MAIL_SENDER = 'Waasle Team <mail-noreply@waasle.com>'
    FLASKY_ADMIN = "Devesh Aggrawal"
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "mail-noreply@waasle.com"
    MAIL_PASSWORD = "noreplywaasle"
    RECAPTCHA_PUBLIC_KEY = "6LeMdw8UAAAAAOJZcdahKaUtJS50O1UB-LrwfKXO"
    RECAPTCHA_PRIVATE_KEY = "6LeMdw8UAAAAAF2fRlBLcNSSxv-sLaxCg6WVnzZt"

    @staticmethod
    def init_app(app): 
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mysql@127.0.0.1:3306/waasle"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:waaslemysqlroot@127.0.0.1:3306/waasle"


config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}
