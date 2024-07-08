
from enumerations import *
from abstractions import *
from actors import *
from classes import *
from room import *
from enemies import *

player = AbstractActor(clas=Ironclad)

myFight = AbstractCombat(actor=player, enemies=[RedLouse()], isElite=False, isBoss=False)
myFight.enemies[0].increase_effect(Block, 5)
myFight.beginRoom()

myFight.printRoom()

myFight.playerTurn()

myFight.printRoom()
