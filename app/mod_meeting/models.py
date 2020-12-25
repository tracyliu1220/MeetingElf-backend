import jwt
import binascii
from Crypto.Cipher import DES

from app import app
from app import db
from app.utils.db_base import Base
from app.mod_participate.models import Participate
from app.mod_user.models import User

class Meeting(Base):
  host_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  host = db.relationship('User', foreign_keys=[host_id], back_populates='host_meetings')
  participates = db.relationship('Participate', back_populates='meeting', cascade="all, delete-orphan")
  references = db.relationship('Reference', back_populates='meeting', cascade="all, delete-orphan")

  title = db.Column(db.String(100), nullable=False)
  mode = db.Column(db.String(15), default='weekly')
  description = db.Column(db.String(1000))
  meeting_link = db.Column(db.String(100))
  location = db.Column(db.String(100))

  start_hour = db.Column(db.Integer)
  end_hour = db.Column(db.Integer)

  final_slots = db.Column(db.JSON)

  # final_slots
  # {
  #    "day": 1,      // integer 1 ~ 7
  #    "hour": 13,    // integer 0 ~ 23
  #    "minute": 30,  // integer 0 ~ 59
  #    "date": null   // date or null
  # }

  @property
  def hash_id(self):
    des = DES.new(app.config['MEETING_HASH_KEY'], DES.MODE_ECB)
    plain = str(self.id)
    plain = (16 - len(plain)) * '0' + plain
    enc = des.encrypt(plain.encode())
    enc = binascii.hexlify(enc).decode().upper()
    return enc

  @staticmethod
  def get_id(hash_id):
    des = DES.new(app.config['MEETING_HASH_KEY'], DES.MODE_ECB)
    try:
      dec = binascii.unhexlify(hash_id.lower().encode())
      dec = des.decrypt(dec).decode()
      id = int(dec)
    except:
      return None
    return id

  @property
  def serialized(self):
    return {
              'hash_id': self.hash_id,
              'title': self.title,
              'mode': self.mode,
              'host': self.host.serialized,
              'description': self.description,
              'meeting_link': self.meeting_link,
              'location': self.location,
              'final_slots': self.final_slots
           }
