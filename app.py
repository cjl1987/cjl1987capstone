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


    # GET Movies
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


    # POST /movie expects a body with 'title' and 'date'
    @app.route('/movies', methods=['POST'])
    #@requires_auth('post:drinks')                                          #to be uncommented later
    def create_movie():                                                  # to be replaced by: <def create_drink(jwt):>   JWT!!
        # get json object
        body = request.get_json()
        new_title = body.get('title', None)
        new_date = body.get('date', None)

        # check whether user input is complete
        if new_title is None:
            abort(400)                                                 #create here correct error-handler
        if new_date is None:
            abort(400)

        try:
            # add row in data base
            movie = Movies(title=new_title, date=new_date)
            movie.insert()
            # return json response
            return jsonify({
                            "success": True
                            }), 201
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

    '''
    # Error-Handler 404
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404
    '''

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

