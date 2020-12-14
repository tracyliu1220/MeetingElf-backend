from flask import Blueprint, request, jsonify

from app import app
from app import db
from app.mod_participate.models import Participate
from app.mod_meeting.models import Meeting
from app.mod_auth.controllers import login_required

mod_meeting = Blueprint('meeting', __name__, url_prefix='/meetings')

@mod_meeting.route('', methods=['GET'])
def meeting_index():
    meetings = [meeting.serialized for meeting in Meeting.query.all()]
    return jsonify(meetings), 200

@mod_meeting.route('', methods=['POST'])
@login_required
def meeting_create(current_user):
  req = request.get_json(force=True)

  meeting = Meeting(
              host_id=current_user.id,
              title=req['title'],
              description=req['description'],
              meeting_link=req['meeting_link'],
              location=req['location'],
              start_hour=int(req['start_hour']),
              end_hour=int(req['end_hour']),
              final_slots=[]
  )
  db.session.add(meeting)
  db.session.commit()

  participate = Participate(user_id=current_user.id, meeting_id=meeting.id, vote_slots=[])
  db.session.add(participate)
  db.session.commit()

  return jsonify({'hash_id': meeting.hash_id, 'message': 'Success'}), 200
