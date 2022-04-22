import Classes.Ironclad
from BattleSimulation import BattleSimulation
from Actors.RandomActor import RandomActor
from Monsters import Cultist

sim = BattleSimulation(
    actor=RandomActor,  # The AI that will be deciding actions
    actor_health=Classes.Ironclad.starting_health,  # Player/AI Starting health
    actor_deck=Classes.Ironclad.starting_deck,      # Player/AI Starting deck
    monsters=[Cultist],   # Enemies to play against
    ascension=1           # Ascension level this will take place at
)

# Simulate one battle
sim.simulate(1, verbose=True)
