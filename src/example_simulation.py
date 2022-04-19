from Battleground import Battleground
from Actors.ComaActor import ComaAI
from Monsters import JawWorm

"""
cards = [  # Starting card deck
    "Strike", "Strike", "Strike", "Strike", "Strike",
    "Defend", "Defend", "Defend", "Defend",
    "Bash"
]

bg = Battleground(ascension=0)  # Create a battleground at ascension 0
bg.add_actor(ComaAI(cards, 72))  # Add a CLI actor
bg.add_monster(JawWorm())  # Add a sentry with 42 health

print("====== Battle Start ======")
while not bg.battle_over():
    bg.next_round()
"""


def fizz():
    print("fizz")


def buss():
    print("buzz")


li = [("%100", 1), ("%5", -1), ("%10", -5), ("%2", 10)]
li.sort(key=lambda x: int(x[0].replace("%", "")))

print(li)
