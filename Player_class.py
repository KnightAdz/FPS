class Player:
    def __init__(self, name, player_deck, player_num, weapon1='Pistol', health=8):
        # Return a Card object whose name is *name* etc.
        self.name = name
        self.weapon1 = weapon1
        self.weapon2 = 0
        self.health = health
        self.armour = 0
        self.hand = []
        self.player_deck = player_deck
        self.discard_pile = []
        self.col_location = player_num

    def draw_hand(self, cards_modifier=0):
        # Draw number of cards from deck according to weapon clipsize
        self.hand = self.player_deck.draw_from(self.weapon1.clip_size + self.weapon2.clip_size)

    def discard_hand(self):
        # Discard hand
        self.discard_pile.add_to_top(self.hand)

    def shuffle_deck(self):
        self.player_deck.combine_with(self.discard_deck)


