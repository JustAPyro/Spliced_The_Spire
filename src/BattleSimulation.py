from Battleground import Battleground
from src.Actors.AbstractActor import AbstractActor


class BattleSimulation:
    def __init__(self,
                 actor: AbstractActor.__class__,
                 actor_health: int,
                 actor_deck: list,
                 monsters: list,
                 ascension: int):

        # Save information needed to create a bot
        self.actor = actor
        self.actor_health = actor_health
        self.actor_deck = actor_deck
        self.monsters = monsters
        self.ascension = ascension

    def simulate(self, quantity, verbose=False):
        # We're going to run this battle a few times
        for battle in range(quantity):
            print(f"Simulating battle {battle + 1}:")

            # Instantiate the actor (player/AI) and the enemies
            actor = self.actor(cards=self.actor_deck, max_health=self.actor_health)
            enemies = list(map(lambda enemy: enemy(ascension=self.ascension), self.monsters))

            # Create a battleground and insert actor and enemies into it
            bg = Battleground(actor=actor, enemies=enemies)
            print(bg.overview()) if verbose else None

            while not bg.battle_over():
                bg.next_round(verbose=verbose)

