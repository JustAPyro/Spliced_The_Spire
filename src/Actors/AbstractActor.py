from abc import ABC, abstractmethod
import random


# Super/Parent class of a "Player" can be actual player or AI
class AbstractActor(ABC):
    def __init__(self, cards, health):

        # Instance variables
        self.max_health = health
        self.current_health = health
        self.block = 0

        # Card piles
        self.draw_pile = cards
        self.hand_pile = []
        self.discard_pile = []
        self.exhaust_pile = []

        # Shuffle the draw pile at the beginning
        random.shuffle(self.draw_pile)

    def execute_turn(self):
        self.__draw_cards(5)  # Start executing by drawing cards
        print("Drew cards:", self.hand_pile)
        self.take_turn()  # Then use whatever logic to make plays is provided
        self.__discard_cards()  # Then discard the remaining cards

    @abstractmethod
    def take_turn(self):
        pass

    def takeDamage(self, dmg):
        self.current_health -= dmg

    def modifyBlock(self):
        pass

    def __draw_cards(self, number):
        for i in range(number):
            self.__draw_card()

    def __draw_card(self):
        if len(self.draw_pile) > 0:
            self.hand_pile.append(self.draw_pile.pop())
        elif len(self.discard_pile) > 0:
            self.draw_pile.extend(self.discard_pile)
            self.discard_pile.clear()
            random.shuffle(self.draw_pile)
            self.hand_pile.append(self.draw_pile.pop())

    def shuffle_in(self, card, pile):
        pile.insert(random.randint(0, len(pile)), card)

    def __discard_cards(self):
        while len(self.hand_pile) > 0:
            self.discard_pile.append(self.hand_pile.pop())
