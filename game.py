from new.cards import *
from new.enemies import Cultist, AbstractEnemy
from new.actors import AbstractActor, LeftToRightAI
from new.classes import Ironclad
from lutil import C


class Simulation:
    def __init__(self, actor: type[AbstractActor], enemies: list[AbstractEnemy], hero, relics, deck, ascension):
        self.actor = actor(hero, cards=deck)
        self.enemies = enemies

    def run(self):
        print("Starting Simulation:")
        print(f'Fighting {self.get_names()} with {self.get_healths()} health')
        while self.actor.health > 0:
            turn_log = self.actor.turn_impl(self.actor.hand_pile, self.enemies, verbose=True)

            if self.enemies_dead():
                break

            print(f'{C.RED}Cultists turn! Health: {self.get_healths()}, effects: {self.enemies.get_effects_dict()}')
            turn = self.enemies.take_turn(self.actor)
            print(f'{C.RED}{self.get_names()} {turn}{C.END}')

        if self.actor.health <= 0:
            print("Actor LOST")
        else:
            print("Actor WON")

    def enemies_dead(self):
        for enemy in self.enemies:
            if enemy.health >= 0:
                return False
        return True

    def get_names(self):
        names = []
        for enemy in self.enemies:
            names.append(enemy.name)
        return names

    def get_healths(self):
        healths = []
        for enemy in self.enemies:
            healths.append(enemy.health)
        return healths


sim = Simulation(actor=LeftToRightAI,
                 enemies=[Cultist(), Cultist()],
                 hero=Ironclad,
                 relics=[Ironclad.start_relic],
                 deck=[RedDefend(), Clash(), Clash(), RedStrike(), RedStrike(), RedStrike()],
                 ascension=0)
sim.run()
