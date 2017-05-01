from Deck_class import Deck
from Card_class import Card

class Player:
    def __init__(self, name, player_deck, player_num, weapon1='Pistol', health=8):
        # Return a Card object whose name is *name* etc.
        self.name = name
        self.weapon1 = Card(weapon1.name,weapon1.type,weapon1.subtype,weapon1.rows_in_range,weapon1.clip_size,
                            weapon1.health,weapon1.num_targets,weapon1.damage,weapon1.text)
        self.weapon2 = []
        self.health = health
        self.max_health = health
        self.armour = 0
        self.hand = Deck(self.name + " hand")
        self.player_deck = Deck(self.name + " deck", player_deck.cards)
        self.discard_deck = Deck(self.name + " discard pile")
        self.col_location = player_num
        self.player_deck.shuffle()

    def __str__(self):
        print(self.name + ' has %d health' % self.health)

    ### Hand functions
    def draw_new_hand(self, cards_modifier=0):
        # Draw number of cards from deck according to weapon clipsize
        num_cards = self.weapon1.clip_size + cards_modifier
        if self.weapon2 != []:
            num_cards += self.weapon2.clip_size
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
        self.discard_pile.add_to_top(self.hand)

    ### Deck functions
    def list_deck(self):
        print(self.name," has the following cards in deck:")
        self.player_deck.list_cards()

    def list_hand(self):
        print(self.name," has the following cards in hand:")
        self.hand.list_cards()

    def list_discard_pile(self):
            print(self.name, " has discarded the following cards:")
            self.discard_deck.list_cards()

    def shuffle_deck(self):
        self.player_deck.combine_with(self.discard_deck, shuffle=1)

    def take_turn(self):
        print(self.name + "'s turn")
        end_turn = False
        self.list_hand()
        while end_turn == False:
            card_to_play = int(input("Choose card to play: "))
            if card_to_play >= self.hand.get_size():
                end_turn = True
            else:
                # Play the card
                print(self.hand.cards[card_to_play], " played")
                # Add to discard pile
                self.discard_deck.cards.append(self.hand.cards[card_to_play])
                # Remove from hand
                del(self.hand.cards[card_to_play])
                # Remind of hand
                self.list_hand()
        #Discard any remaining cards
        for i in range(0,len(self.hand.cards)):
            self.discard_deck.cards.append(self.hands.cards[i])
        self.hands.empty()
        #Draw new hand
        if len(self.hand.cards) == 0:
            self.draw_new_hand()




