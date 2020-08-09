import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Movies, Actors
from flask_cors import CORS

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


    #-------------------------------------movies-------------------------------------
    # GET /movies
    @app.route('/movies', methods=['GET'])
    #@requires_auth('post:drinks')                                          #to be uncommented later
    def get_movie():                                                  # to be replaced by: <def create_drink(jwt):>   JWT!!
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
    #@requires_auth('post:drinks')                                          #to be uncommented later
    def create_movie():                                                  # to be replaced by: <def create_drink(jwt):>   JWT!!
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
    #@requires_auth('delete:drinks')                                            # uncomment here
    def delete_movie(movie_id):                                            #change to def delete_drink(jwt, drink_id):
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



    #--------------------------------------------actors----------------------------
    # GET /actors
    @app.route('/actors', methods=['GET'])
    #@requires_auth('post:drinks')                                    # to be uncommented later
    def get_actor():                                                  # to be replaced by: <def create_drink(jwt):>   JWT!!
        try:
            formatted_actors = []
            actors_all = Actors.query.all()   

            for actor in actors_all: 
                formatted_actors.append(actor.format())
            
            # return json response
            return jsonify({
                            "success": True,
                            "movies": formatted_actors,
                            }), 200
        except Exception:
            abort(422)


    # POST /actors expects a body with 'name' and 'gender' and 'age'
    @app.route('/actors', methods=['POST'])
    #@requires_auth('post:drinks')                                       # to be uncommented later
    def create_actor():                                                  # to be replaced by: <def create_drink(jwt):>   JWT!!
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
    #@requires_auth('delete:drinks')                                            # uncomment here
    def delete_actor(actor_id):                                            #change to def delete_drink(jwt, drink_id):
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



    # Error Handling

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

    '''
    # Error-Handler AuthErrors
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code
    '''


    return app

app = create_app()

if __name__ == '__main__':
    app.run()

