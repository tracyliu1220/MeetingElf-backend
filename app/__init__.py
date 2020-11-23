from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)
from app.mod_user.controllers import mod_user as user_module
app.register_blueprint(user_module)
from app.mod_meeting.controllers import mod_meeting as meeting_module
app.register_blueprint(meeting_module)

db.create_all()

@app.route('/', methods=['GET'])
def hello():
    return 'Hello Meetinelf!'
