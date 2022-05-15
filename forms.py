from enum import Enum
from datetime import datetime
from flask_wtf import Form
from wtforms import IntegerField, StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import NumberRange, DataRequired, URL

class States(Enum):
    AL = 'AL'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'

    def __str__(self):
        return str(self.value)

class Genres(Enum):
    Alternative = 'Alternative'
    Blues =  'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    HeavyMetal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    MusicalTheatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RAndB = 'R&B'
    Reggae = 'Reggae'
    RockNRoll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'

    def __str__(self):
        return str(self.value)

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
        choices=States.__members__.values,
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
        choices=Genres.__members__.values,
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
        choices=States.__members__.values,
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
        choices=Genres.__members__.values,
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
