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
    def __init__(self, actor, enemies: AbstractEnemy, hero, relics, deck, ascension):
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
            for i in range(5):
                if len(self.deck) == 0:
                    self.deck.extend(self.discard_pile)
                    self.actor.discard_pile.clear()


                self.hand.append(self.deck.pop())
            print(f'Actor drew {self.actor.hand} and has {self.actor.health} health and {self.actor.energy} energy')

            turn = self.actor.take_turn(self.actor.hand, self.enemies)
            print('Actor', turn)

            self.discard_pile.extend(self.actor.hand)
            self.hand.clear()

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
