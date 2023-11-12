import random
from abc import abstractmethod

from new.enemies import AbstractEnemy
from new.cards import AbstractCard
from new.effects import EffectMixin
from copy import copy
from typing import TYPE_CHECKING
from lutil import C

if TYPE_CHECKING:
    from enemies import AbstractEnemy


class AbstractActor(EffectMixin):
    def __init__(self, clas, cards: list[AbstractCard] = None):
        super().__init__()
        self.name: str = "Actor"
        self.max_health: int = clas.health
        self.health: int = clas.health
        self.gold: int = 99
        # self.relics: list[AbstractRelics] = [clas.relic]
        self.max_energy: int = 3
        self.energy: int = 3

        self.draw_pile: list[AbstractCard] = (clas.start_cards if cards is None else cards)
        self.hand_pile: list[AbstractCard] = []
        self.discard_pile: list[AbstractCard] = []
        self._exhaust_pile: list[AbstractCard] = []

        # This log contains what the actor did each turn
        self.logging: bool = True
        self.turn_log = []

    def set_start(self, health, hand):
        # TODO: Assert start
        self.max_health = health
        self.health = health
        self.hand = hand
        return self

    def use_card(self, target: AbstractEnemy, card: AbstractCard, all_enemies: list[AbstractEnemy], is_free=False,
                 will_discard=True):
        if card not in self.hand_pile:
            raise RuntimeError("Tried to play card not in hand")
        card.use(self, target, all_enemies)
        if card in self.hand_pile and will_discard:
            self.discard_pile.append(card)
            self.hand_pile.remove(card)
        if not is_free:
            self.energy -= card.energy_cost
        if self.logging:
            self.turn_log[-1]['turn_actions'].append({
                'type': 'use_card',
                'card': card,
                'target': target,
                'message': f'{self.name} used {card.name} on {target.name}'
            })

    def get_hand(self):
        return self.hand_pile

    def get_playable_cards(self) -> list[AbstractCard]:
        playable = []
        for card in self.hand_pile:
            # TODO: This is a sketchy patch
            if card is None:
                continue
            if self.energy >= card.energy_cost and card.is_playable(self):
                playable.append(card)
        return playable

    def deal_damage(self, target, damage):
        actual_damage = self.process_effects('modify_damage_dealt', damage)
        target.take_damage(actual_damage)

    def take_damage(self, damage):
        actual_damage = self.process_effects('modify_damage_taken', damage)
        self.health -= actual_damage

    def end_turn(self):
        self.process_effects('on_end_turn')
        self.discard_pile.extend(self.hand_pile)
        self.hand_pile.clear()

    def start_turn(self, draw=None):
        self.energy = self.max_energy
        self.draw_card(5)
        self.turn_log.append({
            'initial_draw': tuple(self.hand_pile),
            'initial_energy': copy(self.energy),
            'initial_health': copy(self.health),
            'turn_actions': []
        })

        self.process_effects('on_start_turn')

    def exhaust_card(self, card: AbstractCard):
        """Exhausts the selected card. If the card is not in the players hand, throws an error."""
        if card not in self.hand_pile:
            raise RuntimeError("Tried to exhaust card not in hand?")

        self.hand_pile.remove(card)
        self._exhaust_pile.append(card)

    def draw_card(self, quantity: int):
        """Draws quantity of cards, if the draw pile is empty it will auto shuffle and pull from discard."""
        if len(self.draw_pile) == 0 and len(self.discard_pile) == 0:
            return False
        for i in range(quantity):
            if len(self.draw_pile) > 0:
                self.hand_pile.append(self.draw_pile.pop())
            elif len(self.discard_pile) > 0:
                self.draw_pile.extend(self.discard_pile)
                self.discard_pile.clear()
                random.shuffle(self.draw_pile)
                self.hand_pile.append(self.draw_pile.pop())
        return True

    @abstractmethod
    def turn_logic(self, hand: list[AbstractCard], enemies: list[AbstractEnemy]):
        pass

    @abstractmethod
    def select_card(self, options: list[AbstractCard]) -> AbstractCard:
        pass

    def turn_impl(self, hand: list[AbstractCard], enemies: list[AbstractEnemy], verbose: bool):
        self.start_turn()

        if verbose:
            log = self.turn_log[-1]
            print(f'{C.GREEN}Actor\'s turn:'
                  f'\n\t drew {log["initial_draw"]} '
                  f'\n\t has {log["initial_health"]} health / {log["initial_energy"]} energy'
                  f'\n\t these effects: {self.get_effects_dict()}'
                  f'\n\t Draw Pile: {self.draw_pile}'
                  f'\n\t Discard Pile: {self.discard_pile}')

        self.turn_logic(hand, enemies)

        if verbose:
            print(C.GREEN, end='')
            for action in self.turn_log[-1]['turn_actions']:
                print(action['message'])
            print(C.END, end='')

        self.end_turn()

        print(f'Effects after turn: {self.get_effects_dict()}')
        print(f'Draw Pile: {self.draw_pile}'
              f'\nDiscard Pile: {self.discard_pile}')

        return self.turn_log[-1]


class DummyActor(AbstractActor):
    def __init__(self, clas, cards, health, hand, energy):
        super().__init__(clas, cards=cards)
        self.health = health
        self.max_health = health

        self.energy = energy
        self.max_energy = energy

        self.hand_pile = hand

        self.logging = False


class LeftToRightAI(AbstractActor):
    def __init__(self, clas, cards):
        super().__init__(clas, cards=cards)

    def turn_logic(self, hand, enemies):

        # Pic
        choices = self.get_playable_cards()
        while len(choices) > 0:
            # Find a valid enemy with health remaining
            valid_enemy = None
            for enemy in enemies:
                if enemy.health > 0:
                    valid_enemy = enemy
                    break

            # ??? If no valid, end turn
            if not valid_enemy:
                break

            self.use_card(valid_enemy, choices[0], enemies)
            choices = self.get_playable_cards()

    def select_card(self, options: list[AbstractCard]) -> AbstractCard:
        return options[0]
