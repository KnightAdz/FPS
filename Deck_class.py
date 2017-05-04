from Card_class import Card
from random import shuffle
from globals import *

class Deck:
    def __init__(self, name, cards=[]):
        # Return a Deck object whose name is *name* and that contains the list of *cards*
        self.name = name
        #self.cards = cards
        self.cards = list()
        if cards != []:
            for i in range(0,len(cards)):
                self.cards.append(Card(cards[i].name,cards[i].type,cards[i].subtype,cards[i].rows_in_range,
                                       cards[i].clip_size,cards[i].health,cards[i].num_targets,cards[i].damage,cards[i].text))

    def list_cards(self):
        card_str = ""
        if len(self.cards) == 0:
            card_str = "No cards"
        else:
            for i in range(0,len(self.cards)):
                card_str += str(i) + ". " + self.cards[i].name + "\n"
        return card_str

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
            drawn_cards = self.cards[0:num_cards]
            self.cards = self.cards[num_cards:]
        else:
            #Draw what we can
            drawn_cards = self.cards
            self.empty()
        return drawn_cards

    def add_to_top(self,cards,copies=1):
        # Add list of cards to top of this deck
        if isinstance(cards, Card):
            for j in range(0, copies):
                self.cards.append(cards)
        else:
            for j in range(0,copies):
                for i in range(0,len(cards)):
                    self.cards.append(Card(cards[i].name, cards[i].subtype, cards[i].rows_in_range, cards[i].clip_size,
                                        cards[i].health,cards[i].num_targets,cards[i].damage,cards[i].text))

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
