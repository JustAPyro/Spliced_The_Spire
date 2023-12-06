import itertools
import random
from abc import abstractmethod

from new.enemies import AbstractEnemy
from new.enumerations import SelectEvent, CardPiles, CardType
from new.cards import AbstractCard
from new.effects import EffectMixin
from copy import copy
from typing import TYPE_CHECKING
from lutil import C

if TYPE_CHECKING:
    from enemies import AbstractEnemy


class AbstractActor(EffectMixin):
    def __init__(self, clas, environment, cards: list[AbstractCard] = None):
        super().__init__()
        self.times_received_damage: int = 0
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

        self.card_piles = {
            CardPiles.DRAW: self.draw_pile,
            CardPiles.HAND: self.hand_pile,
            CardPiles.DISCARD: self.discard_pile,
            CardPiles.EXHAUST: self._exhaust_pile
        }

        # This log contains what the actor did each turn
        self.logging: bool = True
        self.turn_log = []

        # Save the environment to class and add self to it
        self.environment = environment
        self.environment['actor'] = self

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
        card.use(self, target, self.environment)
        # If card.exhaust:
        # Do exhaust logic

        # Exhaust Card logic
        if card in self.hand_pile and card.exhaust:
            self.exhaust_card(card)
            self.process_effects('on_card_exhaust', self.environment)
        # Poof card logic (powers)
        elif card.poof:
            self.hand_pile.remove(card)
        elif card in self.hand_pile and will_discard:
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

    def add_card_to_draw(self, card, shuffle=False):
        if shuffle:
            insert_at = random.randint(0, len(self.draw_pile))
            self.draw_pile.insert(insert_at, card)
        else:
            raise NotImplementedError

    def add_card_to_hand(self, card):
        self.card_piles[CardPiles.HAND].append(card)

    def get_cards(self, from_piles: list[CardPiles], card_types: list[CardType]):
        # TODO: Might be broken? Investigate Duel Wield
        valid_from_piles = set(itertools.chain([self.card_piles.get(pile) for pile in from_piles]))
        valid_card_types = set([card for card in self.get_all_cards() if card.card_type in card_types])
        return valid_from_piles & valid_card_types

    def get_all_cards(self):
        return set[itertools.chain(self.card_piles.values())]

    def get_hand_without(self, card):
        pile = list(self.hand_pile)
        pile.remove(card)
        return pile

    def get_hand(self):
        return self.hand_pile

    def get_playable_cards(self) -> list[AbstractCard]:
        playable = []
        for card in self.hand_pile:
            # TODO: This is a sketchy patch
            if card is None:
                continue
            # TODO: We need some environment dict thingie
            if self.energy >= card.cost(self) and card.is_playable(self):
                playable.append(card)
        return playable

    def deal_damage(self, target, damage):
        actual_damage = self.process_effects('modify_damage_dealt', self.environment, damage)
        target.take_damage(actual_damage)

    def take_damage(self, damage, damaging_enemy):
        actual_damage = self.process_effects('modify_damage_taken', self.environment, damage)
        self.health -= actual_damage
        if actual_damage > 0:
            self.times_received_damage += 1
            self.process_effects('on_take_damage', self.environment, damaging_enemy)

    def end_turn(self):
        self.process_effects('on_end_turn', self.environment)
        for card in self.hand_pile:
            if card.ethereal:
                self.exhaust_card(card)
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
        self.process_effects('on_start_turn', self.environment)

    def exhaust_card(self, card: AbstractCard):
        """Exhausts the selected card. If the card is not in the players hand, throws an error."""
        if card not in self.hand_pile:
            raise RuntimeError("Tried to exhaust card not in hand?")

        self.hand_pile.remove(card)
        self._exhaust_pile.append(card)

    def draw_card(self, quantity: int = 1):
        """Draws quantity of cards, if the draw pile is empty it will auto shuffle and pull from discard."""
        modify_card_draw = self.process_effects('modify_card_draw', self.environment, quantity)
        if modify_card_draw is None:
            modify_card_draw = 0
        quantity = modify_card_draw
        if len(self.draw_pile) == 0 and len(self.discard_pile) == 0:
            return False
        for i in range(quantity):
            # If we have cards in discard but not in draw, shuffle discard into draw
            if len(self.draw_pile) <= 0 < len(self.discard_pile):
                self.draw_pile.extend(self.discard_pile)
                self.discard_pile.clear()
                random.shuffle(self.draw_pile)
            # Draw a card
            card = self.draw_pile.pop()
            self.hand_pile.append(card)
            # Process effects related to card draw
            self.process_effects('on_card_draw', self.environment, card)
        return True

    @abstractmethod
    def turn_logic(self):
        pass

    @abstractmethod
    def select_card(self, options: list[AbstractCard], event_type: SelectEvent) -> AbstractCard:
        pass

    def gain_energy(self, qty=1):
        self.energy = self.energy + qty

    def get_combat_deck(self):
        return set().union(self.draw_pile, self.hand_pile, self.discard_pile)

    def turn_impl(self, verbose: bool):
        self.start_turn()

        if verbose:
            log = self.turn_log[-1]
            print(f'{C.GREEN}Actor\'s turn:'
                  f'\n\t drew {log["initial_draw"]} '
                  f'\n\t has {log["initial_health"]} health / {log["initial_energy"]} energy'
                  f'\n\t these effects: {self.get_effects_dict()}'
                  f'\n\t Draw Pile: {self.draw_pile}'
                  f'\n\t Discard Pile: {self.discard_pile}')

        self.turn_logic()

        if verbose:
            print(C.GREEN, end='')
            for action in self.turn_log[-1]['turn_actions']:
                print(action['message'])
            print(C.END, end='')

        self.end_turn()

        if verbose:
            print(f'Effects after turn: {self.get_effects_dict()}')
            print(f'Draw Pile: {self.draw_pile}'
                  f'\nDiscard Pile: {self.discard_pile}'
                  f'\nExhaust Pile: {self._exhaust_pile}')

        return self.turn_log[-1]


class DummyActor(AbstractActor):
    def __init__(self, clas, cards, health, hand, energy, environment):
        super().__init__(clas, cards=cards, environment=environment)
        self.health = health
        self.max_health = health

        self.energy = energy
        self.max_energy = energy

        self.hand_pile = hand
        self.environment = environment

        self.logging = False


class LeftToRightAI(AbstractActor):
    def __init__(self, clas, environment, cards):
        super().__init__(clas, environment, cards=cards)

    def turn_logic(self):

        # Pic
        choices = self.get_playable_cards()
        while len(choices) > 0:
            # Find a valid enemy with health remaining
            valid_enemy = None
            for enemy in self.environment['enemies']:
                if enemy.health > 0:
                    valid_enemy = enemy
                    break

            # ??? If no valid, end turn
            if not valid_enemy:
                break

            self.use_card(valid_enemy, choices[0], self.environment['enemies'])
            choices = self.get_playable_cards()

    def select_card(self, options: list[AbstractCard], event_type: SelectEvent) -> AbstractCard:
        return options[0]
