from Deck_class import Deck

class Player:
    def __init__(self, name, player_deck, player_num, weapon1='Pistol', health=8):
        # Return a Card object whose name is *name* etc.
        self.name = name
        self.weapon1 = weapon1
        self.weapon2 = 0
        self.health = health
        self.max_health = health
        self.armour = 0
        self.hand = Deck(self.name + " hand")
        self.player_deck = player_deck
        self.discard_deck = Deck(self.name + " discard pile")
        self.col_location = player_num
        self.player_deck.shuffle()

    def __str__(self):
        print(self.name + ' has %d health' % self.health)

    ### Hand functions
    def draw_new_hand(self, cards_modifier=0):
        # Draw number of cards from deck according to weapon clipsize
        self.hand = self.player_deck.draw_from(self.weapon1.clip_size + self.weapon2.clip_size)

    def discard_hand(self):
        # Discard hand
        self.discard_pile.add_to_top(self.hand)

    ### Deck functions
    def list_deck(self):
        print(self.name," has the following cards in deck:")
        self.player_deck.list_cards()

    def list_discard_pile(self):
            print(self.name, " has discarded the following cards:")
            self.discard_deck.list_cards()

    def shuffle_deck(self):
        self.player_deck.combine_with(self.discard_deck, shuffle=1)

    def take_turn(self):
        print(self.Name + "'s turn")




