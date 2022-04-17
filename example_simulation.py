from Battleground import Battleground
from Monsters.Sentry import Sentry
from Actors.ComaActor import ComaAI

cards = [  # Starting card deck
    "Strike", "Strike", "Strike", "Strike", "Strike",
    "Defend", "Defend", "Defend", "Defend",
    "Bash"
]

bg = Battleground(0)  # Create a battleground at ascension 0
bg.add_monster(Sentry(42))  # Add a sentry with 42 health
bg.add_actor(ComaAI(cards))  # Add a CLI actor
bg.add_monster(Sentry(health=None, attack_first=True))  # Add a sentry with 42 health
print("====== Battle Start ======")
while not bg.battle_over():
    bg.next_round()
