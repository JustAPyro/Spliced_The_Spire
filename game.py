from new.rooms import EnemyRoom
from new.enemies import Cultist, AbstractEnemy
from new.actors import PlayerActor, AbstractActor
from new.classes import Ironclad


class AI(AbstractActor):
    def __init__(self, clas):
        super().__init__(clas)
        self.energy = 3

    def take_turn(self, hand, enemies):
        return 'ended turn'


class Simulation:
    def __init__(self, actor: type[AbstractActor], enemies: AbstractEnemy, hero, relics, deck, ascension):
        self.actor = actor(hero)
        self.deck = deck
        self.hand = []
        self.discard_pile = []
        self.enemies = enemies
        # Player draws cards
        # Takes actions
        # Enemy takes actions
        # repeat

    def run(self):
        print("Starting Simulation:")

        while self.actor.health > 0 and self.enemies.health > 0:

            self.actor.draw(5)
            print(f'Actor drew {self.actor.hand_pile} and has {self.actor.health} health and {self.actor.energy} energy')

            turn = self.actor.take_turn(self.actor.hand_pile, self.enemies)
            print('Actor', turn)

            self.actor.discard_pile.extend(self.actor.hand_pile)
            self.actor.hand_pile.clear()

            print(f'Cultists turn! Health: {self.enemies.health}, effects: {self.enemies.effects}')
            turn=self.enemies.take_turn(self.actor)
            print(self.enemies.name, turn)


        if self.actor.health <= 0:
            print("Actor LOST")
        else:
            print("Actor WON")




sim = Simulation(actor=AI,
                 enemies=Cultist(),
                 hero=Ironclad,
                 relics=[Ironclad.start_relic],
                 deck=Ironclad.start_cards,
                 ascension=0)
sim.run()
