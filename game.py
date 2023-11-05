from new.rooms import EnemyRoom
from new.enemies import Cultist, AbstractEnemy
from new.actors import PlayerActor, AbstractActor
from new.classes import Ironclad


class AI(AbstractActor):
    def __init__(self, clas):
        super().__init__(clas)

    def turn_logic(self, hand, enemies):
        return 'ended turn'


class LeftToRightAI(AbstractActor):
    def __init__(self, clas):
        super().__init__(clas)

    def turn_logic(self, hand, enemies):
        while self.energy > 0:
            choices = self.get_playable_cards()
            if len(choices) == 0:
                break
            self.use_card(enemies, choices[0])


class Simulation:
    def __init__(self, actor: type[AbstractActor], enemies: AbstractEnemy, hero, relics, deck, ascension):
        self.actor = actor(hero)
        self.enemies = enemies

    def run(self):
        print("Starting Simulation:")

        while self.actor.health > 0 and self.enemies.health > 0:
            turn_log = self.actor.turn_impl(self.actor.hand_pile, self.enemies)
            print(f'Actor drew {turn_log["initial_draw"]} and has {self.actor.health} health and {self.actor.energy} energy')
            for action in turn_log['turn_actions']:
                print(action['message'])

            print(f'Cultists turn! Health: {self.enemies.health}, effects: {self.enemies.effects}')
            turn = self.enemies.take_turn(self.actor)
            print(self.enemies.name, turn)

        if self.actor.health <= 0:
            print("Actor LOST")
        else:
            print("Actor WON")


sim = Simulation(actor=LeftToRightAI,
                 enemies=Cultist(),
                 hero=Ironclad,
                 relics=[Ironclad.start_relic],
                 deck=Ironclad.start_cards,
                 ascension=0)
sim.run()
