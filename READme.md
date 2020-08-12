#Full Stack Capstone Project: Casting Agency 

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. 

Models:

    Movies with attributes title and release date
    Actors with attributes name, age and gender

Endpoints:

    GET /actors and /movies
    DELETE /actors/ and /movies/
    POST /actors and /movies and
    PATCH /actors/ and /movies/

Roles:

    Casting Assistant
        Can view actors and movies
    Casting Director
        All permissions a Casting Assistant has and…
        Add or delete an actor from the database
        Modify actors or movies
    Executive Producer
        All permissions a Casting Director has and…
        Add or delete a movie from the database


##Getting Started

Pre-requisites and Local Development

Developers using this project should already have Python3 and pip nstalled on their local machines.


###Setup Backend 

First have your virtual environment setup and running in `/cjl1987capstone`
	
```bash
source env/bin/activate 
```

Then install dependencies by navigating to the `/cjl1987capstone` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


###Running Backend server in Dev Mode

From within the `/cjl1987capstone` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
FLASK_APP=app.py FLASK_DEBUG=true flask run
```


### Testing
To run the tests, first set the environment variables and then start the test script

```bash
. setupsh
python test_app.py
```


##API Reference

###Getting started 
	- Base URL: This application does run 
        - locally following the link http://127.0.0.1:5000/ 
        - on heroku.com folling the base link https://cjl1987capstone.herokuapp.com/
	- Authentication: This version does require a valid bearer token


###Roles
- Casting Assistant
		  "permissions": 
			[
			    "get:actors",
			    "get:movies",
			]
- Casting Director
		  "permissions": 
			[
			    "delete:actors",
			    "get:actors",
			    "get:movies",
			    "patch:actors",
			    "patch:movies",
			    "post:actors",

			]
- Executive Producer
		  "permissions": 
			[
			    "delete:actors",
			    "delete:movies",
			    "get:actors",
			    "get:movies",
			    "patch:actors",
			    "patch:movies",
			    "post:actors",
			    "post:movies"
			]



###Endpoints

###Error Handling
The error response is in JSON in the following format:
	{
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
        }), error.status_code
	}

The API handles the following types of errors:
	- 400: 	'Bad request' / 'Invalid claims'
	- 401: 	'Authorization not sent' / 'Authorization not valid'
	- 403:  'Unauthorized'
	- 404:	'Not found' 
	- 422:	'Unprocessable Entity'


####GET /movies
- General	
	- Returns all available movies
- Sample
	- https://cjl1987capstone.herokuapp.com/movies
	- Authorization: bearer{{TOKEN}}
	
- Response
	{
	    "movies": [
		{
		    "date": "2002",
		    "id": 3,
		    "title": "Men in Black"
		},
		{
		    "date": "2002",
		    "id": 7,
		    "title": "Men in Black"
		},
		{
		    "date": "2002",
		    "id": 8,
		    "title": "Men in Black"
		}
	    ],
	    "success": true
	}


####GET /actors
- General	
	- Returns all available actors
- Sample
	- https://cjl1987capstone.herokuapp.com/actors
	- Authorization: bearer{{TOKEN}}
- Response
	{
	    "actors": [
		{
		    "age": 32,
		    "gender": "female",
		    "id": 1,
		    "name": "Meg Ryan"
		},
		{
		    "age": 32,
		    "gender": "male",
		    "id": 8,
		    "name": "Roger Less"
		}
	    ],
	    "success": true
	}


####POST /movies
- General	
	- Creates a new movie in the database
- Sample
	- https://cjl1987capstone.herokuapp.com/movies
	- Authorization: bearer{{TOKEN}}
	- Content-Type: application/json
	- Body: 
		{
		    "title": "Men in Black",
		    "date": "2002"
		}
		
- Response: 
	{
	    "movie_id": 8,
	    "success": true
	}


####POST /actors
- General	
	- Creates a new actor in the database
- Sample
	- https://cjl1987capstone.herokuapp.com/actors
	- Authorization: bearer{{TOKEN}}
	- Content-Type: application/json
	- Body: 
		{
		    "name": "Meg Ryan",
		    "gender": "female", 
		    "age": "32"
		}
		
- Response: 
	{
	    "actor_id": 10,
	    "success": true
	}


####DELETE /movies/<int:id>
- General	
	- Deletes one movie by id using url parameter
	- Returns the id of deleted actor
- Sample
	- https://cjl1987capstone.herokuapp.com/movies/6
	- Authorization: bearer{{TOKEN}}
- Response
	{
	    "deleted": 6,
	    "success": true
	}


####DELETE /actors/<int:id>
- General	
	- Deletes one actor by id using url parameter
	- Returns the id of deleted actor
- Sample
	- https://cjl1987capstone.herokuapp.com/actors/6
	- Authorization: bearer{{TOKEN}}
- Response
	{
	    "deleted": 6,
	    "success": true
	}


####Patch /movies/6
- General	
	- Change the data set of a movie in the database
- Sample
	- https://cjl1987capstone.herokuapp.com/movies/1
	- Authorization: bearer{{TOKEN}}
	- Content-Type: application/json
	- Body: 
		{
		    "title": "Fast & Greate", 
		    "date": "2002"
		 
		}	
- Response: 
	{
	    "success": true,
	    "updated movie": {
		"date": "2002",
		"id": 8,
		"title": "Fast & Greate"
	    }
	}


####Patch /actors/6
- General	
	- Change the data set of an actor in the database
- Sample
	- https://cjl1987capstone.herokuapp.com/actors/1
	- Authorization: bearer{{TOKEN}}
	- Content-Type: application/json
	- Body: 
		{
		    "name": "Roger Less",
		    "gender": "male", 
		    "age": "32"
		}
		
- Response: 
	{
	    "success": true,
	    "updated actor": {
		"age": 32,
		"gender": "male",
		"id": 1,
		"name": "Roger Less"
	    }
	}


##Authors and API Reference
Christoph Leichte edited and created the API interface (api.py), test suite (test_app.py) and README. The other files in this project were provided by Udacity in the framework of the Nanodegree 'Full Stack Web Developer'.


##Acknowledgements
Great thanks to Nikolai, pushing my progress.

