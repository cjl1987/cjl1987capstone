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

        setup_db(self.app, self.database_path)

        # sample movie used in the tests
        self.new_movie = {
            "title": "Men in Black",
            "date": "2002"
        }

        # sample actor used in the tests
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

    # Test POST /movies --RBAC - Error
    # Casting Assistant is not allowed to perform POST /movies
    def test_create_new_movie_RBAC_error(self):
        token_assistant = os.environ['TOKEN_ASSISTANT']
        res = self.client().post(
            '/movies',
            json={"title": "Men in Black2", "date": "2002"},
            headers={"Authorization": "Bearer "+token_assistant}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 403)

    # Test POST /movies --Authorization - Error ===========================
    def test_create_new_movie_authorization_error(self):
        res = self.client().post(
            '/movies', json={"title": "Men in Black2", "date": "2002"}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 401)

    # Test POST /movies ===========================
    def test_create_new_movie(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        res = self.client().post(
            '/movies', json={"title": "Men in Black2", "date": "2002"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    # Test POST /movies - Error
    def test_create_new_movie_error(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        res = self.client().post(
            '/movies', json={"title": "Men in Black2"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # Test GET /movies
    def test_get_movies(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        res = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer "+token_Producer}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test GET /movies - Error
    def test_get_movies_error(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        # Call endpoint with missing 's' at the end
        res = self.client().get(
            '/movie',
            headers={"Authorization": "Bearer "+token_Producer}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Test DELETE /movies
    def test_delete_movie(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        setup_response = self.client().post(
            '/movies', json={"title": "Men in Black2", "date": "2002"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        tmp = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().delete(
            '/movies/'+str(tmp['movie_id']),
            headers={"Authorization": "Bearer "+token_Producer}
            )
        movie = Movies.query.filter(Movies.id == tmp['movie_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    # Test DELETE /movies - Error
    def test_delete_movie_error(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        setup_response = self.client().post(
            '/movies', json={"title": "Men in Black2", "date": "2002"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        tmp = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().delete(
            '/movies/'+str(tmp['movie_id']+2000),
            headers={"Authorization": "Bearer "+token_Producer}
            )
        movie = Movies.query.filter(Movies.id == tmp['movie_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(bool(movie.id), not None)

    # Test PATCH /movies
    def test_patch_movie(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        setup_response = self.client().post(
            '/movies', json={"title": "Men in Black2", "date": "2002"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        tmp = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().patch(
            '/movies/'+str(tmp['movie_id']),
            json={"title": "Fast and Furious", "date": "2002"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        movie = Movies.query.filter(Movies.id == tmp['movie_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.title, "Fast and Furious")

    # Test PATCH /movies - Error
    def test_patch_movie_error(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        setup_response = self.client().post(
            '/movies', json={"title": "Men in Black2", "date": "2002"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        tmp = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().patch(
            '/movies/'+str(tmp['movie_id']+2000),
            headers={"Authorization": "Bearer "+token_Producer}
            )
        movie = Movies.query.filter(Movies.id == tmp['movie_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test POST /actors =======================================
    def test_create_new_actor(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        res = self.client().post(
            '/actors', json={"name": "Ryan", "gender": "female", "age": "32"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    # Test POST /actors - Error
    def test_create_new_actor_error(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        res = self.client().post(
            '/actors', json={"name": "Ryan", "gender": "female"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # Test GET /actors
    def test_get_actors(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        res = self.client().get(
            '/actors', headers={"Authorization": "Bearer "+token_Producer}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test GET /actors - Error
    def test_get_actors_error(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        # Call endpoint with missing 's' at the end
        res = self.client().get(
            '/actor', headers={"Authorization": "Bearer "+token_Producer}
            )
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Test DELETE /actors
    def test_delete_actor(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        setup_response = self.client().post(
            '/actors', json={"name": "Ryan", "gender": "female", "age": "32"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        tmp = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().delete(
            '/actors/'+str(tmp['actor_id']),
            headers={"Authorization": "Bearer "+token_Producer}
            )
        actor = Actors.query.filter(Actors.id == tmp['actor_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    # Test DELETE /actors - Error
    def test_delete_actor_error(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        setup_response = self.client().post(
            '/actors', json={"name": "Ryan", "gender": "female", "age": "32"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        tmp = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().delete(
            '/actors/'+str(tmp['actor_id']+2000),
            headers={"Authorization": "Bearer "+token_Producer}
            )
        actor = Actors.query.filter(Actors.id == tmp['actor_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(bool(actor.id), not None)

    # Test PATCH /actors
    def test_patch_actor(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        setup_response = self.client().post(
            '/actors', json={"name": "Ryan", "gender": "female", "age": "32"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        tmp = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().patch(
            '/actors/'+str(tmp['actor_id']),
            json={"name": "Bud Spencer", "gender": "male", "age": "57"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        actor = Actors.query.filter(Actors.id == tmp['actor_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.name, "Bud Spencer")

    # Test PATCH /actors - Error
    def test_patch_actor_error(self):
        token_Producer = os.environ['TOKEN_PRODUCER']
        setup_response = self.client().post(
            '/actors', json={"name": "Ryan", "gender": "female", "age": "32"},
            headers={"Authorization": "Bearer "+token_Producer}
            )
        tmp = json.loads(setup_response.data.decode('utf-8'))
        res = self.client().patch(
            '/actors/'+str(tmp['actor_id']+2000),
            headers={"Authorization": "Bearer "+token_Producer}
            )
        actor = Actors.query.filter(Actors.id == tmp['actor_id']).one_or_none()
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
