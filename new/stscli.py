from new.rooms import EnemyRoom
from new.enemies import Cultist
from new.actors import PlayerActor
from new.classes import Ironclad

x = EnemyRoom(
    actor=PlayerActor(Ironclad),
    enemies=[Cultist()])


print(x.state_string)
