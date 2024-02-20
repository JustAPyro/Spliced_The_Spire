from new.cards import *
from new.enemies import Cultist, JawWorm
from new.actors import LeftToRightAI
from new.abstractions import AbstractActor, AbstractEnemy
from new.classes import Ironclad
from lutil import C


class Simulation:
    def __init__(self, actor: type[AbstractActor], enemies, hero, relics, deck, ascension):
        self.environment = {'enemies': []}
        self.actor = actor(hero, self.environment, cards=deck)

        # Instantiate the enemies from the provided classes
        for enemy_class in enemies:
            enemy = enemy_class(self.environment)
            enemy.set_actor(self.actor)

        self.enemies = self.environment['enemies']

    def run(self):
        print("Starting Simulation:")
        print(f'Fighting {self.get_names()} with {self.get_healths()} health')
        print(f'Starting draw order: {self.actor.draw_pile}')
        while self.actor.health > 0:

            self.actor.turn_impl(verbose=True)

            if self.enemies_dead():
                break

            print(f'{C.RED}Enemy turn!')
            for enemy in self.enemies:
                print(f'{enemy.name}\'s turn. \n{enemy.name} has {enemy.health} health'
                      f' and the following effects: {enemy.get_effects_dict()}')

                log = enemy.take_turn()
                print(f'{log[-1]}')

        if self.actor.health <= 0:
            print("Actor LOST")
        else:
            print("Actor WON")

    def enemies_dead(self):
        for enemy in self.enemies:
            if enemy.health > 0:
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
                 enemies=[JawWorm],
                 hero=Ironclad,
                 relics=[],
                 deck=[RedDefend(), RedDefend(), RedStrike(), RedDefend()
                       ],
                 ascension=0)
sim.run()