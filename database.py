
from flask_sqlalchemy import SQLAlchemy

import os

class Database:
    def __init__(self):
        self.app = None
        self.driver = None

    def init_app(self, app):
        self.app = app
        self.connect()
    
    def connect(self):
        db_pw = os.environ.get('DB_PW')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://crb_app:{pwd}@channel-response-bot.ci8o3fo3rwkf.us-east-1.rds.amazonaws.com:5432/crb".format(pwd=db_pw)
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(self.app)
        self.driver = db

    def get_db(self):
        if not self.driver:
            return self.connect()
        return self.driver
        

