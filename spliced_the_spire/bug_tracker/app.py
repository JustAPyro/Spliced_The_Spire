import json
from enum import Enum

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from spliced_the_spire.new.enemies import enemies

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


class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bug_title = db.Column(db.String(100), unique=True, nullable=False)
    bug_type = db.Column(db.Integer, nullable=False)
    bug_location = db.Column(db.Integer, nullable=False)
    bug_status = db.Column(db.Integer, unique=True, nullable=False)
    bug_name = db.Column(db.String(100), nullable=False)
    bug_description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    notes = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/register/monster_room", methods=['GET', 'POST'])
def router():
    room_data = json.loads(request.data.decode())
    print(room_data)
    monsters = room_data['monsters']
    for monster in monsters:
        enemy_klass = enemies.get(monster['name'])
        if not enemy_klass:
            print(f'COULD NOT FIND CLASS FOR ENEMY NAME: {monster["name"]}')

    print(map)
    return "Hi!"
