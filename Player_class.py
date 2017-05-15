from Deck_class import Deck
from Card_class import Card
from globals import *

class Player:
    def __init__(self, name, player_deck, player_num, weapon1='Pistol', health=8):
        # Return a Card object whose name is *name* etc.
        self.name = name
        self.weapons = []
        self.weapons.append(Card(weapon1.name,weapon1.type,weapon1.subtype,weapon1.rows_in_range,weapon1.clip_size,
                            weapon1.health,weapon1.num_targets,weapon1.damage,weapon1.text,weapon1.following_state))
        self.weapon_equipped = self.weapons[0]
        self.health = health
        self.max_health = health
        self.armour = 0
        self.hand = Deck(self.name + " hand")
        self.player_deck = Deck(self.name + " deck", player_deck.cards)
        self.discard_deck = Deck(self.name + " discard pile")
        self.col_location = player_num
        self.player_deck.shuffle()
        self.player_num = player_num

        self.in_cover = False

    def __str__(self):
        print(self.name + ' has %d health' % self.health)

    ### Hand functions
    def draw_new_hand(self, cards_modifier=0):
        # Draw number of cards from deck according to weapon clipsize
        num_cards = cards_modifier
        for i in range(0,len(self.weapons)):
            num_cards += self.weapons[i].clip_size
        self.hand.add_to_top(self.player_deck.draw_from(num_cards))
        # If we didn't get back enough cards
        if len(self.hand.cards) < num_cards:
            # If the discard pile has cards we could use
            if len(self.discard_deck.cards) > 0:
                # Recycle the discard cards back into the deck
                self.shuffle_deck()
                # And try to draw the rest of the cards we need
                self.hand.add_to_top(self.player_deck.draw_from(num_cards - len(self.hand.cards)))

    def discard_hand(self):
        # Discard hand
        if len(self.hand.cards)>0:
            self.discard_deck.add_to_top(self.hand.cards)
        self.hand.empty()

    ### Deck functions
    def list_deck(self):
        deck_str = self.name + " has the following cards in deck:\n"
        deck_str += self.player_deck.list_cards()
        return deck_str

    def list_hand(self):
        hand_str = self.name + " has the following cards in hand:\n"
        return hand_str + self.hand.list_cards()

    def list_discard_pile(self):
            print(self.name, " has discarded the following cards:")
            self.discard_deck.list_cards()

    def shuffle_deck(self):
        self.player_deck.combine_with(self.discard_deck, shuffle=1)

    def heal(self,health_points):
        self.health = min(self.health+health_points, self.max_health)