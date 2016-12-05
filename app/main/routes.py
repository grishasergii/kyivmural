from flask import render_template, abort, redirect, url_for, g, request
from . import main
from ..models import Mural, Artist
from .. import config
import random


@main.route('/index')
def index():
    murals = Mural.query.all()
    mural_count = len(murals)
    artist_count = Artist.query.count()
    random_murals = random.sample(murals, min(len(murals), 4))
    return render_template('index.html',
                           title='Kyivmural',
                           murals=murals,
                           random_murals=random_murals,
                           mural_count=mural_count,
                           artist_count=artist_count)


@main.route('/mural/<int:mural_id>')
def mural(mural_id):
    mural = Mural.query.get(mural_id)
    if mural:
        return render_template('main/mural/detail_view.html',
                               mural=mural)
    else:
        abort(404)


@main.route('/murals')
@main.route('/murals/<int:page>')
def murals(page=1):
    if not isinstance(page, (int, long)):
        page = 1

    pagination = Mural.query.paginate(page, per_page=9, error_out=False)
    murals = pagination.items
    return render_template('main/mural/all.html',
                           murals=murals,
                           pagination=pagination)


@main.route('/artist/<int:id>')
def artist(id):
    artist = Artist.query.get(id)
    if mural:
        return render_template('main/artist/detail_view.html',
                               artist=artist)
    else:
        abort(404)


@main.route('/artists')
def artists():
    artists = Artist.query.all()
    return render_template('main/artist/all.html',
                           artists=artists)


@main.route('/about')
def about():
    return render_template('main/about/about.html')
