import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    LOG_DIR = os.environ.get('LOG_DIR') or '/'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    WTF_CSRF_ENABLED = True
    DEBUG = False
    MURAL_IMG_FOLDER = os.path.join(basedir, 'app', 'static', 'mural_img')
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPEG', 'png'])
    MURALS_PER_PAGE = 9
    LANGUAGES = {
        'en': 'English',
        'uk': 'Ukraininan'
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app_dev.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app_prod.db')


class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig,
    'heroku': HerokuConfig
}