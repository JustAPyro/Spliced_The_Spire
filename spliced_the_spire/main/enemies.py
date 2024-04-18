from __future__ import annotations

import random
from abc import ABC
from typing import TYPE_CHECKING, Optional

from spliced_the_spire.lutil import asc_int
from spliced_the_spire.main.abstractions import AbstractEnemy, Room
from spliced_the_spire.main.cards import Slimed
from spliced_the_spire.main.effects import Ritual, Block, Strength, Weak, CurlUp, Frail
from spliced_the_spire.main.enumerations import IntentType

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


class DummyEnemy(AbstractEnemy, ABC):
    max_health = {0: 10, 100: 10}

    def __init__(self, room=None, health=10, ascension=0, target=None):
        super().__init__(room=room,
                         name='Dummy',
                         max_health=health,
                         ascension=ascension,
                         act=1,
                         target=target)
        self.room = room

    def pattern(self):
        pass


# Checked 12/12/23
class Cultist(AbstractEnemy):
    """
    Cultist: https://slay-the-spire.fandom.com/wiki/Cultist
    The Cultist has two abilities: Incantation and Dark Strike
    """
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

    def __init__(self, *args, **kwargs):
        """
        Creates a Cultist.

        Parameters
        ----------
        :param room:
            The room the enemy is acting in.

        :param ascension:
            The ascension the enemy is fighting on.

        :param act:
            What act the enemy is in (Which can affect behavior)
        """
        super().__init__(*args, **kwargs)

    def incantation(self):
        self.intent = IntentType.BUFF,
        self.message = 'Cultist used incantation'
        self.increase_effect(Ritual, asc_int(self.ascension, {
            +0: 3,
            +2: 4,
            17: 5
        }))

    def dark_strike(self):
        """Deal 6 damage."""
        self.intent = IntentType.AGGRESSIVE
        self.message = 'Cultist used Dark Strike'
        self.deal_damage(6)

    def pattern(self):
        """Simple pattern: casts incantation, then spams dark stroke."""
        yield self.incantation
        while True:
            yield self.dark_strike


