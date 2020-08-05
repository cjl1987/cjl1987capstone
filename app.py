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


    # POST /movie expects a body with 'title' and 'date'
    # and will returns {"success": True, "movies": [???]}
    @app.route('/movies', methods=['POST'])
    #@requires_auth('post:drinks')                                          #to be uncommented later
    def create_movie():                                                  # to be replaced by: <def create_drink(jwt):>   JWT!!
        # get json object
        body = request.get_json()
        new_title = body.get('title', None)
        new_date = body.get('date', None)

        # check whether user input is complete
        if new_title is None:
            abort(422)
        if new_date is None:
            abort(422)

        try:
            # add row in data base
            movie = Movies(title=new_title, date=new_date)
            movie.insert()
            selection = Movies.query.all()


            # return json response
            return jsonify({
                            "success": True,
                            "movies": "List of movies",
                            "movies1": selection[0].title
                            }), 201
        except Exception:
            abort(422)


    return app

app = create_app()

if __name__ == '__main__':
    app.run()

