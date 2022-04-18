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
ex = {
    3: lambda: print("Test3"),
    4: lambda: print("Test4"),
    5: lambda: print("Test5")
}
action =ex[3]
action()

