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
