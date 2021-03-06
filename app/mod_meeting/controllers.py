from flask import Blueprint, request, jsonify

from app import app
from app import db
from app.mod_participate.models import Participate
from app.mod_meeting.models import Meeting
from app.mod_reference.models import Reference
from app.mod_auth.controllers import login_required

mod_meeting = Blueprint('meeting', __name__, url_prefix='/api/meetings')

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

def calculate_vote_slots(meeting):
  vote_slots = []
  for p in meeting.participates:
    for pv in p.vote_slots:
      found = 0
      for v in vote_slots:
        if pv['day'] == v['day'] and pv['hour'] == v['hour'] and pv['minute'] == v['minute']:
          v['count'] += 1
          found = 1
      if not found:
        vote_slots.append(pv)
        vote_slots[len(vote_slots) - 1]['count'] = 1
  return vote_slots

def caluculate_max_vote_slots(vote_slots):
  max_vote = 0
  for v in vote_slots:
    max_vote = max(v['count'], max_vote)
  return max_vote

@mod_meeting.route('/<hash_id>', methods=['GET'])
def meeting_show(hash_id):
  meeting = Meeting.query.get(Meeting.get_id(hash_id))
  vote_slots = calculate_vote_slots(meeting)
  meeting_serialize = meeting.serialized
  meeting_serialize['vote_slots'] = vote_slots
  meeting_serialize['max_vote'] = caluculate_max_vote_slots(vote_slots)

  return jsonify(meeting_serialize), 200

@mod_meeting.route('/<hash_id>', methods=['PATCH'])
@login_required
def meeting_update(current_user, hash_id):
  req = request.get_json(force=True)

  meeting = Meeting.query.get(Meeting.get_id(hash_id))

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  if meeting.host_id != current_user.id:
    return jsonify({'message': 'Forbidden (host_id not correct)'}), 403

  meeting.title = req['title']
  meeting.description = req['description']
  meeting.meeting_link = req['meeting_link']
  meeting.location = req['location']
  meeting.start_hour = int(req['start_hour'])
  meeting.end_hour = int(req['end_hour'])
  # TODO
  # meeting.final_slots=[]

  db.session.add(meeting)
  db.session.commit()

  return jsonify({'message': 'Success'}), 200

@mod_meeting.route('/<hash_id>', methods=['DELETE'])
@login_required
def meeting_destroy(current_user, hash_id):
  meeting = Meeting.query.get(Meeting.get_id(hash_id))

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  if meeting.host_id != current_user.id:
    return jsonify({'message': 'Forbidden (host_id not correct)'}), 403

  db.session.delete(meeting)
  db.session.commit()

  return jsonify({'message': 'Success'}), 200

# === handle participate relationship ===

@mod_meeting.route('/<hash_id>/participate', methods=['GET'])
@login_required
def meeting_participate_show(current_user, hash_id):
  meeting_id = Meeting.get_id(hash_id)

  meeting = Meeting.query.get(Meeting.get_id(hash_id))

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  participate = Participate.query.get((current_user.id, meeting_id))

  if participate:
    return jsonify({'participate': True, 'message': 'Already participated this meeting'}), 200

  return jsonify({'participate': False, 'message': 'Didn\'t participate'}), 200

@mod_meeting.route('/<hash_id>/participate', methods=['POST'])
@login_required
def meeting_participate_create(current_user, hash_id):
  meeting_id = Meeting.get_id(hash_id)

  meeting = Meeting.query.get(Meeting.get_id(hash_id))

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  participate = Participate.query.get((current_user.id, meeting_id))

  if participate:
    return jsonify({'message': 'Already participated this meeting'}), 400

  participate = Participate(user_id=current_user.id, meeting_id=meeting_id, vote_slots=[])
  db.session.add(participate)
  db.session.commit()

  return jsonify({'message': 'Success'}), 200

@mod_meeting.route('/<hash_id>/participate', methods=['DELETE'])
@login_required
def meeting_participate_destroy(current_user, hash_id):
  meeting_id = Meeting.get_id(hash_id)

  meeting = Meeting.query.get(Meeting.get_id(hash_id))

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  participate = Participate.query.get((current_user.id, meeting_id))

  if not participate:
    return jsonify({'message': 'Didn\'t participate'}), 400

  db.session.delete(participate)
  db.session.commit()

  return jsonify({'message': 'Success'}), 200

# === handle voting ===

@mod_meeting.route('/<hash_id>/vote', methods=['GET'])
@login_required
def meeting_vote_show(current_user, hash_id):
  meeting = Meeting.query.get(Meeting.get_id(hash_id))

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  participate = Participate.query.get((current_user.id, meeting.id))

  if not participate:
    return jsonify({'message': 'Didn\'t participate'}), 400

  return jsonify(participate.serialized), 200

@mod_meeting.route('/<hash_id>/vote', methods=['POST'])
@login_required
def meeting_vote(current_user, hash_id):
  req = request.get_json(force=True)
  meeting = Meeting.query.get(Meeting.get_id(hash_id))

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  participate = Participate.query.get((current_user.id, meeting.id))

  if not participate:
    return jsonify({'message': 'Didn\'t participate'}), 400

  participate.vote = False if len(req['vote_slots']) == 0 else True
  participate.vote_slots = req['vote_slots']

  db.session.add(participate)
  db.session.commit()

  return jsonify({'message': 'Success'}), 200

# === handle final voting ===

@mod_meeting.route('/<hash_id>/final_vote', methods=['GET'])
def meeting_final_vote_show(hash_id):
  meeting = Meeting.query.get(Meeting.get_id(hash_id))

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  return jsonify(meeting.final_slots), 200

@mod_meeting.route('/<hash_id>/final_vote', methods=['POST'])
@login_required
def meeting_final_vote(current_user, hash_id):
  req = request.get_json(force=True)
  meeting = Meeting.query.get(Meeting.get_id(hash_id))

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  meeting.final_slots = req['final_slots']

  db.session.add(meeting)
  db.session.commit()

  return jsonify({'message': 'Success'}), 200

# === handle references ===

@mod_meeting.route('/<hash_id>/references', methods=['GET'])
def meeting_reference(hash_id):
  meeting_id = Meeting.get_id(hash_id)
  meeting = Meeting.query.get(meeting_id)

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  references = [reference.serialized for reference in meeting.references]
  return jsonify(references), 200

@mod_meeting.route('/<hash_id>/references', methods=['POST'])
def meeting_reference_create(hash_id):
  meeting_id = Meeting.get_id(hash_id)
  meeting = Meeting.query.get(meeting_id)

  if not meeting:
    return jsonify({'message': 'Meeting not found'}), 404

  req = request.get_json(force=True)
  reference = Reference(meeting_id=meeting_id, title=req['title'], link=req['link'])

  db.session.add(reference)
  db.session.commit()

  return jsonify({'message': 'Success', 'id': reference.id}), 200
