import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Movies, Actors
from flask_cors import CORS
from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)                      
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"


    #----------------movies-------------------------------------
    # GET /movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')                                        
    def get_movie(jwt):                                                 
        try:
            formatted_movies = []
            movies_all = Movies.query.all()   

            for movie in movies_all: 
                formatted_movies.append(movie.format())
            
            # return json response
            return jsonify({
                            "success": True,
                            "movies": formatted_movies,
                            }), 200
        except Exception:
            abort(422)


    # POST /movies expects a body with 'title' and 'date'
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        # get json object
        body = request.get_json()
        new_title = body.get('title', None)
        new_date = body.get('date', None)

        # check whether user input is complete
        if new_title is None:
            abort(400)                                                
        if new_date is None:
            abort(400)

        try:
            # add row in data base
            movie = Movies(title=new_title, date=new_date)
            movie.insert()
            # return json response
            return jsonify({
                            "success": True, 
                            "movie_id": movie.id
                            }), 201
        except Exception:
            abort(422)
    


    # DELETE /movies/<int:movie_id>
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        try:
            # get movie by movie_id
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            # error 404
            if movie is None:
                return jsonify({
                                'success': False,
                                'error': 'Movie is not found', 
                                'movie_id': movie_id
                                }), 404
            # delete row in data base
            movie.delete()
            return jsonify({
                            'success': True,
                            'deleted': movie_id
                            }), 200
        except Exception:
            abort(422)


    # PATCH /movies
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def movies_update(jwt ,movie_id):
        # load PATCH body
        body = request.get_json()
        # get element by id
        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            # error 404
            if movie is None:
                abort(404)
            # prepare body
            if body.get('title'):
                movie.title = body.get('title')
            if body.get('date'):
                movie.date = body.get('date')
            # update data base
            movie.update()
            return jsonify({
                            "success": True,
                            "updated movie": movie.format()
                            }), 200
        except Exception:
            abort(422)



    #--------------actors----------------------------
    # GET /actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(jwt):
        try:
            formatted_actors = []
            actors_all = Actors.query.all()   

            for actor in actors_all: 
                formatted_actors.append(actor.format())
            
            # return json response
            return jsonify({
                            "success": True,
                            "actors": formatted_actors,
                            }), 200
        except Exception:
            abort(422)


    # POST /actors expects a body with 'name' and 'gender' and 'age'
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        # get json object
        body = request.get_json()
        new_name = body.get('name', None)
        new_gender = body.get('gender', None)
        new_age = body.get('age', None)

        # check whether user input is complete
        if new_name is None:
            abort(400)                                                
        if new_gender is None:
            abort(400)
        if new_age is None:
            abort(400)

        try:
            # add row in data base
            actor = Actors(name=new_name, gender=new_gender, age=new_age)
            actor.insert()
            # return json response
            return jsonify({
                            "success": True,
                            "actor_id": actor.id
                            }), 201
        except Exception:
            abort(422)
    
    
    # DELETE  /actors/<int:actor_id>
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        try:
            # get actor by actor_id
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            # error 404
            if actor is None:
                return jsonify({
                                'success': False,
                                'error': 'Actor is not found', 
                                'actor_id': actor_id
                                }), 404
            # delete row in data base
            actor.delete()
            return jsonify({
                            'success': True,
                            'deleted': actor_id
                            }), 200
        except Exception:
            abort(422)



    # PATCH /actors
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def actors_update(jwt, actor_id):
        # load PATCH body
        body = request.get_json()
        # get element by id
        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            # error 404
            if actor is None:
                abort(404)
            # prepare body
            if body.get('name'):
                actor.name = body.get('name')
            if body.get('gender'):
                actor.gender = body.get('gender')
            if body.get('age'):
                actor.age = body.get('age')
            # update data base
            actor.update()
            return jsonify({
                            "success": True,
                            "updated actor": actor.format()
                            }), 200
        except Exception:
            abort(422)



    # ------------------------Error Handling -------------------

    # Error-Handler 422
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    # Error-Handler 404
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    # Error-Handler 400
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success": False,
                        "error": 400,
                        "message": "bad request"
                        }), 400


    # Error-Handler AuthErrors
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
                        "success": False,
                        "error": error.status_code,
                        "message": error.error['description']
                        }), error.status_code
                


    return app

app = create_app()

if __name__ == '__main__':
    app.run()

