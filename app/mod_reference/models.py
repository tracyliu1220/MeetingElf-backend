from app import app
from app import db
from app.utils.db_base import Base

class Reference(Base):
  meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))

  title = db.Column(db.String(120), unique=True, nullable=False)
  link = db.Column(db.String(300), unique=True, nullable=False)

  meeting = db.relationship('Meeting', foreign_keys=[meeting_id], back_populates='references')

  @property
  def serialized(self):
    return {
              'id': self.id,
              'title': self.title,
              'link': self.link
           }
