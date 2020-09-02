import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import dateutil.parser
import babel
from .models import setup_db, Movie, Actor
from .auth import AuthError, requires_auth


def create_app(test_config=None, database_path=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app, refresh=False)
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
      format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

  app.jinja_env.filters['datetime'] = format_datetime


  '''
  Test endpoint pls ignore
  '''
  @app.route('/')
  def hello():
    return jsonify({
      'success': True,
      'hello': 'world'
    })



  '''
  -------------------------------------------------------------------------------------------------------------
                                              Actor endpoints
  -------------------------------------------------------------------------------------------------------------
  '''


  '''
  GET /actors
    Returns all actors
  '''
  @app.route('/actors', methods=['GET'])
  @requires_auth('view:actors')
  def get_actors(f):
    actors = Actor.query.all()

    if actors == None:
      abort(404)

    f_actors = [actor.format() for actor in actors]

    return jsonify({
      'success': True,
      'actors': f_actors
    })

  '''
  DELETE /actors/:id
    Takes param <id> and deletes the corresponding actor
  '''
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(f, actor_id):
    return jsonify({
      'not': 'implemented'
    })

  '''
  POST /actors
    Creates a new actor
  '''

  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actor')
  def post_actor(f):
    body = request.get_json()
    
    if body == None:
      abort(422)

    name = body.get('name', None)
    age = body.get('age',None)
    gender = body.get('gender', None)

    if (name==None) or (age==None) or (gender==None):
      abort(422)
    
    actor = Actor(
      name = name,
      age=age,
      gender=gender
    )

    actor.insert()

    return jsonify({
      'success': True,
      'created_id': actor.id
    })

  '''
  PATCH /actors
    Updates properties of existing actors
  '''
  @app.route('/actors', methods=['PATCH'])
  @requires_auth('edit:actor')
  def patch_actor(f):
    return jsonify({
    'not': 'implemented'
  })  




  '''
  -------------------------------------------------------------------------------------------------------------
                                              Movie endpoints
  -------------------------------------------------------------------------------------------------------------
  '''
  '''
  GET /movies
    Returns all movies
  '''
  @app.route('/movies', methods=['GET'])
  @requires_auth('view:movies')
  def get_movies(f):
    movies = Movie.query.all()

    if movies == None:
      abort(404)

    f_movies = [movie.format() for movie in movies]

    return jsonify({
      'success': True,
      'movies': f_movies
    })



  '''
  DELETE /movies/:id
    Takes param <id> and deletes the corresponding movie
  '''
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(f, drink_id):
    return jsonify({
      'not': 'implemented'
    })


  '''
  POST /movies
    Creates a new movie
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movie')
  def post_movie(f):
    body = request.get_json()
    
    if body == None:
      abort(422)

    title = body.get('title', None)
    release_date = body.get('release_date',None)

    if (release_date==None) or (title==None) :
      abort(422)
    
    movie = Movie(
      title=title,
      release_date=release_date,
    )

    movie.insert()

    return jsonify({
      'success': True,
      'created_id': movie.id
    })

  '''
  PATCH /movies
    Updates properties of existing actors
  '''
  @app.route('/movies', methods=['PATCH'])
  @requires_auth('edit:movie')
  def patch_movie(f):
    return jsonify({
    'not': 'implemented'
  })  

  '''
  -------------------------------------------------------------------------------------------------------------
                                              Error Handlers
  -------------------------------------------------------------------------------------------------------------
  '''

  '''
  422 - unprocessable
  '''
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
    }), 422

  '''
  404 - not found
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not Found'
    }), 404

  '''
  401 - Unauthorized
  '''
  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401
  
    
  return app







