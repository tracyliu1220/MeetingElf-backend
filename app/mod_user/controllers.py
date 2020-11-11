from flask import Blueprint, request, jsonify

from app import db
from app.mod_user.models import User
from app.mod_auth.controllers import login_required

mod_user = Blueprint('user', __name__, url_prefix='/users')

@mod_user.route('', methods=['GET'])
def user_index():
    users = [user.serialized for user in User.query.all()]
    return jsonify(users), 200

@mod_user.route('', methods=['POST'])
def user_create():
  req = request.get_json(force=True)

  user = User.query.filter_by(email=req['email']).first()

  # === request checking ===
  # email used
  if user:
    return jsonify({'message': 'This email has been used'}), 400
  # required fields
  if not req.keys() >= {'username', 'email', 'password'}:
    return jsonify({'message': 'Fields \'username\', \'email\' and \'password\' required'}), 400

  user = User(username=req['username'], email=req['email'])
  user.set_password(req['password'])

  db.session.add(user)
  db.session.commit()

  return jsonify({'message': 'Success'}), 200

@mod_user.route('/<id>', methods=['PATCH'])
@login_required
def user_update(current_user, id):
  if current_user.id != int(id):
    return jsonify({'message': 'Forbidden'}), 403

  if request.json.get('username'):
    current_user.username = request.json.get('username')
    db.session.commit()

  if request.json.get('old_password') and request.json.get('new_password'):
    if current_user.check_password(request.json.get('old_password')):
      current_user.set_password(request.json.get('new_password'))
      db.session.commit()
    else:
      return jsonify({'message': 'Old password does not match'}), 400

  return jsonify({'message': 'Success'}), 200
