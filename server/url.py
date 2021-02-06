from datetime import datetime
from main import db

class Url(db.Model):
  __tablename__ = 'urls'

  # Only alnum or _ in username. Between 3 and 25 characters inclusive
  original_url=db.Column(db.String, primary_key=True)
  shortened_path=db.Column(db.String, unique=True)
  creation_timestamp=db.Column(db.DateTime)

  def __init__(self, original, shortened):
    # TODO: Do some validation on the passed in values.
    self.original_url = original
    self.shortened_path = shortened
    self.creation_timestamp=datetime.now()

  def ToString(self):
    return "original_url: " + self.original_url + ", shortened_path: " + self.shortened_path + ", creation_timestamp: " + self.creation_timestamp.strftime("%m/%d/%Y, %H:%M:%S")

  def getShortenedPath(self):
    return self.shortened_path
  
  def getOriginalPath(self):
    return self.original_url