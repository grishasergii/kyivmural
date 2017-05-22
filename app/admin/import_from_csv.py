from werkzeug.utils import secure_filename
from .. import db
from ..models import Mural, Language, Artist, ArtistTranslation, MuralPhoto, MuralTranslation
import os
import csv
from urlparse import urlparse
from bs4 import BeautifulSoup
from utils import get_address_from_coordinates


def import_from_csv(afile):
    filename = secure_filename(afile.filename)
    _, extension = os.path.splitext(filename)
    if extension != '.csv':
        return False
    languages = Language.query.all()
    reader = csv.reader(afile)
    for row in reader:
        parse_row(row, languages)


def get_artist(artist_name):
    artist = None
    if artist_name:
        artist = Artist.query.filter_by(name=artist_name).first()
        if not artist:
            artist = Artist()
            artist.name = artist_name
            artist.nickname = artist_name
            db.session.add(artist)
            db.session.commit()
    return artist


def parse_row(row, languages):
    """
    0 - id
    1 - lat
    2 - lng
    3 - images
    4 - copyright
    5 - about (ignore, it is always empty)
    6 - artist name
    :param row:
    :return:
    """
    print 'parsing mural id {0}'.format(row[0])
    # artist
    artist_name = row[6]
    artist = get_artist(artist_name)

    mural = Mural()
    mural.lat = row[1]
    mural.lng = row[2]
    if artist is not None:
        mural.artists = [artist]

    db.session.add(mural)
    db.session.commit()

    create_photos(row[3].strip(), row[4].strip(), mural.id)

    for lang in languages:
        address = get_address_from_coordinates(mural.lat, mural.lng, lang.code)
        mural_translation = MuralTranslation()
        mural_translation.language_code = lang.code
        mural_translation.address = address
        mural_translation.mural_id = mural.id
        db.session.add(mural_translation)

    db.session.commit()


def create_photos(photos_string, copyright_string, mural_id):
    copyright_name = ''
    copyright_url = ''
    if copyright_string:
        parsed_url = urlparse(copyright_string)
        if bool(parsed_url.scheme):
            copyright_url = copyright_string
        else:
            copyright_name = copyright_string

    soup = BeautifulSoup(photos_string)

    for imgtag in soup.find_all('img'):
        filename = imgtag['src']
        filename = os.path.basename(filename)
        mural_photo = MuralPhoto()
        mural_photo.file_name = filename
        mural_photo.copyright_name = copyright_name
        mural_photo.copyright_url = copyright_url
        mural_photo.mural_id = mural_id
        db.session.add(mural_photo)

    db.session.commit()
