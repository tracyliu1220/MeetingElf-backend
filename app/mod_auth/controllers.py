from flask import Blueprint, request, jsonify, make_response
import jwt
from functools import wraps
import time

from app import app
from app import db
from app.mod_user.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.cookies.get('token')
    if not token:
        return jsonify({'message': 'Token not found'}), 401

    try:
      data = jwt.decode(token, app.config['JWT_SECRET_KEY'])
      current_user = User.query.get(data['user_id'])
    except:
      return jsonify({'message': 'Token is invalid'}), 401

    if not current_user:
      return jsonify({'message': 'Token is invalid'}), 401

    return f(current_user, *args, **kwargs)
  return decorated

@mod_auth.route('login', methods=['POST'])
def auth_login():
  req = request.get_json(force=True)

  if not 'email' in req.keys() or not 'password' in req.keys():
    return jsonify({'message': 'Could not verify'}), 401

  user = User.query.filter_by(email=req['email']).first()

  if not user:
    return jsonify({'message': 'User does not exist'}), 401

  if not user.check_password(req['password']):
    return jsonify({'message': 'Password incorrect'}), 403

  token = jwt.encode({'user_id': user.id}, app.config['JWT_SECRET_KEY'])

  res = make_response({'id': user.id, 'message': 'Success'}, 200)
  res.set_cookie(key='token', value=token, expires=time.time()+300)

  return res
