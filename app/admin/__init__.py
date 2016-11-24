from flask import Blueprint, g


admin = Blueprint('admin', __name__, url_prefix='/<lang_code>/admin')


@admin.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.get('current_lang', 'uk'))


@admin.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.current_lang = values.pop('lang_code')

from . import routes
