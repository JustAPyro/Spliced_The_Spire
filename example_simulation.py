from Battleground import Battleground
from Actors.CLIActor import Clipper
from Monsters.Sentry import Sentry
from Cards.RedDefend import RedDefend

cards = [  # Starting card deck
    "Strike", "Strike", "Strike", "Strike", "Strike",
    "Defend", "Defend", "Defend", "Defend",
    "Bash"
]

bg = Battleground(0)  # Create a battleground at ascension 0
bg.add_monster(Sentry(42))  # Add a sentry with 42 health
bg.add_actor(Clipper(cards))  # Add a CLI actor
print("====== Battle Start ======")
while not bg.battle_over():
    bg.next_round()
