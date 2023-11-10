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

        self._draw_pile: list[AbstractCard] = (clas.start_cards if cards is None else cards)
        self._hand_pile: list[AbstractCard] = []
        self._discard_pile: list[AbstractCard] = []
        self._exhaust_pile: list[AbstractCard] = []

        # This log contains what the actor did each turn
        self.turn_log = []

    def use_card(self, target: AbstractEnemy, card: AbstractCard, all_enemies: list[AbstractEnemy]):
        if card in self.get_hand():
            self.discard_card(card)
        else:
            raise RuntimeError('Attempted to use card not in hand!')

        self.energy -= card.energy_cost
        card.use(self, target, all_enemies)
        self.turn_log[-1]['turn_actions'].append({
            'type': 'use_card',
            'card': card,
            'target': target,
            'message': f'{self.name} used {card.name} on {target.name}'
        })

    def get_playable_cards(self) -> list[AbstractCard]:
        playable = []
        for card in self.get_hand():
            # TODO: This is a sketchy patch
            if card is None:
                continue
            if self.energy >= card.energy_cost and card.is_playable(self):
                playable.append(card)
        return playable

    def deal_damage(self, target, damage):
        for effect in self.effects.values():
            modification = effect.modify_damage_dealt(damage)
            if modification:
                damage = damage + modification
        target.take_damage(damage)

    def take_damage(self, damage):
        for effect in self.effects.values():
            modification = effect.modify_damage_taken(damage)
            damage = damage + modification
        self.health -= damage

    def end_turn(self):
        self.process_effects('on_end_turn')
        self.discard_hand()

    def start_turn(self, draw=None):
        self.energy = self.max_energy
        random.shuffle(self._draw_pile)
        self.draw_card(5)
        self.turn_log.append({
            'initial_draw': tuple(self.get_hand()),
            'initial_energy': copy(self.energy),
            'initial_health': copy(self.health),
            'turn_actions': []
        })
        for effect in self.effects.values():
            effect.on_start_turn(self)  # TODO Add this to enemies

    @abstractmethod
    def turn_logic(self, hand: list[AbstractCard], enemies: list[AbstractEnemy]):
        pass

    def turn_impl(self, hand: list[AbstractCard], enemies: list[AbstractEnemy], verbose: bool):
        self.start_turn()

        if verbose:
            log = self.turn_log[-1]
            print(f'{C.GREEN}Actor\'s turn:'
                  f'\n\t drew {log["initial_draw"]} '
                  f'\n\t has {log["initial_health"]} health / {log["initial_energy"]} energy'
                  f'\n\t these effects: {self.get_effects_dict()}'
                  f'\n\t Draw Pile: {self.get_draw()}'
                  f'\n\t Discard Pile: {self.get_discard()}')

        self.turn_logic(hand, enemies)

        if verbose:
            print(C.GREEN, end='')
            for action in self.turn_log[-1]['turn_actions']:
                print(action['message'])
            print(C.END, end='')

        self.end_turn()

        print(f'Effects after turn: {self.get_effects_dict()}')

        return self.turn_log[-1]

    # API METHODS
    def get_draw(self) -> list[AbstractCard]:
        """Returns all the cards currently in the players draw pile."""
        return self._draw_pile

    def get_hand(self) -> list[AbstractCard]:
        """Returns all the cards currently in the players hand."""
        return self._hand_pile

    def draw_card(self, quantity: int = 1) -> AbstractCard:
        """
        Draws quantity of cards, if the draw pile is empty it will auto shuffle and pull from discard.
        If card quantity is not specified this will draw 1 card.
        This will return the card that is drawn.
        """
        for i in range(quantity):
            card = None
            # If we can draw a card just do that
            if len(self._draw_pile) > 0:
                card = self._draw_pile.pop()
                self._hand_pile.append(card)
            # If we don't but have draw but have discard shuffle and draw
            elif len(self._discard_pile) > 0:
                self._draw_pile.extend(self._discard_pile)
                self._discard_pile.clear()
                random.shuffle(self._draw_pile)
                card = self._draw_pile.pop()
                self._hand_pile.append(card)
            else:  # If we still can't, something weird is up. Throw an error for investigation
                raise RuntimeWarning('Tried to draw a card but had none in draw and none in discard pile.')
            return card

    def get_discard(self) -> list[AbstractCard]:
        """Returns all the cards currently in the players discard pile."""
        return self._discard_pile

    def discard_card(self, card: AbstractCard):
        """
        This method allows you to discard a card. This will move it from your hand
        to the discard pile without expending energy or initiating any of its use effects.
        """
        self._discard_pile.append(card)
        self._hand_pile.remove(card)

    def discard_hand(self):
        """
        Discard your entire hand. This is the same discard that is used on end of turn,
        All the players cards will be moved to the discard pile.
        """
        for card in self._hand_pile:
            self.discard_card(card)

    def exhaust_card(self, card: AbstractCard):
        """
        This method allows you to exhaust a card. This moves it to the exhaust pile
        without expending energy or initiating any of its use effects.
        If the card is not in your hand this will throw a runtime error.
        """
        # First make sure we have the card
        if card not in self._hand_pile:
            raise RuntimeError("Tried to exhaust card not in hand?")

        # Then move it to the exhaust pile
        self._hand_pile.remove(card)
        self._exhaust_pile.append(card)


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
