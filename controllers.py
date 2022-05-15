#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import babel
import dateutil.parser
from app import app, db
from forms import *
from datetime import datetime
from xmlrpc.client import boolean
from models import Venue, Artist, Show
from flask import Blueprint, render_template, request, abort, flash, redirect, url_for

#----------------------------------------------------------------------------#
# Controller Config.
#----------------------------------------------------------------------------#

controller = Blueprint('controller', __name__)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, datetime):
    date = value
  else:
    date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  venueLocList = Venue.query.distinct(Venue.state, Venue.city).all()
  for venueLocation in venueLocList:
    city = venueLocation.city
    state = venueLocation.state

    venues = []
    current_time = datetime.now()
    venueList = Venue.query.filter_by(city = city, state = state).all()

    for venue in venueList:
      upcomingShows = list(filter(lambda show: show.start_time > current_time, venue.shows))

      venues.append({
        "id" : venue.id,
        "name" : venue.name,
        "num_upcoming_shows" : upcomingShows.count
      })

    data.append({
      "city" : city,
      "state" : state,
      "venues" : venues
    })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  searchTerm = request.form.get('search_term', '')

  venues = Venue.query.filter(Venue.name.ilike("%" + searchTerm + "%")).all()
  
  data = []
  current_time = datetime.now()

  for venue in venues:
    upcomingShows = list(filter(lambda show: show.start_time > current_time, venue.shows))
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": upcomingShows.count,
    })

  result={
    "count": len(venues),
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=result, search_term=searchTerm)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  error = False
  data = {}

  try:
    venue = Venue.query.filter_by(id = venue_id).first()

    data["id"] = venue.id
    data["name"] = venue.name
    data["city"] = venue.city
    data["state"] = venue.state
    data["address"] = venue.address
    data["phone"] = venue.phone
    data["genres"] = venue.genres
    data["image_link"] = venue.image_link
    data["facebook_link"] = venue.facebook_link
    data["website"] = venue.website_link
    data["seeking_talent"] = venue.seeking_talent
    data["seeking_description"] = venue.seeking_description

    past_shows = []
    upcoming_shows = []
    current_time = datetime.now()

    artistShows = db.session.query(
      Show.artist_id, 
      Artist.name, 
      Artist.image_link, 
      Show.start_time
    ).filter_by(
      venue_id = venue.id
    ).join(Artist).all()

    for artistShow in artistShows:
      artistId, artistName, artistImgLink, showtime  = artistShow
      artistShowRecord = {
        "artist_id" : artistId,
        "artist_name": artistName,
        "artist_image_link": artistImgLink,
        "start_time": showtime
      }
      if (showtime > current_time):
        upcoming_shows.append(artistShowRecord)
      else: 
        past_shows.append(artistShowRecord)

    data["past_shows"] = past_shows
    data["upcoming_shows"] = upcoming_shows

    data["past_shows_count"] = len(past_shows)
    data["upcoming_shows_count"] = len(upcoming_shows)
  except:
    error = True
    print(sys.exc_info())
  if error:
    # e.g., on unsuccessful db query, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue id ' + str(venue_id) + ' not found.')
    abort(404)
  else:
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    venue = Venue(
      name = request.form["name"],
      city = request.form["city"],
      state = request.form["state"],
      address = request.form["address"],
      phone = request.form["phone"],
      genres = request.form.getlist("genres", type=str),
      image_link = request.form["image_link"],
      facebook_link = request.form["facebook_link"],
      website_link = request.form["website_link"],
      seeking_talent = request.form.get("seeking_talent", default=False, type=boolean),
      seeking_description = request.form["seeking_description"],
    )
    db.session.add(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # e.g., on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    abort(500)
  else:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  error = False
  try:
    venue = Venue.query.get(venue_id)

    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # e.g., on unsuccessful db delete, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + str(venue_id) + ' not found.')
    abort(404)
  else:
    # on successful db delete, flash success
    flash('Venue ' + str(venue_id)  + ' was successfully deleted!')
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.order_by("id").all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  searchTerm = request.form.get('search_term', '')

  artists = Artist.query.filter(Artist.name.ilike("%" + searchTerm + "%")).all()
  
  data = []
  current_time = datetime.now()

  for artist in artists:
    upcomingShows = list(filter(lambda show: show.start_time > current_time, artist.shows))
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": upcomingShows.count,
    })

  result={
    "count": len(artists),
    "data": data
  }

  return render_template('pages/search_artists.html', results=result, search_term=searchTerm)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  error = False
  data = {}

  try:
    artist = Artist.query.filter_by(id = artist_id).first()

    data["id"] = artist.id
    data["name"] = artist.name
    data["city"] = artist.city
    data["state"] = artist.state
    data["phone"] = artist.phone
    data["genres"] = artist.genres
    data["image_link"] = artist.image_link
    data["facebook_link"] = artist.facebook_link
    data["website"] = artist.website_link
    data["seeking_venue"] = artist.seeking_venue
    data["seeking_description"] = artist.seeking_description

    past_shows = []
    upcoming_shows = []
    current_time = datetime.now()

    venueShows = db.session.query(
      Show.venue_id, 
      Venue.name, 
      Venue.image_link, 
      Show.start_time
    ).filter_by(
      artist_id = artist.id
    ).join(Venue).all()

    for venueShow in venueShows:
      venueId, venueName, venueImgLink, showtime  = venueShow
      venueShowRecord = {
        "venue_id" : venueId,
        "venue_name": venueName,
        "venue_image_link": venueImgLink,
        "start_time": showtime
      }
      if (showtime > current_time):
        upcoming_shows.append(venueShowRecord)
      else: 
        past_shows.append(venueShowRecord)

    data["past_shows"] = past_shows
    data["upcoming_shows"] = upcoming_shows

    data["past_shows_count"] = len(past_shows)
    data["upcoming_shows_count"] = len(upcoming_shows)
  except:
    error = True
    print(sys.exc_info())
  if error:
    # e.g., on unsuccessful db query, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Artist id ' + str(artist_id) + ' not found.')
    abort(404)
  else:
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  data = {}
  error = False
  try:
    artist = Artist.query.get(artist_id)
    form.process(obj = artist)

    data["id"] = artist.id
    data["name"] = artist.name
    data["city"] = artist.city
    data["state"] = artist.state
    data["phone"] = artist.phone
    data["genres"] = artist.genres
    data["image_link"] = artist.image_link
    data["facebook_link"] = artist.facebook_link
    data["website"] = artist.website_link
    data["seeking_venue"] = artist.seeking_venue
    data["seeking_description"] = artist.seeking_description
  except:
    error = True
    print(sys.exc_info())
  if error:
    # e.g., on unsuccessful db query, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Artist ' + str(artist_id) + ' not found.')
    abort(404)
  else:
    return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  try:
    artist = Artist.query.get(artist_id)

    artist.name = request.form["name"]
    artist.city = request.form["city"]
    artist.state = request.form["state"]
    artist.phone = request.form["phone"]
    artist.genres = request.form.getlist("genres")
    artist.image_link = request.form["image_link"]
    artist.facebook_link = request.form["facebook_link"]
    artist.website_link = request.form["website_link"]
    artist.seeking_venue = request.form.get("seeking_venue", default=False, type=boolean)
    artist.seeking_description = request.form["seeking_description"]

    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # e.g., on unsuccessful db update, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Artist ' + str(artist_id) + ' not found.')
    abort(404)
  else:
    # on successful db update, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  data = {}
  error = False
  try:
    venue = Venue.query.get(venue_id)
    form.process(obj = venue)

    data["id"] = venue.id
    data["name"] = venue.name
    data["city"] = venue.city
    data["state"] = venue.state
    data["address"] = venue.address
    data["phone"] = venue.phone
    data["genres"] = venue.genres
    data["image_link"] = venue.image_link
    data["facebook_link"] = venue.facebook_link
    data["website"] = venue.website_link
    data["seeking_talent"] = venue.seeking_talent
    data["seeking_description"] = venue.seeking_description
  except:
    error = True
    print(sys.exc_info())
  if error:
    # e.g., on unsuccessful db query, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + str(venue_id) + ' not found.')
    abort(404)
  else:
    return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
    venue = Venue.query.get(venue_id)

    venue.name = request.form["name"]
    venue.city = request.form["city"]
    venue.state = request.form["state"]
    venue.address = request.form["address"]
    venue.phone = request.form["phone"]
    venue.genres = request.form.getlist("genres", type=str)
    venue.image_link = request.form["image_link"]
    venue.facebook_link = request.form["facebook_link"]
    venue.website_link = request.form["website_link"]
    venue.seeking_talent = request.form.get("seeking_talent", default=False, type=boolean)
    venue.seeking_description = request.form["seeking_description"]

    db.session.add(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # e.g., on unsuccessful db update, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + str(venue_id) + ' not found.')
    abort(404)
  else:
    # on successful db update, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
    artist = Artist(
      name = request.form["name"],
      city = request.form["city"],
      state = request.form["state"],
      phone = request.form["phone"],
      genres = request.form.getlist("genres"),
      image_link = request.form["image_link"],
      facebook_link = request.form["facebook_link"],
      website_link = request.form["website_link"],
      seeking_venue = request.form.get("seeking_venue", default=False, type=boolean),
      seeking_description = request.form["seeking_description"],
    )
    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # e.g., on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    abort(500)
  else:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []

  shows = db.session.query(
    Show.venue_id,
    Show.artist_id,
    Show.start_time,
    Venue.name,
    Artist.name,
    Artist.image_link
  ).join(Venue, Artist).all()

  for show in shows:
    venue_id, artist_id, start_time, venue_name, artist_name, artist_image_link = show
    data.append({
      "venue_id": venue_id,
      "venue_name": venue_name,
      "artist_id": artist_id,
      "artist_name": artist_name,
      "artist_image_link": artist_image_link,
      "start_time": start_time
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
    show = Show(
      venue_id = request.form.get("venue_id", type=int),
      artist_id = request.form.get("artist_id", type=int),
      start_time = request.form["start_time"],
    )
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # e.g., on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Show could not be listed.')
    abort(500)
  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
