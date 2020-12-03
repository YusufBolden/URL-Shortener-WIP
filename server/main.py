import os
import logging

from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Move to config.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

# Move to db.py
db = SQLAlchemy(app)

# Import is down here because db must be initialized.
from url import Url

logger = logging.getLogger('url_shortener')
hdlr = logging.FileHandler('log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

# Move APIs to separate files based no the API functionality.
@app.route('/')
def hello():
    print('Hello world I am running!')
    return 'Hello World!\n'

# Shortening path (i.e. hit this path when we want to shorten a new URL)
@app.route('/s/<original>')
def shorten(original):
    db.create_all()
    # Look it up in the DB.
    url = db.session.query(Url).filter(Url.original_url==original).first()
    # if (found in DB) { return already shortened URL }
    if url is not None:
        return url.getShortenedPath()
    # otherwise, create a shortened url (probably via some hash function)
    short_url = hash(original)
    # store it in the DB
    db.session.add(Url(original, str(short_url)))
    db.session.commit()
    # return the shortened URL to the user 
    return str(short_url)

# Redirection path (i.e. hit this path when we should be redirected by a shortened URL)
@app.route('/r/<shortened>')
def redirect(shortened):
    db.create_all()
    # print('Printing from the redirecting path! The parameter is %s') % shortened
    # Take shortened variable and look it up in the database
    short_url = db.session.query(Url).filter(Url.shortened_path==shortened).first()
    # if (found_in_db) {
    if short_url is not None:
        # redirect to the original URL
      return short_url.getOriginalPath()
    return 'URL not found!'

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

FAKE_ORIGINAL_URL='http://www.google.com'

@app.route('/addfake')
def add_fake():
  db.create_all()
  db.session.add(Url(FAKE_ORIGINAL_URL, 'shortened'))
  db.session.commit()
  return 'Added fake url\n'

@app.route('/showfake')
def show_fake():
  db.create_all()
  url = db.session.query(Url).filter(Url.original_url==FAKE_ORIGINAL_URL).first()
  if url is None:
    return "No Url with the original_url " + FAKE_ORIGINAL_URL + " was found."
  
  return url.ToString()

@app.route('/showcolumn')
def show_column_description():
  return str(db.session.query(Url).column_descriptions)

logger.info(init_db())
logger.info(clear_db_of_everything())
