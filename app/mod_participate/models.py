import datetime

import app
from app import db

class Participate(db.Model):
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)

  # user = db.relationship('User', backref=db.backref('participate', cascade='all, delete-orphan'))
  # meeting = db.relationship('Meeting', backref=db.backref('participate', cascade='all, delete-orphan'))

  user = db.relationship('User', foreign_keys=[user_id], back_populates='participates')
  meeting = db.relationship('Meeting', foreign_keys=[meeting_id], back_populates='participates')

  vote = db.Column(db.Boolean, default=False)
  vote_slots = db.Column(db.JSON)
  # vote_slots
  # {
  #    "day": 1,      // integer 1 ~ 7
  #    "hour": 13,    // integer 0 ~ 23
  #    "minute": 30,  // integer 0 ~ 59
  #    "date": null   // date or null
  # }

  date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

  @property
  def last_view():
    return datetime.datetime.utcnow()

  @property
  def serialized(self):
    return {
              'vote': self.vote,
              'vote_slots': self.vote_slots
           }

  @property
  def serialized_meeting(self):
    return {
              'vote': self.vote,
              'meeting': self.meeting.serialized
           }

  @property
  def serialized_user(self):
    return {
              'vote': self.vote,
              'user': self.user.serialized,
              'vote_slots': self.vote_slots
           }
