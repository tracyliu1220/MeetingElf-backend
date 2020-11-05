from werkzeug.security import check_password_hash, generate_password_hash

import app
from app import db
from app.utils.db_base import Base

class User(Base):
  # id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=False, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(128))

  def set_password(self, plaintext):
    self.password = generate_password_hash(plaintext)

  def check_password(self, candidate):
    return check_password_hash(self.password, candidate)

  def __repr__(self):
    return '<User %r>' % self.username

  @property
  def serialized(self):
    return {
              'id': self.id,
              'username': self.username,
              'email': self.email
           }
