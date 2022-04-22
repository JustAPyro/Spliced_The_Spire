from abc import ABCMeta
from src.Actors.AbstractActor import AbstractActor
import typing


class BattleSimulation:
    def __init__(self,
                 actor: AbstractActor.__class__,
                 actor_health: int,
                 actor_deck,
                 enemies: list):

        # Save information needed to create a bot
        self.actor = actor
        self.actor_health = actor_health
        self.actor_deck = actor_deck



