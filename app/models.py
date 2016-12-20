from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
import os
from config import Config
from flask import Markup
from urlparse import urlparse
from flask_babel import gettext


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

mural_artist = db.Table('mural_artist',
                        db.Column('mural_id', db.Integer, db.ForeignKey('murals.id')),
                        db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')),
                        db.PrimaryKeyConstraint('mural_id', 'artist_id')
                        )


class Mural(db.Model):
    __tablename__ = 'murals'
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    photos = db.relationship('MuralPhoto', backref='mural', cascade="all, delete-orphan")
    artists = db.relationship('Artist', secondary=mural_artist, backref='murals')
    translations = db.relationship('MuralTranslation', backref='mural', cascade="all, delete-orphan")

    def __repr__(self):
        return '<Mural id: {}>'.format(self.id)

    def get_translation(self, lang_code):
        for t in self.translations:
            if t.language_code == lang_code:
                return t
        return None

    def get_address(self, lang_code='uk'):
        for t in self.translations:
            if t.language_code == lang_code:
                return t.address
        return 'n/a'

    def get_name(self, lang_code):
        for t in self.translations:
            if t.language_code == lang_code:
                return t.name
        return 'n/a'

    def get_description(self, lang_code):
        for t in self.translations:
            if t.language_code == lang_code:
                return t.description
        return 'n/a'

    @property
    def artist_names(self):
        r = []
        for artist in self.artists:
            r.append(artist.name)
        if r:
            return ', '.join(r)
        return ''

    @property
    def artist_id(self):
        if self.artists:
            return self.artists[0].id
        else:
            return -1

    @property
    def first_photo_name(self):
        if len(self.photos) > 0:
            return self.photos[0].file_name
        return '#'


class MuralPhoto(db.Model):
    __tablename__ = 'mural_photos'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100))
    copyright_name = db.Column(db.String(50))
    copyright_url = db.Column(db.String(100))
    mural_id = db.Column(db.Integer, db.ForeignKey('murals.id'), nullable=False)

    def __repr__(self):
        return '<Mural Photo %r, mural id %d>' % (self.file_name, self.mural_id)

    @property
    def full_filename(self):
        return os.path.join(Config.MURAL_IMG_FOLDER, self.file_name)

    @property
    def has_copyright(self):
        if self.copyright_url or self.copyright_name:
            return True
        else:
            return False

    @property
    def copyright_string(self):
        result = ''
        if self.copyright_name:
            result = gettext('photo') + ': ' + self.copyright_name
        if self.copyright_url:
            parsed_url = urlparse(self.copyright_url)
            result += gettext('photo') + ': <a href="{}">{}</a>'.format(self.copyright_url, parsed_url.netloc)
        return Markup(result)


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    nickname = db.Column(db.String(50))
    url = db.Column(db.String(100))

    translations = db.relationship('ArtistTranslation', backref='artist', cascade="all, delete-orphan")

    def __repr__(self):
        return '<Artist %r aka %r id %d>' % (self.name, self.nickname, self.id)

    def get_translation(self, lang_code):
        for t in self.translations:
            if t.language_code == lang_code:
                return t

        translation = ArtistTranslation()
        translation.artist_id = self.id
        translation.language_code = lang_code
        db.session.add(translation)
        return translation

    def get_about(self, lang_code):
        for t in self.translations:
            if t.language_code == lang_code:
                return t.about
        return ''

    def set_about(self, value, lang_code):
        translation = self.get_translation(lang_code)
        translation.about = value

    @property
    def full_name(self):
        if self.name and self.nickname:
            if self.name == self.nickname:
                return self.name
            else:
                return self.name + ' aka ' + self.nickname
        elif self.name:
            return self.name
        elif self.nickname:
            return self.nickname
        else:
            return 'The girl has no name'

    @property
    def short_name(self):
        if self.nickname:
            return self.nickname
        if self.name:
            return self.name
        return 'Noname'


class Language(db.Model):
    __tablename__ = 'languages'
    code = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return '<Language %r %r>' % (self.code, self.name)

    @staticmethod
    def insert_languages():
        languages = [
            ('English', 'en'),
            ('Ukrainian', 'uk')
        ]
        for l in languages:
            lang = Language.query.get(l[1])
            if lang is None:
                lang = Language()
                lang.name = l[0]
                lang.code = l[1]
                db.session.add(lang)
                db.session.commit()


class MuralTranslation(db.Model):
    __tablename__ = 'mural_translations'
    id = db.Column(db.Integer, primary_key=True)
    mural_id = db.Column(db.Integer, db.ForeignKey('murals.id'), nullable=False)
    language_code = db.Column(db.String(2), db.ForeignKey('languages.code'), nullable=False)
    description = db.Column(db.Text)
    name = db.Column(db.String(50))
    address = db.Column(db.String(100))

    def __repr__(self):
        return '<Mural translation>'


class ArtistTranslation(db.Model):
    __tablename__ = 'artist_translations'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    language_code = db.Column(db.String(2), db.ForeignKey('languages.code'), nullable=False)
    about = db.Column(db.Text)

    def __repr__(self):
        return '<Artist translation>'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def insert_admin():
        username = os.environ.get('KYIVMURAL_ADMIN_USERNAME')
        password = os.environ.get('KYIVMURAL_ADMIN_PASSWORD')

        u = User.query.filter_by(username=username).first()
        if u is None:
            u = User()
            u.username = username
            u.password = password
            db.session.add(u)
            db.session.commit()





