from datetime import datetime
from enums import States, Genres
from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import NumberRange, DataRequired, URL

class ShowForm(Form):
    artist_id = IntegerField(
        'artist_id',
        validators=[DataRequired(), NumberRange(min=1)]
    )
    venue_id = IntegerField(
        'venue_id',
        validators=[DataRequired(), NumberRange(min=1)],
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=States.choices(),
        coerce=str
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[DataRequired()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genres.choices(),
        coerce=str
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField(
        'seeking_description'
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=States.choices(),
        coerce=str
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[DataRequired()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genres.choices(),
        coerce=str
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField(
            'seeking_description'
    )
