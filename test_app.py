import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Actor, Movie

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.db_username = os.getenv('DATABASE_USERNAME')
        self.db_password = os.getenv('DATABASE_PASSWORD')
        self.db_url = os.getenv('DATABASE_URL')
        self.db_name = os.getenv('DATABASE_NAME')
        self.database_path = "postgres://{}:{}@{}/{}".format(self.db_username, self.db_password, self.db_url, self.db_name)
        
        #Current JWTs 3:11 pm PDT 9/2/2020
        self.executive_producer_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlA2cnVTOU40aU94U0htTDdrTTdYbiJ9.eyJpc3MiOiJodHRwczovL2NqaGFtbW9ucy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZWFmMTAyMDc2YTcwMDY3OGYxOGJmIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTkxODg2NDQsImV4cCI6MTU5OTI3NTAzOCwiYXpwIjoidGxhSW5DSFBZOVRIdjN6SjhhRlV1d0IyTmEwUzYwWjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.bLjw1E9Be1ofB9bW6UZzTujzt_bMRecMLvaLnd5TkWCW21UmMIewSvzJBjlLeI6EXnmJUNadPq3Q0shsA6jhCjrUKMwKQLlhEfzHGY4nB1Wn4dyNLdVufNNYNGR8PM3ioWorEftBJx1GZvwmZ4w3bien16dlLVo9Q-q4v6r2oFRC6rxKsj7oXuxqeGLI1BCI4P-C9XdMoGIZq45NEMKRJeIFdYZm_Hqr-KKmgS_so-MBpR317bbKWbLXodpbsG6XPhAZkkQDeu2NAagDhgQemU3zxAEXn2u-RWlCC5d6xrpVm9WA-8-Zo_jjpVzWsGtXS_pDcYQHPSttld4S9fn35w'
        self.casting_assistant_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlA2cnVTOU40aU94U0htTDdrTTdYbiJ9.eyJpc3MiOiJodHRwczovL2NqaGFtbW9ucy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwZjZlMDA3MTQ2OGMwMDEzMDAzYTYyIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTkxODkxMTgsImV4cCI6MTU5OTI3NTUxMiwiYXpwIjoidGxhSW5DSFBZOVRIdjN6SjhhRlV1d0IyTmEwUzYwWjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.jfUlS0CMHanvDQlcCcP2Nm6vjLpPOyVwqc4-12jsMHm9wuRoobWHjlQrMaKt2YTHMNk6f9OdpaLT_8eJ-Zi4FffxUW3BDQBAbNraVcvX_j8V9_JUjZXt5oUkLDJfDVJ-D2HiADByxLet3L83YvGhj9GYJzF6Atdip2MUNWkU-f8MhJfhJckov4jYHbx-0yYGLhu837oc8DQR6gxryJEJMnvffZWZE_hV9x5s0s8iUigWn9LNsEuy7jeAsumUtrnuJzBWDztIg85JMKA8owoHcE0m9LY5OEs_MhoN2UlnG9UISJP4VNgBwHx_rsqwRJBfbvjQZz6-Bu2su-blhwvuDg'
        self.casting_director_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlA2cnVTOU40aU94U0htTDdrTTdYbiJ9.eyJpc3MiOiJodHRwczovL2NqaGFtbW9ucy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwZTFiNTE2NTJlNWEwMDE5Y2U4MzFlIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTkxODg3NzQsImV4cCI6MTU5OTI3NTE2OCwiYXpwIjoidGxhSW5DSFBZOVRIdjN6SjhhRlV1d0IyTmEwUzYwWjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImRlbGV0ZTphY3RvciIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.gjU9Z9OxapcrsBtx-CTeDO6f_Kw3f1BQFDvlmYOEhv10KTaliLsPPqfUzU6Lu5hzoKWu9Rw0QGEiUmFgDgrS2SCcdRVMxYwy2qKYcFgfY3ie-xit-lEFCWnmnimGXSdwWZj_k6shIFdhC3mK-QRaN8H7N_dnnO-PJ3bmjpYlbda-VDPkuvSKhEDe8ECofzkZ3frPqvQN6evTvHz0pGGE7XybDSx1ydegHuMOGBY_d3-NiVENwPilXLmTYpFGE7sBO5nz74142arYYBdmyHjFooJGEbXqVrHYTlTjomSposAFeO3W0g8MnixGJQTVcjHNuHDYtbCPdFUBdOQtU56ERg'
        
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
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

       
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))


    '''
    DELETE /actors tests
    '''

    def test_delete_actors_success(self):
        id = self.actor.id
        res = self.client().delete('/actors/' + str(id), headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)
        self.assertEqual(Actor.query.get(id), None)

    def test_delete_actors_failure(self):
        id = -1
        res = self.client().delete('/actors/' + str(id), headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 404)

        data = json.loads(res.data)

        self.assertEqual(data['success'], False)

    '''
    POST /actors tests
    '''

    def test_post_actors_success(self):
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        
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
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)

        
        self.assertEqual(data['success'], False)

    def test_post_actors_failure_no_age(self):
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'gender': self.test_gender
        }, headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)

        
        self.assertEqual(data['success'], False)

    def test_post_actors_failure_no_age(self):
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'gender': self.test_gender
        }, headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)

        
        self.assertEqual(data['success'], False)

    '''
    PATCH /actors tests
    '''

    def test_patch_actors_success_name(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.test_name,
            'age':self.actor.age,
            'gender':self.actor.gender
        }, headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)        
        self.assertEqual(data['success'], True)
        self.assertEqual(Actor.query.get(self.actor.id).name, self.test_name)


    def test_patch_actors_success_age(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.test_name,
            'age':self.test_age,
            'gender':self.actor.gender
         }, headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)   
        self.assertEqual(data['success'], True)
        self.assertEqual(Actor.query.get(self.actor.id).age, self.test_age)


    def test_patch_actors_success_gender(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.actor.name,
            'age':self.actor.age,
            'gender':self.test_gender
         }, headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)        
        self.assertEqual(data['success'], True)
        self.assertEqual(Actor.query.get(self.actor.id).gender, self.test_gender)

    def test_patch_actors_failure_bad_input(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'meme':'rawr XD'
         }, headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 422)

    def test_patch_actors_failure_bad_id(self):
        id = -1
        res = self.client().patch('/actors/' + str(id), json={
            'gender': self.test_gender
         }, headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)

        
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
        res = self.client().get('/movies', headers={
             "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))


    '''
    DELETE /movies tests
    '''
    def test_delete_movies_success(self):
        id = self.movie.id
        res = self.client().delete('/movies/' + str(id), headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)
        self.assertEqual(Movie.query.get(id), None)

    def test_delete_movies_failure(self):
        id = -1
        res = self.client().delete('/movies/' + str(id), headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)

        
        self.assertEqual(data['success'], False)

    '''
    POST /movies tests
    '''
    def test_post_movies_success(self):
        res = self.client().post('/movies', json={
            'title': self.test_title,
            'release_date': self.test_release_date,
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])

        new_movie = Movie.query.get(data['created_id'])
        self.assertEqual(new_movie.title, self.test_title)
        self.assertEqual(new_movie.release_date, self.test_release_date)

        new_movie.delete()

    def test_post_movies_failure_no_title(self):
        res = self.client().post('/movies', json={
            'release_date': self.test_release_date,
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })    
        self.assertEqual(res.status_code, 422)

    def test_post_movies_failure_no_release_date(self):
        res = self.client().post('/movies', json={
            'title': self.test_title,
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)        
        self.assertEqual(data['success'], False)

    '''
    PATCH /movies tests
    '''
    def test_patch_movies_success_title(self):
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'title': self.test_title,
            'release_date':self.movie.release_date
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        
        self.assertEqual(data['success'], True)
        self.assertEqual(Movie.query.get(self.movie.id).title, self.test_title)

    def test_patch_movies_success_release_date(self):
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'title': self.movie.title,
            'release_date': self.test_release_date,
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['release_date'], self.test_release_date)

    def test_patch_movies_failure_bad_input(self):
        id = self.movie.id
        res = self.client().patch('/actors/' + str(id), json={
            'memes': 'WOLOLOLOLOLOL'
         }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })


        self.assertTrue(res.status_code, 422)

    def test_patch_movies_failure_bad_id(self):
        id = -1
        res = self.client().patch('/actors/' + str(id), json={
            'release_date': self.test_release_date,
         }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], False)

    '''
    -------------------------------------------------------------------------------------------------------------
                                            Role Tests
    -------------------------------------------------------------------------------------------------------------
    '''

    def test_casting_assistant_authorized_get_actors(self):
        res = self.client().get('/actors', headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        

    def test_casting_assistant_authorized_get_movies(self):
        res = self.client().get('/movies', headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
        })
        self.assertTrue(res.status_code, 200)

    def test_casting_assistant_unauthorized_post_actor(self):
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
        })
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_unauthorized_patch_actor(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.test_name,
            'gender':self.test_gender,
            'age': self.test_age
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
        })
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_unauthorized_delete_actor(self):
        id = self.actor.id
        res = self.client().delete('/actors/' + str(id), headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
        })
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_unauthorized_post_movie(self):
        res = self.client().post('/movies', json={
            'title': self.test_title,
            'release_date': self.test_release_date,
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
        })
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_unauthorized_patch_movie(self):
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'title': self.test_name,
            'release_date': self.test_release_date
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
        })
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant_unauthorized_delete_movie(self):
        id = self.movie.id
        res = self.client().delete('/movies/' + str(id), headers={
            'Bearer': self.casting_assistant_jwt
        })
        self.assertEqual(res.status_code, 401)

    def test_casting_director_authorized(self):
        res = self.client().get('/actors', headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        self.assertTrue(res.status_code, 200)

    def test_casting_director_authorized_get_movies(self):
        res = self.client().get('/movies', headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        self.assertTrue(res.status_code, 200)

    def test_casting_director_authorized_post_actor(self):
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        self.assertEqual(res.status_code, 200)

    def test_casting_director_authorized_patch_actor(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.test_name,
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        self.assertEqual(res.status_code, 200)

    def test_casting_director_authorized_delete_actor(self):
        id = self.actor.id
        res = self.client().delete('/actors/' + str(id), headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        self.assertEqual(res.status_code, 200)

    def test_casting_director_authorized_patch_movie(self):
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'title': self.test_name,
            'release_date': self.test_release_date
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        self.assertEqual(res.status_code, 200)

    def test_casting_director_unauthorized_post_movie(self):
        res = self.client().post('/movies', json={
            'title': self.test_title,
            'release_date': self.test_release_date,
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        self.assertEqual(res.status_code, 401)

    def test_casting_director_unauthorized_delete_movie(self):
        id = self.movie.id
        res = self.client().delete('/movies/' + str(id), headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        self.assertEqual(res.status_code, 401)

    def test_executive_producer_authorized_get_actors(self):
        res = self.client().get('/actors', headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertTrue(res.status_code, 200)

    def test_executive_producer_authorized_get_movies(self):
        res = self.client().get('/movies', headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertTrue(res.status_code, 200)

    def test_executive_producer_authorized_post_actor(self):
        res = self.client().post('/actors', json={
            'name': self.test_name,
            'age': self.test_age,
            'gender': self.test_gender
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)

    def test_executive_producer_authorized_patch_actor(self):
        id = self.actor.id
        res = self.client().patch('/actors/' + str(id), json={
            'name': self.test_name,
            'age': self.test_age,
            'gender':self.test_gender
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
    
    def test_executive_producer_authorized_delete_actor(self):
        id = self.actor.id
        res = self.client().delete('/actors/' + str(id), headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)

    def test_executive_producer_authorized_patch_movie(self):
        id = self.movie.id
        res = self.client().patch('/movies/' + str(id), json={
            'title': self.test_name,
            'release_date': self.test_release_date
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)
        

    def test_executive_producer_authorized_post_movie(self):
        res = self.client().post('/movies', json={
            'title': self.test_title,
            'release_date': self.test_release_date,
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)

    def test_executive_producer_authorized_delete_motie(self):
        id = self.movie.id
        res = self.client().delete('/movies/' + str(id), headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()