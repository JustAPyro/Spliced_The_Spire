from Battleground import Battleground
from Actors.ComaActor import ComaAI
from Monsters import JawWorm
from Monsters import Cultist

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

for i in range(20):
    print(f"A5 Cultist generated with {Cultist(5).max_health} health.")
