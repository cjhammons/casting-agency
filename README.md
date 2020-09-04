# casting-agency
An API that enables a movie production company to keep track of their movies and actors.

# Setup
### Dependencies
Dependencies can be installed with ``pip install -r requirements.txt``. The dependencies are a follows:

```
alembic==1.4.2
aniso8601==8.0.0
Babel==2.8.0
click==7.1.2
ecdsa==0.16.0
Flask==1.1.2
Flask-Cors==3.0.8
Flask-Migrate==2.5.3
Flask-RESTful==0.3.8
Flask-Script==2.0.6
Flask-SQLAlchemy==2.4.4
future==0.18.2
gunicorn==20.0.4
itsdangerous==1.1.0
Jinja2==2.11.2
jose==1.0.0
Mako==1.1.3
MarkupSafe==1.1.1
psycopg2-binary==2.8.5
pycryptodome==3.3.1
python-dateutil==2.8.1
python-editor==1.0.4
python-jose-cryptodome==1.3.2
pytz==2020.1
six==1.15.0
SQLAlchemy==1.3.19
Werkzeug==1.0.1
```

### How to run
Once the repo has been cloned, setup your environment variables as specified in ``setup.sh``. Your database vars will be different for your local machine, but FLASK_APP will be the same. Run the command ``flask run`` to run the application.

### Testing
Run command ``python3 test_app.py`` to run the unittests.


# Endpoints

## GET /actors 
Returns all actors currently in the database.

### Response

```
{
  "actors": [
    {
      "id": 1,
      "name": "Billy Bob",
      "age": 42,
      "gender": "Male
    }
  ],
  "success":true
}
```

## DELETE /actors/<id> 
Deletes a specified actor.

### Response

```
{
  "deleted": 1,
  "success": true
}
```

## POST /actors 
Creates a new actor
### Parameters
All actor fields are required
- ``name``
- ``age``
- ``gender``
### Response

```
{
  "success": true,
  "created_id": 1
}
```

## PATCH /actors 
Edits an actor's fields. 
### Parameters
All actor fields are required, even the ones that are not being changed.
- ``name``
- ``age``
` ``gender``
### Response

```
{
  "success": true,
  "actor": {
      "id": 1
      "name": "Billy Bob",
      "age": 42,
      "gender": "Male
   }
}
```

## GET /movies 
Returns all movies currently in the database.

### Response

```
{
  "movies": [
    {
      "id": 1
      "title": "The Thing From Outer Space!!"
      "releae_date": 1/1/2019
    }
  ],
  "success":true
}
```

## DELETE /movies/<id> 
Deletes a specified movie.

### Response

```
{
  "deleted": 1,
  "success": true
}
```

## POST /movies 
Creates a new movie
### Parameters
All actor fields are required
- ``title``
- ``release_date``
### Response

```
{
  "success": true,
  "created_id": 1
}
```

## PATCH /movies 
Edits an movies's fields. 
### Parameters
All movie fields are required, even the ones that are not being changed.
- ``title``
- ``release_date``
### Response

```
{
  "success": true,
  "movie": {
      "id": 1
      "title": "The Thing From Outer Space!!"
      "releae_date": 1/1/2019
   }
}
```

# Authorization
The API is secured using Auth0. There are 3 roles with the following permissions:

### Casting Assistant:
- view:actors
- view:movies

### Casting Director
 - All of Casting Assistant's permissions
 - add:actor
 - delete:actor
 - edit:actor
 
 ### Executive Producer
 - All of Casting Director's permissions
 - delete:movie
 - add:movie
 
 
 API calls are authenticated with a Bearer Token in the header. The file ``jwt.txt`` contains valid JWTs for a user of each role for testing.
 
 # Live API
 The API is currently  running at the following URL:
 ``https://cjhammons-casting-agency.herokuapp.com``