# Checked 12/12/23
class JawWorm(AbstractEnemy):
    max_health = {
        0: (40, 44),  # A1- Health is 48-54
        7: (42, 46)  # A7+ Health is 50-56
    }

    def __init__(self, room: dict = None, ascension=0, act=1):
        super().__init__(room=room,
                         ascension=ascension,
                         act=act)

    def chomp(self):
        # Chomp: Deal 11 damage, or 12 on ascension 2+
        self.intent = IntentType.AGGRESSIVE
        self.message = 'Jaw Worm used Chomp'
        self.deal_damage(
            asc_int(self.ascension, {
                0: 11,
                2: 12
            }))

    def thrash(self):
        # Thrash: Deal 7 damage, gain 5 block.
        self.intent = IntentType.AGGRESSIVE_DEFENSE
        self.message = 'Jaw Worm used Thrash'
        self.increase_effect(Block, 5)
        self.deal_damage(7)

    def bellow(self):
        # Bellow: Gain strength and block
        self.intent = IntentType.DEFENSIVE_BUFF
        self.message = 'Jaw Worm used Bellow'
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
                successive_limit_dict={
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
        17: (9, 12)
    }

    def __init__(self, room: Room = None, ascension=0, act=1,
                 base_damage: int = random.randint(5, 7),
                 curl_up_stacks: Optional[int] = None, *args, **kwargs):
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
        super().__init__(room=room, ascension=ascension, act=act, *args, **kwargs)
        # Apply the curl up stacks, calculating an appropriate one if none was provided
        self.increase_effect(CurlUp,
                             curl_up_stacks if curl_up_stacks else asc_int(ascension, GreenLouse.curl_up_stack_map))

        self.base_damage = base_damage

    def bite(self):
        """Deals damage based on the base_damage of the louse and the ascension."""
        self.deal_damage(asc_int(self.ascension, {
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
                successive_limit_dict={
                    self.spit_web: 2 if self.ascension >= 17 else 3,
                    self.bite: 3})


class RedLouse(AbstractEnemy):
    """
    Checked 12/12/23 (LH)
    Red Louse: https://slay-the-spire.fandom.com/wiki/Louses#Red_Louse.
    The red Louse has two abilities: Bite and Grow.
    """
    max_health = {
        0: (10, 15),
        7: (11, 16)
    }

    # Curl Up effect applied at start
    curl_up_stack_map = {
        +0: (3, 7),
        +7: (4, 8),
        17: (9, 12)
    }

    # TODO: Is 5, 7 right? Is this inclusive or exclusive?
    def __init__(self, room, ascension=0, act=1,
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
        super().__init__(room, ascension=ascension, act=act)
        # Apply the curl up stacks, calculating an appropriate one if none was provided
        self.increase_effect(CurlUp,
                             curl_up_stacks if curl_up_stacks else asc_int(ascension, RedLouse.curl_up_stack_map))

        self.base_damage = base_damage

    def bite(self):
        """Deals damage based on the base_damage of the louse and the ascension."""
        self.deal_damage(asc_int(self.ascension, {
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
                successive_limit_dict={
                    self.grow: 2 if self.ascension >= 17 else 3,
                    self.bite: 3})


class AcidSlimeSmall(AbstractEnemy):
    max_health = {
        0: (8, 12),
        7: (9, 13)
    }

    def __init__(self, room, ascension=0, act=1):
        super().__init__(room, ascension=ascension, act=act)

    def lick(self):
        self.get_actor().increase_effect(Weak, 1)

    def tackle(self):
        self.deal_damage(3) if self.ascension < 2 else self.deal_damage(4)

    def pattern(self):
        if self.ascension >= 17 or random.randint(0, 1) == 0:
            first_ability = self.lick
            second_ability = self.tackle
        else:
            first_ability = self.tackle
            second_ability = self.lick

        while True:
            yield first_ability
            yield second_ability


class AcidSlimeMedium(AbstractEnemy):
    max_health = {
        0: (28, 32),
        7: (29, 34)
    }

    def __init__(self, room, ascension=0, act=1, *args, **kwargs):
        super().__init__(room, ascension=ascension, act=act, *args, **kwargs)

    def corrosive_spit(self):
        self.deal_damage(7) if self.ascension < 2 else self.deal_damage(8)
        self.get_actor().discard_pile.append(Slimed())

    def lick(self):
        self.get_actor().increase_effect(Weak, 1)

    def tackle(self):
        self.deal_damage(10) if self.ascension < 2 else self.deal_damage(12)

    def pattern(self):
        while True:
            yield self.rule_pattern(
                chances={
                    self.corrosive_spit: 30 if self.ascension < 17 else 40,
                    self.tackle: 40,
                    self.lick: 30 if self.ascension < 17 else 20},
                successive_limit_dict={
                    self.tackle: 2,
                    self.lick: 3 if self.ascension < 17 else 2,
                    self.corrosive_spit: 3})


class AcidSlimeLarge(AbstractEnemy):
    max_health = {
        0: (65, 69),
        7: (68, 72)
    }

    def __init__(self, room, ascension=0, act=1):
        super().__init__(room, ascension=ascension, act=act)

    def corrosive_spit(self):
        self.deal_damage(11) if self.ascension < 2 else self.deal_damage(12)
        self.get_actor().discard_pile.extend([Slimed(), Slimed()])

    def lick(self):
        self.get_actor().increase_effect(Weak, 2)

    def tackle(self):
        self.deal_damage(16) if self.ascension < 2 else self.deal_damage(18)

    def split(self):
        self.room.enemies.extend(
            [AcidSlimeMedium(max_health=self.health, ascension=self.ascension, room=self.room, act=self.act),
             AcidSlimeMedium(max_health=self.health, ascension=self.ascension, room=self.room, act=self.act)])
        self.room.enemies.remove(self)
        self.health = 0

    def pattern(self):
        while True:
            if self.health <= self.max_health * 0.5:
                yield self.split
            else:
                yield self.rule_pattern(
                    chances={
                        self.corrosive_spit: 30 if self.ascension < 17 else 40,
                        self.tackle: 40,
                        self.lick: 30 if self.ascension < 17 else 20},
                    successive_limit_dict={
                        self.tackle: 2,
                        self.lick: 3 if self.ascension < 17 else 2,
                        self.corrosive_spit: 3})


class SpikeSlimeSmall(AbstractEnemy):
    max_health = {
        0: (10, 14),
        7: (11, 15)
    }

    def __init__(self, room, ascension=0, act=1):
        super().__init__(room, ascension=ascension, act=act)

    def tackle(self):
        self.deal_damage(5) if self.ascension < 2 else self.deal_damage(6)

    def pattern(self):
        while True:
            yield self.tackle


class SpikeSlimeMedium(AbstractEnemy):
    max_health = {
        0: (28, 32),
        7: (29, 34)
    }

    def __init__(self, room, ascension=0, act=1, *args, **kwargs):
        super().__init__(room, ascension=ascension, act=act, *args, **kwargs)

    def lick(self):
        self.get_actor().increase_effect(Frail, 1)

    def flame_tackle(self):
        self.deal_damage(8) if self.ascension < 2 else self.deal_damage(10)
        self.get_actor().discard_pile.append(Slimed())

    def pattern(self):
        while True:
            yield self.rule_pattern(
                chances={
                    self.flame_tackle: 30,
                    self.lick: 70},
                successive_limit_dict={
                    self.flame_tackle: 3,
                    self.lick: 3 if self.ascension < 17 else 2, })


class SpikeSlimeLarge(AbstractEnemy):
    max_health = {
        0: (64, 70),
        7: (67, 73)
    }

    def __init__(self, room, ascension=0, act=1):
        super().__init__(room, ascension=ascension, act=act)

    def lick(self):
        frail = 2 if self.ascension < 17 else 3
        self.get_actor().increase_effect(Frail, frail)

    def flame_tackle(self):
        self.deal_damage(16) if self.ascension < 2 else self.deal_damage(18)
        self.get_actor().discard_pile.extend([Slimed(), Slimed()])

    def split(self):
        self.room.enemies.extend(
            [SpikeSlimeMedium(max_health=self.health, ascension=self.ascension, room=self.room, act=self.act),
             SpikeSlimeMedium(max_health=self.health, ascension=self.ascension, room=self.room, act=self.act)])
        self.room.enemies.remove(self)
        self.health = 0

    def pattern(self):
        while True:
            if self.health <= self.max_health * 0.5:
                yield self.split
            else:
                yield self.rule_pattern(
                    chances={
                        self.flame_tackle: 30,
                        self.lick: 70},
                    successive_limit_dict={
                        self.flame_tackle: 3,
                        self.lick: 3 if self.ascension < 17 else 2, })


env = {}
enemies = {cls(env).sts_name: cls for cls in AbstractEnemy.__subclasses__()}
