from flask import Blueprint, request, jsonify

from app import app
from app import db
from app.mod_participate.models import Participate
from app.mod_reference.models import Reference
from app.mod_auth.controllers import login_required

mod_reference = Blueprint('reference', __name__, url_prefix='/api/references')

@mod_reference.route('', methods=['GET'])
def reference_index():
    references = [reference.serialized for reference in Reference.query.all()]
    return jsonify(references), 200

@mod_reference.route('/<id>', methods=['GET'])
def reference_show(id):
    reference = Reference.query.get(int(id))

    if not reference:
      return jsonify({'message': 'Reference not found'}), 404

    return jsonify(reference.serialized), 200

@mod_reference.route('/<id>', methods=['PATCH'])
@login_required
def reference_update(current_user, id):
    reference = Reference.query.get(int(id))

    if not reference:
      return jsonify({'message': 'Reference not found'}), 404

    participate = Participate.query.get((current_user.id, reference.meeting.id))

    if not participate:
      return jsonify({'message': 'Haven\'t participate in this meeting'}), 200

    req = request.get_json(force=True)
    reference.title = req['title']
    reference.link = req['link']

    db.session.add(reference)
    db.session.commit()

    return jsonify({'message': 'Success'}), 200

@mod_reference.route('/<id>', methods=['DELETE'])
@login_required
def reference_destroy(current_user, id):
    reference = Reference.query.get(int(id))

    if not reference:
      return jsonify({'message': 'Reference not found'}), 404

    participate = Participate.query.get((current_user.id, reference.meeting.id))

    if not participate:
      return jsonify({'message': 'Haven\'t participate in this meeting'}), 200

    db.session.delete(reference)
    db.session.commit()

    return jsonify({'message': 'Success'}), 200
