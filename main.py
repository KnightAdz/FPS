import Player_class
import Deck_class

# Globals
quit = False
MAX_LEVEL = 4
GRID_WIDTH = 4
GRID_HEIGHT = 4

#Game loop
while quit == False:
    # Define number of players
    num_players = input('How many players?')
    # Create the players and their decks, and the level deck
    Setup_game(num_players)

    #Begin the game at level 1
    level = 1
    while level <= MAX_LEVEL:
        Load_level(level)
        while Enemies_Alive():
            for num_players:
                Player_turn()
            Enemy_turn()
            if all_players_dead:
                quit = True
        #If enemies dead, level is complete (##LATER: To be changed to when level+1 card is drawn)
        Next_level_prep()
        level = level+1

    #If level > max_level, players have won!
    msg('You win!')
    quit = True


def Setup_game(n_players):
    # Create the players and their decks
    for i in 1:n_players:
        player[i] = Player("Player"+str(i),<Deck>,i)
    # Create the level deck
    level_deck = Create_level_deck()

def Load_Level(level_n):
    # Number of level cards should scale up to 16 (##LATER: could be enemies?)
    num_cards = level_n*2 + 4
    # Draw cards from the levek deck
    this_level_cards = level_deck.draw_cards(num_cards)
    #Create level grid

def Next_level_prep()
    #Heal up
    #Reload
    #Swap equipment
    #Define order

def Enemies_Alive()
    #Check the enemy grid for alive enemy cards
    enemies_alive = False
    if level_deck.size() > 0: ##LATER: this won't consider environment cards
        enemies_alive = True
    return enemies_alive