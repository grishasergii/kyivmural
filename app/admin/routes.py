from flask import render_template, redirect, url_for, request, g
from . import admin
from flask_login import login_required
from ..models import Mural, Language, Artist, ArtistTranslation, MuralPhoto, MuralTranslation
from .forms import artist_form, mural_form, MuralPhotoForm, ImportCsvForm
from .. import db
from utils import save_mural_from_form
from import_from_csv import import_from_csv

# Murals

@admin.route('/mural')
@login_required
def murals():
    _murals = Mural.query.all()
    return render_template('admin/mural/all.html',
                           murals=_murals)


@admin.route('/mural/delete/<int:id>', methods=['POST'])
@login_required
def mural_delete(id):
    mural = Mural.query.get(id)
    if mural is not None:
        db.session.delete(mural)
        db.session.commit()
    return redirect(url_for('admin.murals'))


@admin.route('/mural/update/<int:id>', methods=['POST'])
@login_required
def mural_update(id):
    mural = Mural.query.get(id)
    artists = Artist.query.all()
    languages = Language.query.all()
    form = mural_form(languages, artists)

    if 'save_mural_button' in request.form:
        if form.validate_on_submit():
            save_mural_from_form(mural, form, languages)
            return redirect(url_for('admin.murals'))

    form.lat.data = mural.lat
    form.lng.data = mural.lng
    form.artist.data = mural.artist_id

    for lang in languages:
        field = getattr(form, 'address_{}'.format(lang.code), None)
        if field:
            field.data = mural.get_address(lang.code)

        field = getattr(form, 'description_{}'.format(lang.code), None)
        if field:
            field.data = mural.get_description(lang.code)

        field = getattr(form, 'name_{}'.format(lang.code), None)
        if field:
            field.data = mural.get_name(lang.code)

    return render_template('admin/mural/form.html',
                           title='Edit Mural',
                           form=form,
                           languages=languages,
                           photos=mural.photos)

    db.session.commit()
    return redirect(url_for('admin.artists'))


@admin.route('/mural/new', methods=['GET', 'POST'])
@login_required
def mural_create():
    languages = Language.query.all()
    artists = Artist.query.all()
    form = mural_form(languages, artists)
    if form.validate_on_submit():
        # mural
        mural = Mural()
        save_mural_from_form(mural, form, languages)
        return redirect(url_for('admin.murals'))

    return render_template('admin/mural/form.html',
                           title='Create Mural',
                           form=form,
                           languages=languages,
                           photos=[])


# Mural photo
@admin.route('/mural_photo/delete/<int:id>', methods=['POST'])
@login_required
def mural_photo_delete(id):
    mural_photo = MuralPhoto.query.get(id)
    if mural_photo is not None:
        db.session.delete(mural_photo)
        db.session.commit()

    return redirect(url_for('admin.murals'))


@admin.route('/mural_photo/update/<int:id>', methods=['POST'])
@login_required
def mural_photo_update(id):
    photo = MuralPhoto.query.get(id)
    form = MuralPhotoForm()

    if 'save_mural_photo_button' in request.form:
        if form.validate_on_submit():
            photo.copyright_name = form.copyright_name.data
            photo.copyright_url = form.copyright_url.data
            db.session.add(photo)
            db.session.commit()
            return redirect(url_for('admin.mural_update', id=photo.mural_id), code=307)

    form.copyright_url.data = photo.copyright_url
    form.copyright_name.data = photo.copyright_name
    form.filename.data = photo.file_name

    return render_template('admin/mural_photo/form.html',
                           title='Edit Mural Photo',
                           form=form,
                           photo=photo)


# Artists

@admin.route('/artist')
@login_required
def artists():
    _artists = Artist.query.all()
    languages = Language.query.all()
    return render_template('admin/artist/all.html',
                           artists=_artists,
                           languages=languages)


@admin.route('/artist/delete/<int:id>', methods=['POST'])
@login_required
def artist_delete(id):
    artist = Artist.query.get(id)
    if artist is not None:
        db.session.delete(artist)
        db.session.commit()
    return redirect(url_for('admin.artists'))


@admin.route('/artist/update/<int:id>', methods=['POST'])
@login_required
def artist_update(id):
    artist = Artist.query.get(id)

    languages = Language.query.all()
    form = artist_form(languages)

    if 'save_artist_button' in request.form:
        if form.validate_on_submit():
            artist.name = form.name.data
            artist.nickname = form.nickname.data
            artist.url = form.url.data
            for lang in languages:
                field = getattr(form, 'about_{}'.format(lang.code), None)
                if field:
                    artist.set_about(field.data, lang.code)
            db.session.commit()
            return redirect(url_for('admin.artists'))

    form.name.data = artist.name
    form.nickname.data = artist.nickname
    form.url.data = artist.url
    for lang in languages:
        field = getattr(form, 'about_{}'.format(lang.code), None)
        if field:
            field.data = artist.get_about(lang.code)
    return render_template('admin/artist/form.html',
                           title='Edit Artist',
                           form=form,
                           languages=languages)

    db.session.commit()
    return redirect(url_for('admin.artists'))


@admin.route('/artist/new', methods=['GET', 'POST'])
@login_required
def artist_create():
    languages = Language.query.all()
    form = artist_form(languages)
    if form.validate_on_submit():
        artist = Artist()
        artist.name = form.name.data
        artist.nickname = form.nickname.data
        artist.url = form.url.data
        db.session.add(artist)
        db.session.commit()
        for lang in languages:
            artist_translation = ArtistTranslation()
            artist_translation.language_code = lang.code
            artist_translation.artist_id = artist.id
            artist_translation.about = ''
            field = getattr(form, 'about_{}'.format(lang.code), None)
            if field:
                artist_translation.about = field.data
            db.session.add(artist_translation)
        db.session.commit()
        return redirect(url_for('admin.artists'))

    return render_template('admin/artist/form.html',
                           title='Create Artist',
                           form=form,
                           languages=languages)


@admin.route('/import', methods=['GET', 'POST'])
@login_required
def import_csv():
    form = ImportCsvForm()
    if form.validate_on_submit():
        csv_file = request.files['csv_file']
        import_from_csv(csv_file)
        return redirect(url_for('admin.murals'))

    return render_template('admin/import_csv/form.html',
                           title='Import Recirds from csv',
                           form=form)