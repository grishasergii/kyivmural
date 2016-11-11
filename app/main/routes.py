from flask import render_template, abort, redirect, url_for, g, request
from . import main
from ..models import Mural
from .. import config
import random


@main.route('/')
def root():
    return redirect(url_for('main.index',
                            lang_code=g.get('current_lang', 'uk')))


@main.route('/<lang_code>/index')
def index():
    murals = Mural.query.all()
    random_murals = random.sample(murals, min(len(murals), 4))
    return render_template('index.html',
                           title='Kyivmural',
                           murals=murals,
                           random_murals=random_murals)


@main.route('/<lang_code>/mural/<int:mural_id>')
def mural(mural_id):
    mural = Mural.query.get(mural_id)
    if mural:
        return render_template('main/mural/detail_view.html',
                               mural=mural)
    else:
        abort(404)
