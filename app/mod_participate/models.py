import datetime

import app
from app import db
from app.utils.db_base import Base
# from app.mod_user.models import User
# from app.mod_meeting.models import Meeting

class Participate(Base):
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))

  user = db.relationship('User', backref=db.backref('participate', cascade='all, delete-orphan'))
  meeting = db.relationship('Meeting', backref=db.backref('participate', cascade='all, delete-orphan'))

  vote = db.Column(db.Boolean)
  vote_slots = db.Column(db.JSON)
  # vote_slots
  # {
  #    "day": 1,      // integer 1 ~ 7
  #    "hour": 13,    // integer 0 ~ 23
  #    "minute": 30,  // integer 0 ~ 59
  #    "date": null   // date or null
  # }

  @property
  def last_view():
    return datetime.datetime.utcnow()
