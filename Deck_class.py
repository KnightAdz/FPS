import Card_class
from random import shuffle

class Deck:
    def __init__(self, name, cards=[]):
        # Return a Deck object whose name is *name* and that contains the list of *cards*
        self.name = name
        #self.cards = cards
        self.cards = list()
        if cards != []:
            self.cards.append(cards)

    def list_cards(self):
        if len(self.cards) == 0:
            print("No cards")
        else:
            for i in range(0,len(self.cards)):
                print(i,self.cards[i])

    def shuffle(self):
        # Sort the list of cards in random order
        shuffle(self.cards)

    def get_size(self):
        # Return number of cards in deck
        return len(self.cards)

    def draw_from(self, num_cards):
        # Return *num_cards* from the top of the deck and remove them from the list, if less cards than requested are
        # returned then we know the deck is empty

        # Check if we can draw needed amount of cards
        if num_cards < self.get_size():
            drawn_cards = self.cards[0:num_cards-1]
            self.cards = self.cards[num_cards:-1]

        else:
            #Draw what we can
            drawn_cards = self.cards
            deck.empty(self)
        return drawn_cards

    def add_to_top(self,new_cards,copies=1):
        # Add list of cards to top of this deck
        for i in range(0,copies):
            self.cards.append(new_cards)

    def combine_with(self, other_deck, shuffle=1):
        # Combine two decks to make one deck
        self.add_to_top(other_deck.cards)
        #Empty other deck
        other_deck.empty()
        if shuffle:
            self.shuffle()

    def empty(self):
        # Remove all cards from deck
        self.cards = []
