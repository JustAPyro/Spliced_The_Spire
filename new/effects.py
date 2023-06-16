from __future__ import annotations

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from actors import AbstractActor
    from enemies import AbstractEnemy

BLOCK = 'BLOCK'
CURLUP = 'CURLUP'
VULNERABLE = 'VULNERABLE'
STRENGTH = 'STRENGTH'


class EffectMixin:
    def __init__(self):
        self.effects = {}

    def negate_effect(self, effect):
        self.effects[effect] = 0

    def decrease_effect(self, effect, quantity):
        current = self.get_effect(effect)
        if current > 1:
            self.set_effect(effect, current - quantity)

    def has_effect(self, effect, quantity=None):
        cur_quantity = self.effects.get(effect, 0)
        if quantity is None:
            return cur_quantity > 0
        return cur_quantity == quantity

    def get_effect(self, effect):
        return self.effects.get(effect, 0)

    def set_effect(self, effect, value):
        self.effects[effect] = value

    def _stack(self: AbstractActor | AbstractEnemy, effect, quantity):
        existing = self.effects.get(effect, 0)
        self.effects[effect] = existing + quantity

    def apply_all_effects(self: AbstractActor | AbstractEnemy, effects: list[tuple[str, int]]):
        for effect, quantity in effects:
            self._stack(effect, quantity)

    def apply_effect(self: AbstractActor | AbstractEnemy, effect: str, quantity: int):
        self._stack(effect, quantity)

    def apply_block(self: AbstractActor | AbstractEnemy, quantity: int):
        self._stack(BLOCK, quantity)

    def apply_vulnerable(self: AbstractActor | AbstractEnemy, quantity: int):
        self._stack(VULNERABLE, quantity)

    def apply_curlup(self: AbstractActor | AbstractEnemy, quantity: int):
        self._stack(CURLUP, quantity)

    def apply_strength(self: AbstractActor | AbstractEnemy, quantity: int):
        self._stack(STRENGTH, quantity)
