import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_url = os.getenv('DB_URL')
db_name = os.getenv('DB_NAME')
#database_path = "postgres://{}:{}@{}/{}".format(db_username, db_password, db_url, db_name)
database_path = db_url