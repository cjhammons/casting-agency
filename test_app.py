import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Actor, Movie
from app import create_app

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.db_username = os.getenv('DB_USERNAME')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_url = os.getenv('DB_URL')
        self.db_name = os.getenv('DB_NAME')
        self.database_path = "postgres://{}:{}@{}/{}".format(self.db_username, self.db_password, self.db_url, self.db_name)
        
        #Current JWTs 8:42 pm 9/1/2020
        self.executive_producer_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlA2cnVTOU40aU94U0htTDdrTTdYbiJ9.eyJpc3MiOiJodHRwczovL2NqaGFtbW9ucy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZWFmMTAyMDc2YTcwMDY3OGYxOGJmIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTkwMTgyNDAsImV4cCI6MTU5OTEwNDYzNCwiYXpwIjoidGxhSW5DSFBZOVRIdjN6SjhhRlV1d0IyTmEwUzYwWjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.JyCVkzz4U1NRmdgPVHMLR2_QcDoF2ANcKhm1ZCRLwcpI-MwmLBTEbTm-COSA-BU8xOmgBpbYTXr9FwzCqRoC4jvLM1PdQYzHODHdNwkzlo8Ywhdbnt-HqD8FEmA5xlT-chaCR4Mgl-HWkNp-Xus_xEGzw_SLvkyarPM50KLDaApNwCAK4UUQTIuQibe8xaiFmE27nbMtbs9jEXP5waIls6s4dvz6dUNifwkdjj_bs9hh6GoQBlUiDP6q2wkgv1EIQp6aA26pyxzP_116G_4bA7aoilN7-VY3fqGeogCJRa8j0-qhm1Rqp34TLLQtXfaf0SvXdKxWzeI_z7-tDI2s_w'
        self.casting_assistant_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlA2cnVTOU40aU94U0htTDdrTTdYbiJ9.eyJpc3MiOiJodHRwczovL2NqaGFtbW9ucy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwZjZlMDA3MTQ2OGMwMDEzMDAzYTYyIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTkwMTgwODgsImV4cCI6MTU5OTEwNDQ4MiwiYXpwIjoidGxhSW5DSFBZOVRIdjN6SjhhRlV1d0IyTmEwUzYwWjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.I3momkTT2A7uQCBp470ooJgxmR75Sxz_5eIkA2GBRfRXJSrkEmJBdUp-uNuKBETEIVOxk7fPoeaTswKTqWw_xz_wsPq2wj7N897W8d-Xh-TuEvQC1YTWCPnx7lRXozUsU4C2pC019b93kAH1Fd_segXk99xB4TQ6fUiRCmITU5wNb3D88l2Lfba2OvrdcbfI_eYKUcGLiTyueqgO2Vj9R7oWOYaeUPOorScYeLnTj9D8v9GVMMf_QKLx12CP6EGuC3h2ZieNxbsaruXUC-TRt5lKnF8JapgDbhTvIq95W3yJB7c-f65RhP7vY3AjiV5Cgu3woOKL4mGKm8KVwRRp7g'
        self.casting_director_jwt = ''
        
        setup_db(self.app,refresh=True)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.actor = Actor(
            name='Billy Bob',
            age=22,
            gender='Male'
        )
        self.actor.insert()

        self.test_name = 'John Doe'
        self.test_age = 69
        self.test_gender = 'male'

        self.movie = Movie(
            title='The Thing from Outer space',
            release_date='1/1/2020'
        )
        self.movie.insert()

        self.test_title = 'Bad Movie'
        self.test_release_date = '1/2/2019'       


    def tearDown(self):
        self.actor.delete()
        self.movie.delete()


    '''
    -------------------------------------------------------------------------------------------------------------
                                            Actor endpoint Tests
    -------------------------------------------------------------------------------------------------------------
    '''

    '''
    GET /actors tests
    '''
    def test_get_actors_success(self):
        res = self.client().get('/actors', headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))


    '''
    DELETE /actors tests
    '''

    def test_delete_actors_success(self):
        id = self.actor.id
        res = self.client().delete('/actors/' + str(id), headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(Actor.query.get(id))

    def test_delete_actors_failure(self):
        id = -1
        res = self.client().delete('/actors/' + str(id), headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(Actor.query.get(id))

    '''
    POST /actors tests
    '''

    def test_post_actors_success(self):
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'], True)

        new_actor = Actor.query.get(data['created_id'])
        self.assertEqual(new_actor.name, self.test_name)
        self.assertEqual(new_actor.age, self.test_age)
        self.assertEqual(new_actor.gender, self.test_gender)

        new_actor.delete()

    def test_post_actors_failure_no_gender(self):
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'age': self.test_age
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_actors_failure_no_age(self):
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'gender': self.test_gender
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_actors_failure_no_age(self):
        res = self.client().post('/actors', json={
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    PATCH /actors tests
    '''

    def test_patch_actors_success_name(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.test_name,
        }, headers={
            'Bearer': self.executive_producer_jwt
        })

        data = json.loads(res.data)

        self.assertTrue(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Actor.query.get(self.actor.id).name, self.test_name)


    def test_patch_actors_success_age(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'age': self.test_age,
         }, headers={
            'Bearer': self.executive_producer_jwt
        })

        data = json.loads(res.data)

        self.assertTrue(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Actor.query.get(self.actor.id).age, self.test_age)


    def test_patch_actors_success_gender(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'gender': self.test_gender
         }, headers={
            'Bearer': self.executive_producer_jwt
        })

        data = json.loads(res.data)

        self.assertTrue(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Actor.query.get(self.actor.id).gender, self.test_gender)

    def test_patch_actors_failure_bad_input(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'meme':'rawr XD'
         }, headers={
            'Bearer': self.executive_producer_jwt
        })

        data = json.loads(res.data)

        self.assertTrue(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_actors_failure_bad_id(self):
        id = -1
        res = self.client().patch('/actors/' + str(id), json={
            'gender': self.test_gender
         }, headers={
            'Bearer': self.executive_producer_jwt
        })

        data = json.loads(res.data)

        self.assertTrue(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    -------------------------------------------------------------------------------------------------------------
                                            Movie endpoint Tests
    -------------------------------------------------------------------------------------------------------------
    '''

    '''
    GET /movies tests
    '''

    def test_get_movies_success(self):
        res = self.client().get('/actors', headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))


    def test_get_movies_failure(self):
        pass

    '''
    DELETE /movies tests
    '''
    def test_delete_movies_success(self):
        id = self.movie.id
        res = self.client().delete('/movies/' + str(id), headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(Movie.query.get(id))

    def test_delete_movies_failure(self):
        id = -1
        res = self.client().delete('/movies/' + str(id), headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(Movie.query.get(id))

    '''
    POST /movies tests
    '''
    def test_post_movies_success(self):
        res = self.client().post('/movies', json={
            'title': self.test_title,
            'release_date': self.test_release_date,
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created_id'], True)

        new_movie = Movie.query.get(data['created_id'])
        self.assertEqual(new_movie.title, self.test_title)
        self.assertEqual(new_movie.release_date, self.test_release_date)

        new_movie.delete()

    def test_post_movies_failure_no_title(self):
        res = self.client().post('/movies', json={
            'title': self.test_title,
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_post_movies_failure_no_release_date(self):
        res = self.client().post('/movies', json={
            'title': self.test_title,
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    '''
    PATCH /movies tests
    '''
    def test_patch_movies_success_title(self):
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'title': self.test_name,
        }, headers={
            'Bearer': self.executive_producer_jwt
        })

        data = json.loads(res.data)

        self.assertTrue(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Movie.query.get(self.movie.id).title, self.test_title)

    def test_patch_movies_success_release_date(self):
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'release_date': self.test_release_date,
        }, headers={
            'Bearer': self.executive_producer_jwt
        })

        data = json.loads(res.data)

        self.assertTrue(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Movie.query.get(self.movie.id).release_date, self.test_release_date)

    def test_patch_movies_failure_bad_input(self):
        id = self.movie.id
        res = self.client().patch('/actors/' + str(id), json={
            'memes': 'WOLOLOLOLOLOL'
         }, headers={
            'Bearer': self.executive_producer_jwt
        })

        data = json.loads(res.data)

        self.assertTrue(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_movies_failure_bad_id(self):
        id = -1
        res = self.client().patch('/actors/' + str(id), json={
            'release_date': self.test_release_date,
         }, headers={
            'Bearer': self.executive_producer_jwt
        })

        data = json.loads(res.data)

        self.assertTrue(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    -------------------------------------------------------------------------------------------------------------
                                            Role Tests
    -------------------------------------------------------------------------------------------------------------
    '''

    def test_casting_assistant_authorized(self):
        res = client().get('/actors', headers={
            'Bearer': self.casting_assistant_jwt
        })
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)

        res = client().get('/movies', headers={
            'Bearer': self.casting_assistant_jwt
        })
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)

    def test_casting_assistant_unauthorized(self):
        # post actor
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
            'Bearer': self.casting_assistant_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        Actor.query().get(data['created_id'])

        # patch actor
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.test_name,
        }, headers={
            'Bearer': self.casting_assistant_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

        # delete actor
        id = self.actor.id
        res = self.client().delete('/actors/' + str(id), headers={
            'Bearer': self.casting_assistant_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

        #post movie
        res = self.client().post('/movies', json={
            'title': self.test_title,
            'release_date': self.test_release_date,
        }, headers={
            'Bearer': self.casting_assistant_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        Movie.query.get(data['created_id']).delete()

        #patch movie
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'title': self.test_name,
        }, headers={
            'Bearer': self.casting_assistant_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

        #delete movie
        id = self.movie.id
        res = self.client().delete('/movies/' + str(id), headers={
            'Bearer': self.casting_assistant_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_casting_director_authorized(self):
        res = client().get('/actors', headers={
            'Bearer': self.casting_director_jwt
        })
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)

        res = client().get('/movies', headers={
            'Bearer': self.casting_director_jwt
        })
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)

        # post actor
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
            'Bearer': self.casting_director_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        Actor.query().get(data['created_id'])

        # patch actor
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.test_name,
        }, headers={
            'Bearer': self.casting_director_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        # delete actor
        id = self.actor.id
        res = self.client().delete('/actors/' + str(id), headers={
            'Bearer': self.casting_director_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        #patch movie
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'title': self.test_name,
        }, headers={
            'Bearer': self.casting_director_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_casting_director_unauthorized(self):
        #post movie
        res = self.client().post('/movies', json={
            'title': self.test_title,
            'release_date': self.test_release_date,
        }, headers={
            'Bearer': self.casting_director_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        Movie.query.get(data['created_id']).delete()

        #delete movie
        id = self.movie.id
        res = self.client().delete('/movies/' + str(id), headers={
            'Bearer': self.casting_director_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_executive_producer_authorized(self):
        res = client().get('/actors', headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)

        res = client().get('/movies', headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)

        # post actor
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        Actor.query().get(data['created_id'])

        # patch actor
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.test_name,
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        # delete actor
        id = self.actor.id
        res = self.client().delete('/actors/' + str(id), headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        #patch movie
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'title': self.test_name,
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        #post movie
        res = self.client().post('/movies', json={
            'title': self.test_title,
            'release_date': self.test_release_date,
        }, headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        Movie.query.get(data['created_id']).delete()

        #delete movie
        id = self.movie.id
        res = self.client().delete('/movies/' + str(id), headers={
            'Bearer': self.executive_producer_jwt
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()