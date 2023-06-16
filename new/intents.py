class Intent:
    pass


class Buff(Intent):
    pass


class Attack(Intent):
    def __init__(self, attack: int):
        self.attack = attack
