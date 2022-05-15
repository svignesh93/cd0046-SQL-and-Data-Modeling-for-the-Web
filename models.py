#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from app import db
from datetime import datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False, default=[])
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship("Show", backref="venue_shows_list", lazy=True, cascade="all, delete-orphan")

    # Equivalent of toString()
    def __repr__(self) -> str:
      return f"""<
        id: {self.id}, 
        name: {self.name}, 
        city: {self.city}, 
        state: {self.state}, 
        address: {self.address}, 
        phone: {self.phone}, 
        genres: {self.genres}, 
        image_link: {self.image_link}, 
        facebook_link: {self.facebook_link}, 
        website_link: {self.website_link}, 
        seeking_talent: {self.seeking_talent}, 
        seeking_description: {self.seeking_description}, 
        shows: {self.shows}
      >"""

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False, default=[])
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship("Show", backref="artist_shows_list", lazy=True, cascade="all, delete-orphan")

    # Equivalent of toString()
    def __repr__(self) -> str:
      return f"""<
        id: {self.id}, 
        name: {self.name}, 
        city: {self.city}, 
        state: {self.state}, 
        phone: {self.phone}, 
        genres: {self.genres}, 
        image_link: {self.image_link}, 
        facebook_link: {self.facebook_link}, 
        website_link: {self.website_link}, 
        seeking_venue: {self.seeking_venue}, 
        seeking_description: {self.seeking_description}, 
        shows: {self.shows}
      >"""

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False, default=datetime.today())

  # Equivalent of toString()
  def __repr__(self) -> str:
    return f"""<
      id: {self.id}, 
        venue_id: {self.venue_id}, 
        artist_id: {self.artist_id}, 
        start_time: {self.start_time}
      >"""
