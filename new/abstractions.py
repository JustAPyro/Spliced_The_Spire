from __future__ import annotations

import random
from abc import abstractmethod, ABC
from copy import copy

from lutil import C
from new.cards import NO_COST
from new.effects import EffectMixin
from new.enemies import AbstractEnemy
from new.enumerations import CardPiles, CardType, SelectEvent, CardColor, CardRarity


class DamageMixin:
    """
    Adding this to a subclass will provide it with the ability to take, deal
    and manage damage.
    """
    def damage(self, target):
        pass


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
        self.card_piles[CardPiles.EXHAUST].append(card)

    def discard_card(self, card):
        self.card_piles[CardPiles.DISCARD].append(card)
        self.card_piles[CardPiles.HAND].remove(card)

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


class AbstractCard(ABC):
    """
    Abstract card class is the blueprint for all cards. The goal for this class
    is to allow simple, quick implementation of Slay the Spire cards. To use write an implementation
    for a card, write a class that inherits this class as well as ABC, then implement an __init__,
    use, and upgrade_logic methods.
    """

    def __init__(self,
                 card_type: CardType = CardType.UNKNOWN,
                 card_color: CardColor = CardColor.UNKNOWN,
                 card_rarity: CardRarity = CardRarity.UNKNOWN,
                 energy_cost: int | bool = NO_COST,
                 upgraded: bool = False,
                 name: str = None,
                 exhaust: bool = False,
                 ethereal: bool = False,
                 innate: bool = False,
                 unplayable: bool = False,
                 remove_after_combat: bool = False,
                 allow_multiple_upgrades: bool = False):
        """
        Primarily designed tobe called in subclassed cards.

        Parameters
        ----------
        :param card_type:
            The type of the card created. Options: ATTACK, SKILL, POWER, STATUS, CURSE

        :param energy_cost:
            The amount of energy the card uses, with two exceptions:
            True is a stand-in for x cost cards, which will be set to all energy available when played.
            False is a stand-in for cards that have no cost, mostly curse or status cards.
            '
        :param upgraded:
            If the card has been upgraded or not. Not that Searing Blow can be upgraded multiple times.

        :param name:
            The name of the card.

        :param exhaust:
            If the card should be exhausted when played. (Sent to exhaust pile and not shuffled back in deck)

        :param ethereal:
            If the card is ethereal (card will exhaust if it's in your hand at end of turn).

        :param innate:
            If the card is innate (card will always be drawn turn 1)

        :param unplayable:
            Sets the card to unplayable. Note that this will OVERRIDE the is_playable method.

        :param allow_multiple_upgrades:
            If the card can be upgraded multiple times (Example: Searing blow)

        """
        # If name is not provided then it will be parsed from subclass name
        if name is None:
            class_name = type(self).__name__
            final_name = ''

            for char in class_name:
                if char.isupper():
                    final_name += ' '
                final_name += char
            self.name: str = final_name[1:]
        else:
            self.name: str = name

        # normal energy cost of card ("cost" int)
        self.energy_cost: int = energy_cost

        # old cost of the card if the cost is ever changed temporarily (For example, card costs 0 this turn)
        self.ex_energy_cost: int = -1

        # If the card is innate or not
        self.innate: bool = innate

        # If the card is upgraded or not
        self.upgraded: bool = upgraded

        # Type of card
        self.card_type: CardType = card_type

        # Card behavior
        self.exhaust: bool = exhaust
        self.ethereal: bool = ethereal
        self.unplayable: bool = unplayable
        self.poof: bool = False

        # Allows the card to be upgraded multiple times (Searing blow)
        self.allow_multiple_upgrades = allow_multiple_upgrades

        # Setup for power type cards
        if self.card_type is CardType.POWER:
            self.poof = True
            if self.exhaust or self.ethereal:
                raise RuntimeError('WAT? (Power card with exhaust/ethereal found)')

    @abstractmethod
    def use(self, caller: 'AbstractActor', target: 'AbstractEnemy', environment):
        """
        * You are REQUIRED to implement this method in subclasses. *
        Overriding this method provides the default behavior of a card.

        Parameters
        ----------
        :param caller:
            The player using the card.

        :param target:
            The target of the card, if applicable.

        :param environment:
            The environment the card was played in, including all enemies in the room.
        """
        pass

    @abstractmethod
    def upgrade_logic(self):
        """
        * You are REQUIRED to implement this method in subclasses. *
        Overriding this method defines the behavior change when a card is upgraded.
        """
        pass

    def is_playable(self, caller: 'AbstractActor'):
        """
        * You may OPTIONALLY implement this method. *
        Overriding this method defines when a subclassed card may be playable.

        parameters
        ----------
        caller: new.abstractions.AbstractActor
            The player using the card.
        """
        return True

    # Only for cards that have an effect when they're exhausted by other cards
    def on_exhaust(self, caller: 'AbstractActor'):
        """
        * You may OPTIONALLY implement this method. *
        Overriding this method defines an effect that will be triggered on the card's exhaustion.
        This is -ONLY- for cards that have an effect when they're exhausted by other cards.

        Parameters
        ----------
        :param caller: AbstractActor
                The player using the card.
        """

    def on_fatal(self, caller):
        """
        * You may OPTIONALLY implement this method. *
        Overriding this method defines behavior that occurs if the card successfully kills an enemy.

        Parameters
        ----------
        :param caller: AbstractActor
                The player using the card.
        """
        pass

    # --- Card Sandbox Method API ---
    # These are methods that can be called during the implementations of cards using self.method_name()
    # They are mostly utility methods that allow implementations to be more readable and concise.

    def modify_cost_this_turn(self, cost: int):
        """
        Modifies the cost of the card only for this turn.

        Parameters
        ----------
        :param cost:
            The cost the card will be set to for the remainder of the turn.
        """
        self.ex_energy_cost = self.energy_cost
        self.energy_cost = cost

    # --- Card methods ---
    # These are methods you may wish to call on a card itself.

    def upgrade(self):
        """
        This method does everything required to fully upgrade the card.
        It handles marking the card upgraded, modifying the name, and executing the upgrade logic.
        """

        # If it's already upgraded and doesn't allow upgrades do nothing
        if self.upgraded and not self.allow_multiple_upgrades:
            return

        # Append the + to the name
        if not self.upgraded:
            self.name = self.name + "+"

        # Set the card to upgrade and execute the upgrade logic
        self.upgraded = True
        self.upgrade_logic()

    def __str__(self):
        """Override the str() method so printing it returns the name"""
        return self.name

    def __repr__(self):
        """Override the repr() method so arrays of cards print neatly"""
        return self.name


