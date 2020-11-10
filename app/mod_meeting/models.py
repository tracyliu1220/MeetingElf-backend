import jwt
import binascii

import app
from app import db
from app.utils.db_base import Base
from app.mod_participate.models import Participate
# from app.config import MEETING_HASH_KEY

# des = DES.new(MEETING_HASH_KEY, DES.MODE_ECB)

class Meeting(Base):
  host_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  host = db.relationship('User', foreign_keys=[host_id], back_populates='host_meetings')
  users = db.relationship('User', secondary='participate')

  title = db.Column(db.String(100), nullable=False)
  mode = db.Column(db.String(15), nullable=False)
  description = db.Column(db.String(1000))
  meeting_link = db.Column(db.String(100))
  location = db.Column(db.String(100))
  final_slots = db.Column(db.JSON)

  # final_slots
  # {
  #    "day": 1,      // integer 1 ~ 7
  #    "hour": 13,    // integer 0 ~ 23
  #    "minute": 30,  // integer 0 ~ 59
  #    "date": null   // date or null
  # }

  def hash_id(self, des):
    plain = str(self.id)
    plain = (16 - len(plain)) * '0' + plain # padding to 32
    enc = des.encrypt(plain.encode())
    enc = binascii.hexlify(enc).decode().upper()
    return enc

  @staticmethod
  def get_id(des, hash_id):
    try:
      dec = binascii.unhexlify(hash_id.lower().encode())
      dec = des.decrypt(dec).decode()
      id = int(dec)
    except:
      return None
    return id

  def serialized(self, des):
    return {
              'hash_id': self.hash_id(des),
              'title': self.title,
              'mode': self.mode,
              'host': self.host.serialized,
              'description': self.description,
              'meeting_link': self.meeting_link,
              'location': self.location,
              'final_slots': self.final_slots
           }
