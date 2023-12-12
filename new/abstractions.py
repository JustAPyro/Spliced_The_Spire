from __future__ import annotations

import random
from abc import abstractmethod, ABC
from copy import copy
from typing import Optional

import lutil
from lutil import C, asc_int
from new.cards import AbstractCard
from new.effects import EffectMixin
from new.enumerations import CardPiles, CardType, SelectEvent


class DamageMixin:
    """
    Adding this to a subclass will provide it with the ability to take, deal
    and manage damage.
    """

    def damage(self: AbstractEnemy, damage):
        self.get_actor().take_damage(damage, self)


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

    def receive_damage_from_card(self, damage: int, card: AbstractCard):
        self.health = self.health - damage
        self.process_effects('receive_damage_from_card', self.environment, card)

    def use_card(self, target: AbstractEnemy, card: AbstractCard, all_enemies: list[AbstractEnemy], is_free=False,
                 will_discard=True):
        if card not in self.hand_pile:
            raise RuntimeError("Tried to play card not in hand")
        if card.energy_cost == 'x':
            card.energy_cost = self.energy
        card.use(self, target, self.environment)

        # If enemy was killed call the on_fatal effect
        card.on_fatal(self)

        self.process_effects('on_card_play', self.environment, card)

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

    def heal(self, increase: int):
        self.health += increase

    def add_card_to_draw(self, card, shuffle=False):
        if shuffle:
            insert_at = random.randint(0, len(self.draw_pile))
            self.draw_pile.insert(insert_at, card)
        else:
            raise NotImplementedError

    def add_card_to_hand(self, card):
        self.card_piles[CardPiles.HAND].append(card)

    def add_card_to_exhaust(self, card):
        self.card_piles[CardPiles.DISCARD].append(card)

    def get_cards(self,
                  from_piles: CardPiles | list[CardPiles] = None,  # DRAW, HAND, DISCARD, EXHAUST | Default: All
                  with_types: CardType | list[CardType] = None,  # ATTACK, SKILL, POWER, STATUS, CURSE | Default: All
                  exclude_cards: AbstractCard | list[AbstractCard] = None):
        """
        Get a set of cards based on search criteria

        :param from_piles: Which card piles you want included in the search.
            (Options: DRAW, HAND, DISCARD, EXHAUST | Default: ALL)
        :param with_types: Which type of cards you want included in the search.
            (Options: ATTACK, SKILL, POWER, STATUS, CURSE | Default: ALL)
        :param exclude_cards: Specific cards that you want *excluded* from the search. (Default: NONE)
        """

        # 1. Default to using all options if none are specified
        # 2. If a singular option was provided auto-insert it into a list
        # 3. Fetch all the cards based on the options provided
        from_piles = CardPiles.all() if from_piles is None else from_piles
        from_piles = [from_piles] if type(from_piles) == CardPiles else from_piles
        valid_by_pile_cards = []
        for pile in from_piles:
            valid_by_pile_cards += self.card_piles.get(pile)

        # 1. Default to using all options if none are specified
        # 2. If a singular option was provided auto-insert it into a list
        # 3. Fetch all the cards based on the options provided
        with_types = CardType.all() if with_types is None else with_types
        with_types = [with_types] if type(with_types) == CardType else with_types
        valid_by_type_cards = [card for card in self.get_all_cards() if card.card_type in with_types]

        # 1. For exclude cards if none default to empty list
        # 2. Listify data
        exclude_cards = [] if exclude_cards is None else exclude_cards
        exclude_cards = [exclude_cards] if issubclass(type(exclude_cards), AbstractCard) else exclude_cards

        return (set(valid_by_type_cards) & set(valid_by_pile_cards)) - set(exclude_cards)

    def get_all_cards(self):
        cards = []
        for pile in self.card_piles.values():
            cards += pile
        return cards

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
            # TODO This logic doesn't seem right
            if (card.energy_cost == 'x'
                    or (self.energy >= card.energy_cost
                        and card.is_playable(self)
                        and not card.unplayable)):
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

        for card in (*self.hand_pile, *self.discard_pile, *self.draw_pile, *self._exhaust_pile):
            # If the card's energy has been modified temporarily
            if card.ex_energy_cost != -1:
                card.energy_cost = card.ex_energy_cost
                card.ex_energy_cost = -1

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

    def recover_card(self, card):
        if card not in self._exhaust_pile:
            raise RuntimeError('???')

        self._exhaust_pile.remove(card)
        self.hand_pile.append(card)

    def exhaust_card(self, card: AbstractCard):
        """Exhausts the selected card. If the card is not in the players hand, throws an error."""
        if card not in self.hand_pile:
            raise RuntimeError("Tried to exhaust card not in hand?")

        card.on_exhaust(self)

        self.hand_pile.remove(card)
        self._exhaust_pile.append(card)

    def draw_card(self, quantity: int = 1):
        """Draws quantity of cards, if the draw pile is empty it will auto shuffle and pull from discard."""
        modify_card_draw = self.process_effects('modify_card_draw', self.environment, quantity)
        if modify_card_draw is None:
            modify_card_draw = 0
        quantity = modify_card_draw

        # If it's turn 1 force innate cards to be drawn
        if len(self.turn_log) == 0:
            for card in [card for card in self.draw_pile if card.innate is True]:
                self.draw_pile.remove(card)
                self.hand_pile.append(card)
                quantity = quantity - 1

        for i in range(quantity):
            # If you can't draw cards
            if len(self.draw_pile) <= 0 and len(self.discard_pile) <= 0:
                return False
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
                  f'\nExhaust Pile: {self._exhaust_pile}'
                  f'\nEnergy: {self.energy}')

        return self.turn_log[-1]


