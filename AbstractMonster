class Monster(ABC):
    
    def __init__(self, name, max_health):
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.turn = 0
        
        # Some defaults that need to be set before using
        self.ascention = 0
        self.actor = None
        
    @abstractmethod
    def take_turn(self):
        pass
    
