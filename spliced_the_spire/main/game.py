
from enumerations import *
from abstractions import *
from actors import *
from classes import *
from room import *
from enemies import *


player = AbstractActor(clas=Ironclad)

myFight = AbstractCombat(actor=player, enemies=[RedLouse()], isElite=False, isBoss=False)

print("my louse", myFight.enemies[0].get_effect_stacks(CurlUp))
myFight.beginRoom()

print("my louse", myFight.enemies[0].get_effect_stacks(CurlUp))
myFight.printRoom()

print("my louse", myFight.enemies[0].get_effect_stacks(CurlUp))
myFight.playerTurn()

print("my louse", myFight.enemies[0].get_effect_stacks(CurlUp))
myFight.printRoom()
