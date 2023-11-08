from new.cards import *
from new.enemies import Cultist, AbstractEnemy
from new.actors import AbstractActor, LeftToRightAI
from new.classes import Ironclad
from lutil import C


class Simulation:
    def __init__(self, actor: type[AbstractActor], enemies: AbstractEnemy, hero, relics, deck, ascension):
        self.actor = actor(hero, cards=deck)
        self.enemies = enemies

    def run(self):
        print("Starting Simulation:")
        print(f'Fighting {self.enemies.name} with {self.enemies.health} health')
        while self.actor.health > 0 and self.enemies.health > 0:
            turn_log = self.actor.turn_impl(self.actor.hand_pile, self.enemies, verbose=True)

            if self.enemies.health <= 0:
                break

            print(f'{C.RED}Cultists turn! Health: {self.enemies.health}, effects: {self.enemies.get_effects_dict()}')
            turn = self.enemies.take_turn(self.actor)
            print(f'{C.RED}{self.enemies.name} {turn}{C.END}')

        if self.actor.health <= 0:
            print("Actor LOST")
        else:
            print("Actor WON")


sim = Simulation(actor=LeftToRightAI,
                 enemies=Cultist(),
                 hero=Ironclad,
                 relics=[Ironclad.start_relic],
                 deck=[RedDefend(), RedDefend(), Armaments(), Armaments(), Armaments(), Anger(), BodySlam()],
                 ascension=0)
sim.run()
