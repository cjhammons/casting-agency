import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import setup_db, Movie, Actor

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app, refresh=True)

    return app

app = create_app()

'''
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
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
def get_actors():
    actors = Actor.query.all()

    if actors == None:
      abort(404)

    f_actors = [actors.format() for actor in actors]

    return jsonify({
      'success': True,
      'actors': f_actors
    })


'''
DELETE /actors/:id
  Takes param <id> and deletes the corresponding actor
'''
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(f, drink_id):
    pass

'''
POST /actors
  Creates a new actor
'''
@app.route('/actors', methods=['POST'])
def post_actor():
    pass



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
def get_movies():
    pass


'''
DELETE /movies/:id
  Takes param <id> and deletes the corresponding movie
'''
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(f, drink_id):
    pass

'''
POST /movies
  Creates a new movie
'''
@app.route('/movies', methods=['POST'])
def post_movie():
    pass


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

'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401
'''