from Player_class import Player
from Deck_class import Deck
from Card_class import Card
import pandas as pd

#
# Globals
#
quit = False
MAX_LEVEL = 4
GRID_WIDTH = 4
GRID_HEIGHT = 4

#Card reference numbers
CT_PISTOL = 0
CT_UZI = 1
CT_SHOT = 19
CT_TACT = 22 # Tactical movement
CT_ENTCOV = 21 # Enter cover

CT_GRUNT = 12
CT_COMMANDER = 15

def Load_cards():
    # Load card stats from CSV file
    cards_df = pd.DataFrame.from_csv("Cards.csv")
    card_types = []
    # Create a card object for each row
    for i in range(1,cards_df.shape[0]+1):
        rows_in_range = [ cards_df.loc[i,"row1"],cards_df.loc[i,"row2"],cards_df.loc[i,"row3"],cards_df.loc[i,"row4"] ]
        card_types.append(Card(cards_df.loc[i,"Name"],cards_df.loc[i,"Type"],
                          cards_df.loc[i, "Subtype"], rows_in_range,
                          cards_df.loc[i, "clip size"],cards_df.loc[i,"health"],
                          cards_df.loc[i, "no. targets"],cards_df.loc[i,"damage"],
                          cards_df.loc[i, "Text"]))
        print(len(card_types), " ", card_types[len(card_types)-1])

    return card_types

def Setup_game(n_players):
    # Check that the number of players makes sense
    if ~isinstance(n_players,int):
        n_players = int(n_players)
    if ~(n_players < 5 & n_players > 0):
        n_players = 2

    # Load cards to create decks from
    card_types = Load_cards()

    # Create a default player deck
    starting_deck = Deck("Starting deck")
    starting_deck.add_to_top(card_types[CT_SHOT],4)
    starting_deck.add_to_top(card_types[CT_TACT])
    starting_deck.add_to_top(card_types[CT_ENTCOV])

    # Create the players and their decks
    players = []
    for i in range(0,n_players):
        players.append(Player("Player "+str(i+1),starting_deck,i+1))
        print("Player %d has joined the game" % len(players))
        players[i].list_deck()


    # Create the level deck
    level_deck = Deck("Level deck")
    level_deck.add_to_top(card_types[CT_GRUNT],num_players*10)
    level_deck.add_to_top(card_types[CT_COMMANDER],num_players)
    level_deck.shuffle()
    print("Level deck contains:")
    level_deck.list_cards()

    players[1].player_deck.cards[0].name = "Changed"

    players[0].list_deck()
    players[0].list_discard_pile()

    return players, level_deck

def Load_level(level_n):
    # Number of level cards should scale up to 16 (##LATER: could be enemies?)
    num_cards = level_n*2 + 4
    # Draw cards from the levek deck
    this_level_cards = level_deck.draw_cards(num_cards)
    #Create level grid

def Next_level_prep():
    x = 0
    #Heal up
    #Reload
    #Swap equipment
    #Define order

def Enemies_alive():
    #Check the enemy grid for alive enemy cards
    #enemies_alive = False
    #if level_deck.size() > 0: ##LATER: this won't consider environment cards
    enemies_alive = True
    return enemies_alive


#Game loop
while quit == False:
    # Define number of players
    #num_players = input('How many players?')
    num_players = 2
    # Create the players and their decks, and the level deck
    players, level_deck = Setup_game(num_players)

    #Begin the game at level 1
    level = 1
    while level <= MAX_LEVEL:
        level_grid = Load_level(level)
        while Enemies_alive():
            for i in range(1,num_players):
                players[i].Take_turn()
            #Enemy_turn()
            #if all_players_dead:
            #    quit = True
        #If enemies dead, level is complete (##LATER: To be changed to when level+1 card is drawn)
        Next_level_prep()
        level = level+1
        if input('Continue?') == 'n':
            quit = True

    #If level > max_level, players have won!
    msg('You win!')
    quit = True


