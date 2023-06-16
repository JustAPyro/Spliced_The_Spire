from effects import EffectMixin, CURLUP, VULNERABLE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from intents import Intent
    from actors import AbstractActor


class AbstractEnemy(EffectMixin):
    def __init__(self, max_health):
        self.max_health = max_health
        self.health = max_health
        self.intent = None

        super().__init__()

    def action(self, target, action):
        action.do(self, target)

    def is_dead(self):
        return self.health <= 0

    def _trigger_before_damage(self, damage: int):
        curl = False
        for effect in self.effects:
            if effect == CURLUP:
                curl = True

        if curl:
            self.apply_block(self.effects[CURLUP])
            self.negate_effect(CURLUP)

    def _trigger_after_turn(self):
        for effect in self.effects:
            if effect == VULNERABLE:
                self.decrease_effect(VULNERABLE, 1)

    def take_damage(self, damage: int):
        self._trigger_before_damage(damage)
        if self.has_effect(VULNERABLE):
            damage = damage * 1.5
        self.health -= damage

    def deal_damage(self, damage: int):
        pass

    def set_start(self, health, effects, intent):
        # TODO: Assert beginning
        self.max_health = health
        self.health = health
        self.apply_all_effects(effects)
        self.intent = intent
        return self


class Louse(AbstractEnemy):
    def __init__(self):
        super().__init__(50)

    def bite(self, target, quantity: int):
        target.take_damage(damage=quantity)
        self._trigger_after_turn()

    def grow(self, quantity):
        self.apply_strength(quantity)
        self._trigger_after_turn()
