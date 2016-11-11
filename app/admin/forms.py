from flask.ext.wtf import Form
from wtforms import StringField, FloatField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, URL, Optional, NumberRange, Length


class MuralPhotoForm(Form):
    filename = StringField()
    copyright_name = StringField()
    copyright_url = StringField(validators=[Optional(), URL()])


class ImportCsvForm(Form):
    csv_file = FileField(validators=[DataRequired()])


def artist_form(languages):
    """
    Dynamically creates artist form.
    http://stackoverflow.com/questions/31160781/wtforms-generate-fields-in-constructor
    :param languages: list of Language objects, available languages
    :return: instance of ArtistForm
    """
    class ArtistForm(Form):
        name = StringField('name')
        nickname = StringField('nickname', validators=[DataRequired()])
        url = StringField('url', validators=[Optional(), URL()])

    for lang in languages:
        label = 'about_{}'.format(lang.code)
        field = TextAreaField(label)
        setattr(ArtistForm, label, field)

    return ArtistForm()


def mural_form(languages, artists):
    """
    Dynamically creates a mural form
    :param languages: list of Language objects, available languages
    :param artists: list of Artist objects, available artists
    :return: instance of MuralForm
    """
    class MuralForm(Form):
        # coordinates
        lat = FloatField('Latitude', validators=[DataRequired(), NumberRange(min=-90, max=90)])
        lng = FloatField('Longitude', validators=[DataRequired(), NumberRange(min=-180, max=180)])

        # photos
        photo_rename_to = StringField(validators=[Optional(), Length(min=3)])
        photo_copyright_name = StringField(validators=[Optional(), Length(min=3)])
        photo_copyright_url = StringField(validators=[Optional(), URL()])
        photo_files = FileField()

    # choice of artists
    label = 'artist'
    artist_choices = [(a.id, a.name) for a in artists]
    artist_choices.insert(0, (-1, ''))
    field = SelectField(label, choices=artist_choices, coerce=int)
    setattr(MuralForm, label, field)

    for lang in languages:
        # address
        label = 'address_{}'.format(lang.code)
        field = StringField(label, validators=[DataRequired()])
        setattr(MuralForm, label, field)

        # name
        label = 'name_{}'.format(lang.code)
        field = StringField(label)
        setattr(MuralForm, label, field)

        # description
        label = 'description_{}'.format(lang.code)
        field = TextAreaField(label)
        setattr(MuralForm, label, field)

    return MuralForm()
