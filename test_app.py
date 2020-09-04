import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from src.database.models import setup_db, Actor, Movie

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
        self.executive_producer_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlA2cnVTOU40aU94U0htTDdrTTdYbiJ9.eyJpc3MiOiJodHRwczovL2NqaGFtbW9ucy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZWFmMTAyMDc2YTcwMDY3OGYxOGJmIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTkwODQ2ODEsImV4cCI6MTU5OTE3MTA3NSwiYXpwIjoidGxhSW5DSFBZOVRIdjN6SjhhRlV1d0IyTmEwUzYwWjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.ie_IgzTbLQLP8QZ3FYSRyISODcJDRvhfU1oo7l-H7b8V1Eft33RGAD7GQnigAre5UFkXpcySwfVj4n_9Gf0w48JVHsExLIz1RbHkbUIOFdAY_FNI0Io2uSP3l2zN5Nj_8W7DQn3hXkJdhLIdmw3xJG49d30MvQ0DjBzsZeHoU8xskZMR53n7Hr5QeXUmr7s5Uw76ULuFDVV8VKdRdfF07KzpDmYovm7P4MH7VKmt4kvOQ4SyTDE_sSQ2LR12Xx-n_gjFdNExMQxoQ1Z-P3hklz9qeMCqCKpcaf6s4V9BJ5Ht0YNUsAlb6t8AIosmci_5bH25s5-I8f4Fp76uEmwRJw'
        self.casting_assistant_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlA2cnVTOU40aU94U0htTDdrTTdYbiJ9.eyJpc3MiOiJodHRwczovL2NqaGFtbW9ucy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwZjZlMDA3MTQ2OGMwMDEzMDAzYTYyIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTkwODQ1NDcsImV4cCI6MTU5OTE3MDk0MSwiYXpwIjoidGxhSW5DSFBZOVRIdjN6SjhhRlV1d0IyTmEwUzYwWjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.NaTTHfMMJe5LKB2DJnSt5XIg45kVg00NjpSsuzcZ_85q1jSanCM2v5h5-RIF-ZftfJxdQc7DTd8ONIgH3ixkFOBtkmMpuEMgp0yLm2iyzk2MWciueFrv0KHaYSBua1nHVpoDqqwB7hDavfRmajGsZA3L6EzuLDBjGcVFgJSd6kLn0CTb3w2-sFx1DFt5Fhm4XE2cmUticDqWhcwk1JM3xFhZ5DQuOeTbikYxUjcLmjb1MVGKFOIyCI_r_BbsHdIxD7u0zsjRqdMXUEjBD8jva81ORBptm-JVez_bkMkaxxae4OcTDl_LaaNam2Fj2dUxUtK9XvOXSW66n6sbJbV99Q'
        self.casting_director_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlA2cnVTOU40aU94U0htTDdrTTdYbiJ9.eyJpc3MiOiJodHRwczovL2NqaGFtbW9ucy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwZTFiNTE2NTJlNWEwMDE5Y2U4MzFlIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1OTkwODQ2NDIsImV4cCI6MTU5OTE3MTAzNiwiYXpwIjoidGxhSW5DSFBZOVRIdjN6SjhhRlV1d0IyTmEwUzYwWjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImRlbGV0ZTphY3RvciIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.AkDb5xnqmVWB2ELym62y14-zWp2VsTcboYeaBrq_fu9VW_38FPQigGYZxfrw8rp2K2TNfS6CiyBrOKhtgNal0HMoB3fOxpSxSE3OHaP23hWLEGd5_RN5WFgXugsG70KY0nYU3I2_259t4INFK54g90wmkw8MH9owXmZ9lMZPn_fyHaYfExwUaecmyb3XR1R-9iUWOImEBbIUmkWUa9x2US7B9PLv34Hqcud0VoVPmmTQkhPcNaeP0bT80DEWTEtXrVu3y7puinE79Ukz0-m4jdZ4THkUFoaE57ymGhhrJzbyy1wSzWAF7M3Vx7S_hU_DQKRPSVrtUoMZ_yieFpM3bw'
        
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