#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import datetime
import os
import json

# Connect to postgresql database specified by the DATABASE_URL env var
db = SQLAlchemy()
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
    migrate = Migrate(app, db)

'''
Surf Spot / Surf Location
'''
class SurfLocation(db.Model):
  __tablename__ = 'surf_location'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String)
  city = Column(db.String)
  state = Column(db.String)
  country = Column(db.String)
  wave_type = Column(db.String)
  contests = db.relationship(
    'surf_contest',
    backref='surf_spot',
    lazy=True
  )

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'city': self.city,
      'state': self.state,
      'country': self.country,
      'wave_type': self.wave_type}

'''
Surf Contests
'''
class SurfContest(db.Model):
  __tablename__ = 'surf_contest'

  id = db.Column(db.Integer, primary_key=True)
  contestName = db.Column(db.String, nullable=False)
  contestDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
  # Foreign key reference to this contest's surf spot/location/venue
  surfSpotId = db.Column(
    db.Integer,
    db.ForeignKey('SurfLocation.id'),
    nullable=False)
  surfers = db.relationship(
    'Surfer', secondary=surf_contests, backref=db.backref('contests', lazy=True)
  )

  def __init__(self, name, date, spotId):
    self.contestName = name
    self.contestDate = date
    self.surfSpotId = spotId

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'contest_date': self.contestDate
      'contest_name': self.contestName
    }

'''
Surfers
'''
class Surfer(db.Model):
  __tablename__ = 'surfer'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  age = db.Column(db.Integer)
  stance = db.Column(db.String, nullable=False, default="Regular")
  hometown = db.Column(db.String, nullable=False)
  ranking = db.Column(db.Integer)

  def __init__(self, name, age, stance, hometown, ranking):
    self.name = name
    self.age = age
    self.stance = stance
    self.hometown = hometown
    self.ranking = ranking

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'surfer_name': self.name
      'surfer_age': self.age
      'surfer_stance': self.stance
      'surfer_hometown': self.hometown
      'surfer_ranking': self.ranking
    }