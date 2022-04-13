# A battleground to actually simulate a fighti n
class Battleground:
    def __init__(self, ascention):
        self.ascention = ascention
        self.monsters = []
        print("New battleground created at ascention", ascention)
        
    # Allows you to add a monster to this battleground
    def add_monster(self, monster):
        
        # When the monster is added to the battleground assign it to the correct asc level
        monster.ascention = self.ascention
        
        # Add the monster to the battleground monster list
        self.monsters.append(monster)
        
