from src.Cards.AbstractCard import AbstractCard


class RedStrike(AbstractCard):
    def __init__(self):
        self.damage = 6
        AbstractCard.__init__(self,
                              name="Strike",
                              energy_cost=1)

    def upgrade(self):
        self.name = self.name + '+'
        self.damage = 9

    def useCard(self, target):
        target.take_damage(self.damage)

    @staticmethod
    def get_test_cases():
        from tests.test_framework import TestDealsDamage, TestDealsDamageUpgraded
        return [
            TestDealsDamage(6),
        ]
