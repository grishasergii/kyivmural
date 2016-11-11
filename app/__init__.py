from flask import Flask, request, g, abort
from flask import url_for as flask_url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_bootstrap import Bootstrap
from flask_babel import Babel
import os


# push application context when working from termial
# http://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w
# create_app().app_context().push()

bootstrap = Bootstrap()
babel = Babel()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


@babel.localeselector
def get_locale():
    return g.get('current_lang', 'uk')


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    # set up Babel
    babel.init_app(app)
    app.jinja_env.globals.update(get_locale=get_locale)

    db.init_app(app)

    login_manager.init_app(app)

    # attach routes and custom error pages here
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/<lang_code>/auth')

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/<lang_code>/admin')

    with app.app_context():
        db.create_all()

    if not os.path.exists(app.config['MURAL_IMG_FOLDER']):
        os.makedirs(app.config['MURAL_IMG_FOLDER'])

    @app.before_request
    def before():
        if request.view_args and 'lang_code' in request.view_args:
            if request.view_args['lang_code'] not in app.config['LANGUAGES']:
                abort(404)
            g.current_lang = request.view_args['lang_code']
            request.view_args.pop('lang_code')

    @app.context_processor
    def inject_url_for():
        return {
            'url_for': lambda endpoint, **kwargs: flask_url_for(
                endpoint, lang_code=g.get('current_lang', 'uk'), **kwargs
            )
        }

    url_for = inject_url_for()['url_for']

    return app

"""
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app import models
from app.main import views
"""