from flask import Blueprint, request, jsonify

from app import app
from app import db
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
    return jsonify(reference.serialized), 200

@mod_reference.route('/<id>', methods=['PATCH'])
def reference_update(id):
    req = request.get_json(force=True)

    reference = Reference.query.get(int(id))
    reference.title = req['title']
    reference.link = req['link']

    db.session.add(reference)
    db.session.commit()

    return jsonify({'message': 'Success'}), 200
