from new.cards import Anger, RedDefend, BodySlam
from new.enemies import Cultist, AbstractEnemy
from new.actors import PlayerActor, AbstractActor
from new.classes import Ironclad
from lutil import C


class AI(AbstractActor):
    def __init__(self, clas, cards):
        super().__init__(clas, cards=cards)

    def turn_logic(self, hand, enemies):
        return 'ended turn'


class LeftToRightAI(AbstractActor):
    def __init__(self, clas, cards):
        super().__init__(clas, cards=cards)

    def turn_logic(self, hand, enemies):
        while self.energy > 0:
            choices = self.get_playable_cards()
            if len(choices) == 0:
                break
            self.use_card(enemies, choices[0])


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
                 deck=[RedDefend(), RedDefend(), RedDefend(), RedDefend(), RedDefend()],
                 ascension=0)
sim.run()
