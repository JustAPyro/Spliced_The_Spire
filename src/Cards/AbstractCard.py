from abc import ABC, abstractmethod









class BurningBlood():
    pass












player = Actor(Ironclad)
enemy = Enemy()

player.use_card(enemy, RedStrike())
print(enemy.health)
print(player.energy)
player.use_card(None, RedDefend())
player.use_card(None, RedDefend())
print(player.buffs['BLOCK'])
print(player.energy)
