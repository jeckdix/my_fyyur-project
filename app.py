#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from ast import Raise
from calendar import WEDNESDAY
import json
from lib2to3.pgen2.pgen import generate_grammar
from ntpath import join
from pickle import FALSE
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://babajide@localhost:5432/fyyur'

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.String(255), nullable=True)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)
    venue_genres = db.relationship('Venue_genre', lazy=True)
    
class City (db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(), nullable=False)
    venues = db.relationship('Venue', backref='city', lazy=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))

class State (db.Model):
  __tablename__ = 'state'
  id = db.Column(db.Integer, primary_key =True)
  name = db.Column(db.String, nullable=False)
  cities = db.relationship('City', backref='state', lazy=True)

class Genre (db.Model):
  __tablename__ = 'genre'
  id = db.Column(db.Integer, primary_key =True)
  name = db.Column(db.String(), nullable=False)
    
class Artist_genre (db.Model):
    __tablename__ = 'artist_genre'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable = False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable = False)
    genre = db.relationship('Genre', backref='artist_genre', lazy=True)
    
class Venue_genre (db.Model):
    __tablename__ = 'venue_genre'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable = False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable = False)
  
    # 1 venue m shows, 

# class Genre (db.Model):
#     __tablename__ = 'genres'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(), nullable=False)
#     venue = db.relationship('Venue', backref='genre_table', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city_id = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(120),  nullable=False)
    image_link = db.Column(db.String(500),  nullable=False)
    facebook_link = db.Column(db.String(120),  nullable=False)
    seeking_venue = db.Column(db.String(), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_description = db.Column(db.String(), nullable=True)
    show = db.relationship('Show', backref='artist', lazy=True)
    artist_genre= db.relationship('Artist_genre', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show (db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False )


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
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
    # TODO: replace with real venues data.
    # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    all_cities = City.query.join(State).order_by(State.name).all()
    # all_city_venues = Venue.query.filter_by(city_id=)
    
    the_data = []
    
    for city in all_cities:
      venues = Venue.query.filter_by(city_id=city.id).all()
      city_dict = {
        "city": city.name,
        "state": city.state.name,
        "venues": venues
      }
      the_data.append(city_dict)
      
      


    data = [{
        "city": "San Francisco",
        "state": "CA", 
        "venues": [{
            "id": 1,
            "name": "The Musical Hop",
            "num_upcoming_shows": 0,
        }, {
            "id": 3,
            "name": "Park Square Live Music & Coffee",
            "num_upcoming_shows": 1,
        }]
    }, {
        "city": "New York",
        "state": "NY",
        "venues": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }]

    return render_template('pages/venues.html', areas=the_data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    
    q = request.form.get('search_term')
    search_result = Venue.query.filter(Venue.name.ilike("%" + q + "%")).all()
    
    # print(search_result[0])
    # print(search_result[1])
    
    response_data = {
      "count": len(search_result),
      "data": search_result
    }
    
    
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response_data, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    
    venue = Venue.query.all()
    
    data1 = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "past_shows": [{
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2 = {
        "id": 2,
        "name": "The Dueling Pianos Bar",
        "genres": ["Classical", "R&B", "Hip-Hop"],
        "address": "335 Delancey Street",
        "city": "New York",
        "state": "NY",
        "phone": "914-003-1132",
        "website": "https://www.theduelingpianos.com",
        "facebook_link": "https://www.facebook.com/theduelingpianos",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }
    data3 = {
        "id": 3,
        "name": "Park Square Live Music & Coffee",
        "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
        "address": "34 Whiskey Moore Ave",
        "city": "San Francisco",
        "state": "CA",
        "phone": "415-000-1234",
        "website": "https://www.parksquarelivemusicandcoffee.com",
        "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "past_shows": [{
            "artist_id": 5,
            "artist_name": "Matt Quevedo",
            "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
        }],
        "upcoming_shows": [{
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
        }],
        "past_shows_count": 1,
        "upcoming_shows_count": 1,
    }
    data = list(filter(lambda d: d['id'] ==
                venue_id, [data1, data2, data3]))[0]
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

def create_city(name, state_id):
  city = City(
    name=name,
    state_id=state_id
  )
  try:
    db.session.add(city)
    db.session.flush()
    city_id = city.id
    db.session.commit()
    return city_id
  except:
    return None

def get_state_id(state):
  result = State.query.filter_by(name=state).first()
  
  if result == None:
    new_state_data = State(name=state)
    db.session.add(new_state_data)
    db.session.commit()
    new_state =  State.query.filter_by(name=state).first()
    return new_state.id
  return result.id

def get_city_id(city, state_id):
  result = City.query.filter_by(name=city).first()
  if result == None:
    print('Getting here')
    return create_city(city, state_id)
  return result.id

def get_genre_ids(genres):
  print("Getting to get_genre_ids ")
  print(genres)
  result = Genre.query.filter(Genre.name.in_(genres)).all()
  print(result)
  print('point 1')
  genre_names = []
  genre_ids = []
  for genre in result:
    genre_names.append(genre.name)
    genre_ids.append(genre.id)
   
  if len(genres) == len(genre_ids):
    print('point 2')
    return genre_ids
  
  new_genre_names =  []
  create_genre_insert = []
  for genre in genres:
    print('point 3')
    if genre not in genre_names:
      genre_insert = Genre(name=genre)
      new_genre_names.append(genre)
      create_genre_insert.append(genre_insert)
  
  db.session.add_all(create_genre_insert)
  db.session.commit()
  
  print('point 4 ngn')
  print(new_genre_names)
  newly_inserted = Genre.query.filter(Genre.name.in_(new_genre_names)).all()
  

  print('point 5')
  new_genre_ids = []

  for gengen in newly_inserted:
    new_genre_ids.append(gengen.id)
  all_genre_ids = genre_ids + new_genre_ids
  
  print(all_genre_ids)
  print('point 5')
  return all_genre_ids

def build_venue_genre_insert(genre_ids, venue_id):
  inserts = []
  for genre_id in genre_ids:
    insertQuery = Venue_genre(venue_id=venue_id, genre_id=genre_id)
    inserts.append(insertQuery)
  return inserts
 
def build_artist_genre_insert(genre_ids, artist_id):
  inserts = []
  for genre_id in genre_ids:
    insertQuery = Artist_genre(artist_id=artist_id, genre_id=genre_id)
    inserts.append(insertQuery)
  return inserts 

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)
  

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
        name = request.form.get('name')
        city = request.form.get('city')  
        address = request.form.get('address')
        state = request.form.get('state')
        phone = request.form.get('phone')
        genres = request.form.getlist('genres')
        image_link = request.form.get('image_link')
        website_link = request.form.get('website_link')
        facebook_link = request.form.get('facebook_link')
        seeking_talent = request.form.get('seeking_talent')
        seeking_description = request.form.get('seeking_description')
        
        print(genres)
        print("Point")
        state_id = get_state_id(state)
        city_id = get_city_id(city, state_id)
        print(city_id)
        genre_ids = get_genre_ids(genres)
        venue_data = Venue(
            name=name,
            city_id=city_id,
            address = address,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            website_link = website_link,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description
        )
        db.session.add(venue_data)
        db.session.flush()
        
        venue_id = venue_data.id
        genre_query = build_venue_genre_insert(genre_ids, venue_id)
        db.session.add_all(genre_query)
        db.session.commit()      
    except Exception as e:
      print('this is the error =>', str(e))
      error = True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    
    
    artists = Artist.query.all()
    
    data = [{
        "id": 4,
        "name": "Guns N Petals",
    }, {
        "id": 5,
        "name": "Matt Quevedo",
    }, {
        "id": 6,
        "name": "The Wild Sax Band",
    }]
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    q = request.form.get("search_term")
    print(q)
    search_result = Artist.query.filter(Artist.name.ilike("%" + q + "%")).all()
    
    # print(search_result[0])
    # print(search_result[1])
    
    response_data = {
      "count": len(search_result),
      "data": search_result
    }
    
    
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response_data, search_term=request.form.get('search_term', ''))

def get_genre_name(id):
  result = Genre.query.filter_by(id=id).first()
  return result.name
  
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    
    # artist = Artist.query.filter_by(id=artist_id).join(City, Artist.city_id==City.id).first()
    artist_data = {}
    artist = Artist.query.filter_by(id=artist_id).join(Artist_genre, Artist.id==Artist_genre.artist_id).first()
    artist_city = City.query.filter_by(id=artist.city_id).join(State, City.state_id==State.id).first()
    artist_past_shows = Show.query.filter_by(artist_id=artist.id).filter(Show.start_time < datetime.datetime.now()).join(Venue, Show.venue_id==Venue.id).all()
    artist_future_shows = Show.query.filter_by(artist_id=artist.id).filter(Show.start_time > datetime.datetime.now()).join(Venue, Show.venue_id==Venue.id).all()
    artist_past_shows_n = []
    artist_future_shows_n = []
    
    for show in artist_past_shows:
      this_show = {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": str(show.start_time)
      }
      artist_past_shows_n.append(this_show)

    for show in artist_future_shows:
      this_show = {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": str(show.start_time)
      }
      artist_future_shows_n.append(this_show)
    
    # artist_past_shows = Show.query.filter(artist_id=artist.id).all()
    
  
    
    print(artist_past_shows)
    print(artist_future_shows)
    
    
    print(artist_city)
    print(artist_city.name)
    print(artist_city.state)
    print(artist.id)
    artist_data['id']= artist.id
    artist_data["name"] = artist.name
    artist_data["genres"] = [get_genre_name(genre.id) for genre in artist.artist_genre]
    artist_data['phone'] = artist.phone
    artist_data["city"] = artist_city.name
    artist_data["state"] = artist_city.state.name
    artist_data['image_link']= artist.image_link
    artist_data['facebook_link']= artist.facebook_link
    artist_data['website_link']= artist.website_link
    artist_data['seeking_talent'] = artist.seeking_venue
    artist_data['seeking_description'] = artist.seeking_description
    artist_data['past_shows'] = artist_past_shows_n
    artist_data['upcoming_shows'] = artist_future_shows_n
    artist_data['past_shows_count'] = len(artist_past_shows_n)
    artist_data['upcoming_shows_count'] = len(artist_future_shows_n)
     
    
    # .join(Genre, Artist_genre.id==Genre.id).first()
  
    data1 = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2 = {
        "id": 5,
        "name": "Matt Quevedo",
        "genres": ["Jazz"],
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "past_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data3 = {
        "id": 6,
        "name": "The Wild Sax Band",
        "genres": ["Jazz", "Classical"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "past_shows": [],
        "upcoming_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
        }],
        "past_shows_count": 0,
        "upcoming_shows_count": 3,
    }
    # data = list(filter(lambda d: d['id'] ==
    #             artist_id, [data1, data2, data3]))[0]
    return render_template('pages/show_artist.html', artist=artist_data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

# // 

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        genres = request.form.getlist('genres')
        image_link = request.form.get('image_link')
        website_link = request.form.get('website_link')
        facebook_link = request.form.get('facebook_link')
        seeking_venue = request.form.get('seeking_venue')
        seeking_description = request.form.get('seeking_description')
        
        state_id = get_state_id(state)
        city_id = get_city_id(city, state_id)
        genre_ids = get_genre_ids(genres)
        
        
        artist = Artist(
            name=name,
            city_id=city_id,
            state_id=state_id,
            phone=phone,
            image_link=image_link,
            website_link = website_link,
            facebook_link=facebook_link,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,
        )
        
        db.session.add(artist)
        db.session.flush()
        
        artist_id = artist.id
        genre_query = build_artist_genre_insert(genre_ids, artist_id)
        db.session.add_all(genre_query)
        db.session.commit()
        
    except Exception as e:
      print('this is the error =>',str(e))
      error = True
      db.session.rollback()
    finally:
      db.session.close()
    
    if error:
      print(error)
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # on successful db insert, flash success
    
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)
  

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    error = False
    try:
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')
      data = Show(
      artist_id = artist_id,
      venue_id = venue_id,
      start_time = start_time   
      )
      db.session.add(data)
      db.session.commit()
    
    except Exception as e:
      print("the error is =>", str(e))
      error = True
    finally:
      db.session.close()
      
    if error:
      flash('An error occurred. Show could not be listed.')
    else:
      flash('Show was successfully listed!')

    # on successful db insert, flash success
    
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
