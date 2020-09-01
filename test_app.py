import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Actor, Movie
from app import create_app

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.db_username = os.getenv('DB_USERNAME')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_url = os.getenv('DB_URL')
        self.db_name = os.getenv('DB_NAME')
        self.database_path = "postgres://{}:{}@{}/{}".format(self.db_username, self.db_password, self.db_url, self.db_name)

        self.app = create_app()
        self.client = self.app.test_client
        
        setup_db(self.app,refresh=True)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass


    '''
    -------------------------------------------------------------------------------------------------------------
                                            Actor endpoint Tests
    -------------------------------------------------------------------------------------------------------------
    '''

    '''
    GET /actors tests
    '''
    def test_get_actors_success(self):
        res = self.client().get('/actors')
        print(res.data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_get_actors_failure(self):
        pass

    '''
    DELETE /actors tests
    '''

    def test_delete_actors_success(self):
        pass

    def test_delete_actors_failure(self):
        pass

    '''
    POST /actors tests
    '''

    def test_post_actors_success(self):
        pass

    def test_post_actors_failure(self):
        pass

    '''
    PATCH /actors tests
    '''

    def test_patch_actors_success(self):
        pass

    def test_patch_actors_failure(self):
        pass

    '''
    -------------------------------------------------------------------------------------------------------------
                                            Movie endpoint Tests
    -------------------------------------------------------------------------------------------------------------
    '''

    '''
    GET /movies tests
    '''

    def test_get_movies_success(self):
        pass

    def test_get_movies_failure(self):
        pass

    '''
    DELETE /movies tests
    '''
    def test_delete_movies_success(self):
        pass

    def test_delete_movies_failure(self):
        pass

    '''
    POST /movies tests
    '''
    def test_post_movies_success(self):
        pass

    def test_post_movies_failure(self):
        pass

    '''
    PATCH /movies tests
    '''
    def test_patch_movies_success(self):
        pass

    def test_patch_movies_failure(self):
        pass

    '''
    -------------------------------------------------------------------------------------------------------------
                                            Role Tests
    -------------------------------------------------------------------------------------------------------------
    '''

