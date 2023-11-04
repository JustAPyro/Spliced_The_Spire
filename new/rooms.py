from typing import List

from new.actors import AbstractActor
from new.enemies import AbstractEnemy
class EnemyRoom:
    def __init__(self, actor: AbstractActor, enemies: List[AbstractEnemy]):
        self.enemies = enemies
        self.turn = True

        self.actor = actor


    @property
    def state_object(self):
        return {
            'player': self.actor,
            'players_turn': self.turn,
            'enemies': self.enemies
        }

    @property
    def state_string(self):
        red = "\033[31m"
        green = "\033[32m"
        blue = "\033[34m"
        reset = "\033[39m"



        output = ''
        output += f'Player (H: {self.actor.health}/{self.actor.max_health} | E: {self.actor.max_energy}/{self.actor.energy})'
        output += f' with potions: [Empty], [Empty], [Empty]'

        # Print info about player hand
        output += '\nHand: ['+', '.join([f'({self.actor.hand.index(card)}) {red if card.energyCost > self.actor.energy else green}{card}{reset}' for card in self.actor.hand]) + ']'

        output += f'\nEnemies: '
        for enemy in self.enemies:
            output += f'\n{enemy.name} (H: {enemy.health}/{enemy.max_health}) with intent: {enemy.intent}'
        return output