class AbstractEnemy(ABC, EffectMixin, DamageMixin):
    """
    This class is an abstract class designed to streamline the implementation
    of enemies and elites.
    https://slay-the-spire.fandom.com/wiki/Monsters
    """

    def __init__(self,
                 name: Optional[str] = None,
                 max_health: dict[int, tuple[int, int]] | int | None = None,
                 set_health: Optional[int] = None,
                 ascension=0,
                 environment=None,
                 act=1):
        """
        Create an enemy.

        Parameters
        ----------
        :param name:
            The name of the enemy.
            Note that if this is not provided, the name of the enemy will be parsed from
            the class name.

        :param max_health:
            The creature's max_health. This can be provided in three formats. You can either declare it
            as a static class level variable, by adding a max_health map to the class (outside __init__/self), or
            you can pass it into the init function either as a map, or just as an int if you want to set it to a
            specific value.

        :param set_health:
            If specified will set the health of the creature to this amount.

        Exceptions
        ----------
        :raises RuntimeError:
            This will be thrown if max_health is not provided and the subclass does not
            implement its own static class "max_health" variable.
        """
        # Use the provided name if there is, otherwise parse it from class name
        self.name = name if name else lutil.parse_class_name(type(self).__name__)

        # Guard against people not providing a max_health anywhere
        if not max_health and not hasattr(self, 'max_health'):
            raise RuntimeError(f'Tried to call subclass AbstractEnemy without providing static max_health variable. '
                               f'Please verify that {type(self).__name__}.max_health is a defined value. '
                               f'You may also choose to provide it in the {type(self).__name__}.__init__ constructor.')

        # Assigns a max health based on the ascension and the class.max_health property
        self.max_health = asc_int(ascension, getattr(self, 'max_health'))

        # Since this was just created current health should be full
        self.health = set_health if set_health else self.max_health

        # Information about the environment that is relevant to the battle
        self.ascension = ascension
        self.act = act

        # Add self to the environment
        if environment:
            self.environment = environment
            self.environment['enemies'].append(self)

        # This stores the move pattern of the enemy,
        # It will populate with a generator the first time
        # that take_turn is called on this enemy
        self.ability_method_generator = self.pattern()

        # Track the history and stuffs
        self.log = []

        # Initialize the EffectMixin
        super().__init__()

    def get_actor(self) -> AbstractActor:
        return self.environment['actor']

    def is_dead(self):
        return self.health <= 0

    def take_damage(self, damage: int):
        damage = self.process_effects('modify_damage_taken', self.environment, damage)
        self.health -= damage

    def deal_damage(self, damage: int, target, log):
        damage = self.process_effects('modify_damage_dealt', self.environment, damage)
        log.append(f'used Dark Strike on {target.name} to deal {damage} damage.')
        target.take_damage(damage, self)

    @property
    def intent(self):
        return None

    @abstractmethod
    def pattern(self):
        raise NotImplementedError

    def rule_pattern(self, chances, successive_limit):
        # Get a list of the possible abilites bassed on successiveness?

        valid_abilities = []
        for ability in successive_limit:
            if successive_limit[ability] > len(self.log):
                valid_abilities.append(ability)
                continue

            for i in range(successive_limit[ability]):
                if (len(self.log) < type(self.log[-i]) == ability):
                    valid_abilities.append(type(self.log[-i]))

        # Then use chances to pick between them
        weights = []
        for ability in valid_abilities:
            weights.append(chances[ability])

        return random.choices(valid_abilities, weights)

    class Collector:
        def __init__(self):
            self.message = NotImplemented
            self.intent = NotImplemented

        def set_message(self, message: str):
            self.message = message

        def has_message(self):
            return self.message is not NotImplemented

        def set_intent(self, intent):
            self.intent = intent

        def has_intent(self):
            return self.intent is not NotImplemented

    @classmethod
    def ability(cls, func):
        """
        This is a decorator function. Decorators are kind of convoluted, but what
        actually happens here is that a Collector is created and passes injects two methods
        into the ability method (set_message and set_intent). If these are not used by the
        ability message it will throw an exception.
        """

        def ability_with_collector(*args, **kwargs):
            self = args[0]
            collector = AbstractEnemy.Collector()

            func(self, collector.set_message, collector.set_intent)

            # TODO: Clean up these guards
            if not collector.has_message() or not collector.has_intent():
                raise RuntimeError(f'{cls.__name__}.{func.__name__} implementation does not use the provided collector method set_message. '
                                   f'Please add a {func.__name__}(\'message\') to the implementation.')
            if not collector.has_intent():
                raise RuntimeError(
                    f'{cls.__name__}.{func.__name__} implementation does not use the provided collector method set_message. '
                    f'Please add a {func.__name__}(\'message\') to the implementation.')


        return ability_with_collector

    def take_turn(self, actor):
        log = []
        self.process_effects('on_start_turn', self.environment)
        next_method = next(self.ability_method_generator)
        self.log.append(next_method.__name__)
        next_method()
        self.process_effects('on_end_turn', self.environment)
        return log
