import os
import logging

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABSE_URI'] = 'postgresql://localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
db = SQLAlchemy(app)

logger = logging.getLogger('graffiti')
hdlr = logging.FileHandler('log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

@app.route('/')
def hello():
    print 'Hello world I am running!'
    return 'Hello World!\n'

# Shortening path (i.e. hit this path when we want to shorten a new URL)
@app.route('/s')
def shorten():
    print 'Printing from the shortened path!'
    return 'URL shortening not yet available!\n'

# Redirection path (i.e. hit this path when we should be redirected by a shortened URL)
@app.route('/r/<shortened>')
def redirect(shortened):
    print 'Printing from the redirecting path! The parameter is %s' % shortened
    # Take shortened variable and look it up in the database
    # if (found_in_db) {
    #   redirect to the original URL
    # else
    #   return error message akin to url NOT_FOUND
    return 'URL redirecting for %s not yet available!\n' % shortened

@app.route('/initdb')
def init_db():
  db.session.commit()
  db.drop_all()
  db.create_all()
  return 'initted the DB\n'

@app.route('/cleardb')
def clear_db_of_everything():
  # Need this otherwise postgresql freezes
  db.session.commit()
  db.session.close_all()
  db.drop_all()
  return 'dropped\n'

class Url(db.Model):
  __tablename__ = 'urls'

  # Only alnum or _ in username. Between 3 and 25 chars inclusive
  original_url=db.Column(db.String, primary_key=True)
  shortened_path=db.Column(db.String, unique=True)
  creation_timestamp=db.Column(db.DateTime)

  def __init__(self, original, shortened):
    # TODO: Do some validation on the passed in values.
    self.original_url = original
    self.shortened_url = shortened 

@app.route('/addfake')
def add_fake():
  db.create_all()
  db.session.add(Url('http://www.google.com', 'shortened'))
  db.session.commit()
  return 'Added fake url\n'

logger.info(init_db())
logger.info(clear_db_of_everything())
