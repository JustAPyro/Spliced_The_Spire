from __future__ import annotations

import random
from abc import ABC, abstractmethod
from random import randint
from typing import TYPE_CHECKING, Optional

import lutil
from lutil import asc_int
from new.abstractions import DamageMixin, AbstractActor
from new.effects import EffectMixin, Ritual, Block, Strength, Weak, CurlUp

if TYPE_CHECKING:
    pass


# Short term goal for this file
# - TODO: Polish and complete AbstractEnemy
# - - TODO: Fix the bad messaging code in take/deal damage of AbstractEnemy
# - TODO: Cultist, Jaw Worm, Red Louse & Green Louse, Acid Slime (m), Spike Slime(m), Acid Slime(s), Spike Slime(s)

class Intent:
    """
    A class that encompasses managing the Intent of enemies
    https://slay-the-spire.fandom.com/wiki/Intent
    """
    # The types of Intent that indicate an attack
    # and require a value for incoming damage
    __damage_types = (
        IntentType.AGGRESSIVE,
        IntentType.AGGRESSIVE_DEBUFF,
        IntentType.AGGRESSIVE_DEFENSE,
        IntentType.AGGRESSIVE_BUFF,
    )

    def __init__(self, intent_type: IntentType, damage: int = None):
        """
        Create an intent.

        Parameters
        ----------
        :param intent_type:
            The type of intent. These generally fall
            under a mix of "Aggressive", "Defensive, "Buff" and "Debuff"

        :param damage:
            The amount of damage being dealt for aggressive intents.
        """
        # Some guards to make sure damage values are only appearing when they should.
        if intent_type in self.__damage_types and not damage:
            raise ValueError("Aggressive Intent must have damage amount.")
        if damage and intent_type not in self.__damage_types:
            raise ValueError("Can't provide damage for intents not in __damage_types.")

        # Save the instance variables
        self.intent_type = intent_type
        self.damage = damage


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
        return self.environment['player']

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

    def take_turn(self, actor):
        log = []
        self.process_effects('on_start_turn', self.environment)
        next_method = next(self.ability_method_generator)
        self.log.append(next_method.__name__)
        next_method(actor, None, log)
        self.process_effects('on_end_turn', self.environment)
        return log[0]


class DummyEnemy(AbstractEnemy, ABC):
    def __init__(self, environment, health=10, ascension=0):
        super().__init__(name='Dummy',
                         max_health=health,
                         ascension=ascension,
                         act=1,
                         environment=environment)
        self.environment = environment

    def pattern(self):
        pass


# Checked 12/12/23
class Cultist(AbstractEnemy):
    max_health = {
        0: (48, 54),  # Health is 48-54 on A0+
        7: (50, 56)  # Health is 50-56 on A7+
    }
    # The amount of ritual gained by ascension
    ritual_gain = {
        +0: 3,
        +2: 4,
        17: 5
    }

    def __init__(self, environment=None, ascension=0):
        super().__init__(environment=environment,
                         ascension=ascension,
                         act=1)

    def incantation(self, target, quantity: Optional[int] = None, log=None):
        if log is None:
            log = []
        log.append('used incantation')

        increase = quantity if quantity is not None else asc_int(self.ascension, Cultist.ritual_gain)
        self.increase_effect(Ritual, increase)

    def dark_strike(self, target, damage: Optional[int] = None, log=None):
        if log is None:
            log = []
        self.deal_damage(6, target, log)

    def pattern(self):
        # Simple pattern: casts incantation, then spams dark stroke.
        yield self.incantation
        while True:
            yield self.dark_strike


# Checked 12/12/23
class Jaw_Worm(AbstractEnemy):
    max_health = {
        0: (40, 44),  # A1- Health is 48-54
        7: (42, 46)  # A7+ Health is 50-56
    }

    def __init__(self, ascension=0, act=1):
        super().__init__(ascension=ascension,
                         act=act)

    def chomp(self, target):
        # Chomp: Deal 11 damage, or 12 on ascension 2+
        target.take_damage(
            asc_int(self.ascension, {
                0: 11,
                2: 12
            }))

    def thrash(self, target):
        # Thrash: Deal 7 damage, gain 5 block.
        self.increase_effect(Block, 5)
        target.take_damage(7)

    def bellow(self):
        # Bellow: Gain strength and block
        self.increase_effect(Strength,
                             asc_int(self.ascension, {
                                 +0: 3,
                                 +2: 4,
                                 17: 5}))
        self.increase_effect(Block,
                             asc_int(self.ascension, {
                                 +0: 6,
                                 17: 9}))

    def pattern(self):
        yield self.chomp
        while True:
            yield self.rule_pattern(
                chances={
                    self.bellow: 45,
                    self.thrash: 30,
                    self.chomp: 25},
                successive_limit={
                    self.bellow: 2,
                    self.thrash: 3,
                    self.chomp: 2
                }
            )


