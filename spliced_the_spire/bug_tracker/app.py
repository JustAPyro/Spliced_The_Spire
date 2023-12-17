import json
from enum import Enum

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from spliced_the_spire.new.enemies import enemies
from bug_enums import BugStatus, BugType, BugLocation

data_base_name = 'pyredevelopment$spliced_the_spire'
database_location = 'pyredevelopment.mysql.pythonanywhere-services.com'
database_username = 'pyredevelopment'
database_password = 'stssqlpassword'

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="pyredevelopment",
    password="stssqlpassword",
    hostname="pyredevelopment.mysql.pythonanywhere-services.com",
    databasename="pyredevelopment$spliced_the_spire",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class SplicedBugs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    tagged_by = db.Column(db.String(100), unique=False, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    location = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    last_modified = db.Column(db.DateTime(timezone=True), server_default=func.now())
    notes = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/register/room/monster", methods=['GET', 'POST'])
def router():
    name = 'something'
    description = f'Could not locate implementation of enemy {name}. This was reported in the following room/act: 1.2/1'
    reporter = 'Luke'
    room_data = json.loads(request.data.decode())
    bug = SplicedBugs(
        title='Missing or misnamed monster "{name}"',
        tagged_by=f'AUTO-TAGGER ({reporter})',
        type=BugType.MISSING,
        location=BugLocation.MONSTERS,
        status=BugStatus.OPEN,
        description=description
    )
    db.session.add(bug)
    db.session.commit()

    return "Hi!"
