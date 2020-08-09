import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        
        #self.database_name = "trivia_test"
        #self.database_path = "postgresql://caryn:geheimwort@localhost:5432/trivia_test"   #"postgres://{}/{}".format('localhost:5432', self.database_name)       #"postgresql://caryn:geheimwort@localhost:5432/trivia"  #My_TODO:Check path
        
        setup_db(self.app, self.database_path)

        #sample movie used in the tests
        self.new_movie = {
            "title": "Men in Black",
            "date": "2002"
        }

        #sample actor used in the tests
        self.new_actor = {
            "name": "Meg Ryan",
            "gender": "female", 
            "age": "32"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    """
    Tests to be executed
    """
        
    #Test POST /movies
    def test_create_new_movie(self):
        res = self.client().post('/movies', json={"title": "Men in Black2", "date": "2002"})
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    #Test POST /movies - Error
    def test_create_new_movie_error(self):
        res = self.client().post('/movies', json={"title": "Men in Black2"})
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    #Test GET /movies
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data.decode('utf-8')) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test GET /movies - Error
    def test_get_movies_error(self):
        # Call endpoint with missing 's' at the end
        res = self.client().get('/movie')                       
        data = json.loads(res.data.decode('utf-8')) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

   #Test DELETE /movies
    def test_delete_movie(self):
        setup_response = self.client().post('/movies', json={"title": "Men in Black2", "date": "2002"})
        data_setup = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().delete('/movies/'+str(data_setup['movie_id']))
        movie = Movies.query.filter(Movies.id==data_setup['movie_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8')) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

   #Test DELETE /movies - Error
    def test_delete_movie_error(self):
        setup_response = self.client().post('/movies', json={"title": "Men in Black2", "date": "2002"})
        data_setup = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().delete('/movies/'+str(data_setup['movie_id']+2000))
        movie = Movies.query.filter(Movies.id==data_setup['movie_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8')) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(bool(movie.id), not None)
    '''
    #Test DELETE  /questions/<int:question_id>
    def test_delete_question_by_id(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data.decode('utf-8'))

        question = Question.query.filter(Question.id==5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question'], 5)
        self.assertEqual(question, None)

    #Test DELETE  /questions/<int:question_id>  - Error
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    '''

    #Test POST /actors =======================================
    def test_create_new_actor(self):
        res = self.client().post('/actors', json={"name": "Meg Ryan", "gender": "female", "age": "32"})
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    #Test POST /actors - Error
    def test_create_new_actor_error(self):
        res = self.client().post('/actors', json={"name": "Meg Ryan", "gender": "female"})
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    #Test GET /actors
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test GET /actors - Error
    def test_get_actors_error(self):
        # Call endpoint with missing 's' at the end
        res = self.client().get('/actor')                       
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

   #Test DELETE /actors
    def test_delete_actor(self):
        setup_response = self.client().post('/actors', json={"name": "Meg Ryan", "gender": "female", "age": "32"})
        data_setup = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().delete('/actors/'+str(data_setup['actor_id']))
        actor = Actors.query.filter(Actors.id==data_setup['actor_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8')) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

   #Test DELETE /actors - Error
    def test_delete_actor_error(self):
        setup_response = self.client().post('/actors', json={"name": "Meg Ryan", "gender": "female", "age": "32"})
        data_setup = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().delete('/actors/'+str(data_setup['actor_id']+2000))
        actor = Actors.query.filter(Actors.id==data_setup['actor_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8')) 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(bool(actor.id), not None)



'''  
    #Test GET /actors
    def test_get_paginated_questions(self):
        res=self.client().get('/questions')
        data = json.loads(res.data.decode('utf-8'))  
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    #Test GET /questions - Error 
    def test_404_sent_requesting_beyond_valid_page(self):
        res=self.client().get('/questions?page=1000', )
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')




    #Test DELETE  /questions/<int:question_id>
    def test_delete_question_by_id(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data.decode('utf-8'))

        question = Question.query.filter(Question.id==5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question'], 5)
        self.assertEqual(question, None)

    #Test DELETE  /questions/<int:question_id>  - Error
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)



    #Test POST endpoint to create new questions
    def test_create_new_question(self):
        res = self.client().post('/questions', json={"question":"How high is the Eiffel tower?", "answer":"300 meter", "difficulty": 4, "category":"1"})
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)

    #Test POST endpoint to create new questions - Error 
    def test_422_create_new_question_with_missing_json_data(self):
        res = self.client().post('/questions', json={"answer":"300 meter", "difficulty": 4, "category":"1"})
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    
    #Test POST to get questions based on a search term.
    def test_search_Term(self):
        res = self.client().post('/questions', json={"searchTerm":"paint"})
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    #Test POST to get questions based on a search term. - Error
    def test_422_if_search_Term_does_not_match(self):
        res = self.client().post('/questions', json={"searchTerm":"ü"})
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    #Test GET endpoint to get questions based on category.
    def test_get_questions_based_on_categories(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data.decode('utf-8'))
      
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    #Test GET endpoint to get questions based on category.  - Error
    def test_422_get_questions_based_on_categories_category_not_available(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data.decode('utf-8'))
      
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    

    #Test POST to start quizz.
    def test_start_quizz(self):
        res = self.client().post('/quizzes', json={"previous_questions":[20],"quiz_category":{"type":"Science","id":"1"}})
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))


    #Test POST to start quizz. - Error
    def test_422_start_quizz_no_category_in_json(self):
        res = self.client().post('/quizzes', json={"previous_questions":[20]})
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

'''


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

