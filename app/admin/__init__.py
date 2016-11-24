from flask import Blueprint, g


admin = Blueprint('admin', __name__, url_prefix='/<lang_code>/admin')


@admin.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.get('current_lang', 'uk'))


@admin.url_value_preprocessor
def pull_lang_code(endpoint, values):
    lang_code = values.pop('lang_code')
    if lang_code not in ['en', 'uk']:
        lang_code = 'uk'
    g.current_lang = lang_code

from . import routes