class GreenLouse(AbstractEnemy, ABC):
    """
    Checked 12/12/23 (LH)
    Green Louse: https://slay-the-spire.fandom.com/wiki/Louses#Green_Louse.
    The green Louse has two abilities: Bite and Spit Web.
    """
    max_health = {
        0: (11, 17),
        7: (12, 18)
    }

    # Curl up effect applied at start
    curl_up_stack_map = {
        +0: (3, 7),
        +7: (4, 8),
        17: (9, 12),
    }

    def __init__(self, ascension=0, act=1,
                 base_damage: int = random.randint(5, 7),
                 curl_up_stacks: Optional[int] = None):
        """
        Create a Green louse. Note that base damage may be provided as a static value, but
        if it is not, then it will be randomly selected between 5 and 7 on enemy creation,
        which is how it happens in slay the spire.

        Parameters
        ----------
        :param ascension:
            The ascension the enemy is fighting on.

        :param act:
            What act the enemy is in (Which can affect behavior)

        :param base_damage:
            Green Louse select a value 'D' on creation, and then deal damage consistently
            throughout the fight based on that. The base_damage variable allows you to set
            the value of d manually, if you choose to. If you choose not to it will be
            generated randomly per slay the spire rules.

        :param curl_up_stacks:
            Green Louse starts with multiple stacks of Curl Up. Generally, this is
            determined randomly based on ascension, following the mapping in
            GreenLouse.curl_up_stack_map. If you would like to create a Green Louse
            starting with a specific number of curl up, you may provide it here.
        """
        # Apply the curl up stacks, calculating an appropriate one if none was provided
        self.increase_effect(CurlUp,
                             curl_up_stacks if curl_up_stacks else asc_int(ascension, GreenLouse.curl_up_stack_map))

        self.base_damage = base_damage
        super().__init__(ascension=ascension, act=act)

    def bite(self):
        """Deals damage based on the base_damage of the louse and the ascension."""
        self.damage(asc_int(self.ascension, {
            self.base_damage: 0,
            self.base_damage + 1: 2
        }))

    def spit_web(self):
        """Applies two weak."""
        self.get_actor().increase_effect(Weak, 2)

    def pattern(self):
        """
        Has a 25% chance of using Spit Web and a 75% chance of using Bite.
        Cannot use the same move three times in a row.

        On Ascension Icon Ascension 17, it cannot use Spit Web twice in a row
        and cannot use Bite three times in a row.
        """
        while True:
            yield self.rule_pattern(
                chances={
                    self.spit_web: 25,
                    self.bite: 75},
                successive_limit={
                    self.spit_web: 2 if self.ascension >= 17 else 3,
                    self.bite: 3})


class RedLouse(AbstractEnemy):
    """
    Checked 12/12/23 (LH)
    Red Louse: https://slay-the-spire.fandom.com/wiki/Louses#Red_Louse.
    The red Louse has two abilities: Bite and Grow.
    """
    health_range = {
        0: (10, 15),
        7: (11, 16)
    }

    # Curl Up effect applied at start
    curl_up_power = {
        +0: (3, 7),
        +7: (4, 8),
        17: (9, 12)
    }

    # TODO: Is 5, 7 right? Is this inclusive or exclusive?
    def __init__(self, ascension=0, act=1,
                 base_damage: int = random.randint(5, 7),
                 curl_up_stacks: Optional[int] = None):
        """
        Create a Red Louse. Note that base damage may be provided as a static value, but
        if it is not, then it will be randomly selected between 5 and 7 on enemy creation,
        which is how it happens in slay the spire.

        Parameters
        ----------
        :param ascension:
            The ascension the enemy is fighting on.

        :param act:
            What act the enemy is in (Which can affect behavior)

        :param base_damage:
            Red Louse select a value 'D' on creation, and then deal damage consistently
            throughout the fight based on that. The base_damage variable allows you to set
            the value of d manually, if you choose to. If you choose not to it will be
            generated randomly per slay the spire rules.

        :param curl_up_stacks:
            Red Louse starts with multiple stacks of Curl Up. Generally, this is
            determined randomly based on ascension, following the mapping in
            RedLouse.curl_up_stack_map. If you would like to create a Red Louse
            starting with a specific number of curl up, you may provide it here.
        """
        # Apply the curl up stacks, calculating an appropriate one if none was provided
        self.increase_effect(CurlUp,
                             curl_up_stacks if curl_up_stacks else asc_int(ascension, GreenLouse.curl_up_stack_map))

        self.base_damage = base_damage
        super().__init__(ascension=ascension, act=act)

    def bite(self):
        """Deals damage based on the base_damage of the louse and the ascension."""
        self.damage(asc_int(self.ascension, {
            self.base_damage: 0,
            self.base_damage + 1: 2
        }))

    def grow(self):
        """Gains 3 Strength. (4 on asc. 17+)"""
        self.increase_effect(Strength, 4 if self.ascension >= 17 else 3)

    def pattern(self):
        """
        Has a 25% chance of using Spit Web and a 75% chance of using Bite.
        Cannot use the same move three times in a row.

        On Ascension Icon Ascension 17, it cannot use Spit Web twice in a row
        and cannot use Bite three times in a row.
        """
        while True:
            yield self.rule_pattern(
                chances={
                    self.grow: 25,
                    self.bite: 75},
                successive_limit={
                    self.grow: 2 if self.ascension >= 17 else 3,
                    self.bite: 3})


x = Jaw_Worm()
gen = x.pattern()
last = None
for i in range(1000):
    print(next(gen))
