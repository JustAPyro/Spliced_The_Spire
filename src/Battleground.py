# This class also handles making sure turns are being called properly
# Represents a battle room
class Battleground:
    def __init__(self, actor, enemies):
        self.actor = actor
        self.enemies = enemies
        self.game_turn = 0

    # Allows you to add a monster to this battleground
    def add_monster(self, monster):

        print(monster.name, "has joined the battleground.")

        # Assign the monster the correct ascension level and actor target
        monster.ascension = self.ascension
        monster.actor = self.actor

        # Add the monster to the battleground monster list
        self.monsters.append(monster)

    def add_actor(self, actor):
        print("An actor has joined the battleground")
        self.actor = actor

    def next_round(self, verbose=False):
        self.actor.execute_turn()
        for monster in self.enemies:
            monster.take_turn()

    def battle_over(self):
        if self.actor.current_health > 0 and len(self.enemies) > 0:
            return False

        return True

    def overview(self):
        return f"{self.actor.name} vs {','.join(map(lambda n: n.name, self.enemies))}"
