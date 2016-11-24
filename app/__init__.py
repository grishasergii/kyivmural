from flask import Flask, request, g, abort, render_template, redirect, url_for
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
    app.register_blueprint(auth_blueprint)

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    with app.app_context():
        db.create_all()

    if not os.path.exists(app.config['MURAL_IMG_FOLDER']):
        os.makedirs(app.config['MURAL_IMG_FOLDER'])

    @app.route('/')
    def index():
        return redirect(url_for('main.index', lang_code=g.get('current_lang', 'uk')))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

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