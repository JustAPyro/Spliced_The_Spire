from flask import Flask
from flask import request


from spliced_the_spire.new.enemies import *
from spliced_the_spire.new.abstractions import AbstractEnemy

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/register/monster_room", methods=['GET', 'POST'])
def router():
    room_data = request.data.decode()
    monsters = room_data['monsters']

    AbstractEnemy()


    print(map)
    return "Hi!"
