import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_url = os.getenv('DB_URL')
db_name = os.getenv('DB_NAME')
database_path = "postgres://{}:{}@{}/{}".format(db_username, db_password, db_url, db_name)
#database_path = db_url

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, refresh=False):
    print("Connecting to ", database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
    if refresh:
        db.drop_all()

    db.create_all()


class Actor(db.Model):
    __tablename__='actors'
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    '''
    format()
        representation of the Actor model
    '''
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

class Movie(db.Model):
    __tablename__='movies'
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    release_date = Column(String)


    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    format()
        representation of the Movie model
    '''
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