class AbstractEffect:
    """
    This abstraction allows the easy creation of Effects.
    An effect in this context is a Slay The Spire Buff,
    Debuff, or block.
    """

    def __init__(self):
        self.stacks = 0  # Number of stacks of this effect

    # === API/SANDBOX METHODS ===

    def modify_damage_taken(self, owner, environment, damage: int) -> int:
        """
        Effects overriding this can modify the damage taken by an actor or enemy.
        The return value of this method will be added to the damage, you can lower the damage
        received by returning a negative value.
        """
        pass

    def modify_damage_dealt(self, owner, environment, damage: int) -> int:
        """
        Effects overriding this can modify the damage dealt by an actor or enemy.
        The return value of this method will be added to the damage, you can lower the damage
        dealt by returning a negative value.
        """
        pass

    def on_end_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        """
        Effects overriding this can cause things to happen on the end of turn.
        """
        pass

    def on_start_turn(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        """
        Effects overriding this can cause things to happen on the end of turn.
        """
        pass

    def on_receive_damage_from_card(self: AbstractEffect, owner, environment, card):
        pass

    def on_card_play(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, card):
        pass

    def on_card_draw(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, card):
        pass

    def on_card_exhaust(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment):
        pass

    def on_take_damage(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment,
                       damaging_enemy: AbstractEnemy):
        pass

    def modify_card_draw(self: AbstractEffect, owner: AbstractActor | AbstractEnemy, environment, quantity):
        """
        Effects overriding this will modify the number of cards drawn
        """
        return 0


# ===================================
# === Effect Management and Mixin ===
# ===================================

class EffectMixin:
    """
    This EffectMixin class is added to both the actors and the enemies, and allows for
    managing different effects.

    Below are listed common API methods you are encouraged to use in the development
    of cards, enemies, relics, and effects. (Note that entity in this case means a player
    or enemy)

    - entity.clear_effects() -> Remove all effects from an entity
    - entity.add_effects(effect, qty) -> increments stacks of effect by qty
    - entity.set_effects(effect, qty) -> sets the stacks of effect to qty
    - entity.has_effect(effect) -> Returns true if entity has effect
    - entity.has_effect(effect, qty) -> returns true if entity has at least qty stacks of effect
    - entity.get_stacks(effect) -> Returns the number of stacks of effect
    """

    def __init__(self):
        # This is the primary dictionary of effects on an entity
        self.effects: dict[type[AbstractEffect], AbstractEffect] = {}
        self.ritual_flag: bool = False

    def process_effects(self: AbstractActor | AbstractEnemy, method_name: str, environment, parameter=None):
        """
        This method streamlines the processing of effects by allowing you to quickly
        call a given method on all effects. It is
        """
        # Note: func = getattr(obj, method_name); func;
        # is essentially the same as doing obj.method_name()
        # This is somewhat brittle since we take method name as
        # a string, but I think it simplifies enough to be worth it
        # TODO: Only call on methods where it exists

        for effect_name in list(self.effects):
            func = getattr(self.effects.get(effect_name), method_name)
            if parameter is not None:
                # Bug here?
                modification = func(self.effects.get(effect_name), environment, parameter)
                if modification is not None:
                    parameter = parameter + modification
            else:
                func(self, environment)
            for effect in list(self.effects):
                if self.effects.get(effect).stacks <= 0:
                    self.effects.pop(effect)

        return parameter

    def get_effects_dict(self) -> dict[str, int]:
        """
        Returns a dictionary of effects in the format {"effect name": stacks}
        This is primarily used for displaying information about all the stacks on an entity.
        """
        # Start with an empty dictionary
        effects_dict = {}
        for effect in self.effects:
            # Add a dictionary entry using the name of the effect as key and stacks as qty
            effects_dict[effect.__name__] = self.effects[effect].stacks
        # Return the final dict
        return effects_dict

    def clear_effects(self):
        """
        Removes all effects from the owner.
        """
        self.effects.clear()

    def has_effect(self, effect, quantity=None):
        if quantity is None:
            return effect in self.effects
        else:
            return effect.stacks >= quantity

    def _check_instantiate_effect(self, effect):
        if effect not in self.effects:
            self.effects[effect] = effect()

    def set_effect(self, effect, value):
        self._check_instantiate_effect(effect)
        self.effects.get(effect).stacks = value

    def increase_effect(self, effect, value):
        self._check_instantiate_effect(effect)
        self.effects.get(effect).stacks += value

    def decrease_effect(self, effect, value):
        self._check_instantiate_effect(effect)
        self.effects.get(effect).stacks -= value

    def get_effect_stacks(self, effect):
        self._check_instantiate_effect(effect)
        return self.effects.get(effect).stacks