from flask import Blueprint, request, jsonify
from Crypto.Cipher import DES

from app import app
from app import db
from app.mod_meeting.models import Meeting
from app.mod_auth.controllers import login_required

mod_meeting = Blueprint('meeting', __name__, url_prefix='/meetings')

des = DES.new(app.config['MEETING_HASH_KEY'], DES.MODE_ECB)

@mod_meeting.route('', methods=['GET'])
def meeting_index():
    meetings = [meeting.serialized(des) for meeting in Meeting.query.all()]
    return jsonify(meetings), 200
