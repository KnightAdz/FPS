from Player_class import Player
from Deck_class import Deck
from Card_class import Card
from GUI_class import GUI
from globals import *
import pandas as pd
from random import shuffle

quit = False
MAX_LEVEL = 4

#Card reference numbers
CT_PISTOL = 0
CT_UZI = 1
CT_SHOTGUN = 2
CT_SHOT = 19
CT_TACT = 22 # Tactical movement
CT_ENTCOV = 21 # Enter cover

CT_GRUNT = 12
CT_COMMANDER = 15

CT_WALL = 16
CT_BARREL = 17

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
        #print(len(card_types), " ", card_types[len(card_types)-1])
    return card_types

def Setup_game(n_players):
    # Check that the number of players makes sense
    if ~isinstance(n_players,int):
        n_players = int(n_players)
    if ~(n_players < 5 & n_players > 0):
        n_players = 2

    # Load cards to create decks from
    card_types = Load_cards()

    # Create the level deck
    level_deck = Deck("Level deck")
    level_deck.add_to_top(card_types[CT_GRUNT],num_players*5)
    level_deck.add_to_top(card_types[CT_COMMANDER],num_players)
    level_deck.add_to_top(card_types[CT_SHOTGUN],num_players)
    level_deck.add_to_top(card_types[CT_WALL], num_players)
    level_deck.shuffle()
    #print("Level deck contains:")
    #level_deck.list_cards()

    # Create a default player deck
    starting_deck = Deck("Starting deck")
    starting_deck.add_to_top(card_types[CT_SHOT],4)
    starting_deck.add_to_top(card_types[CT_TACT])
    starting_deck.add_to_top(card_types[CT_ENTCOV])

    # Create the players and their decks
    players = []
    for i in range(0,n_players):
        players.append(Player("Player "+str(i+1),starting_deck,i+1, weapon1=card_types[CT_PISTOL]))
        print("Player %d has joined the game" % len(players))
        players[i].draw_new_hand()
        # players[i].list_deck()
        # players[i].list_discard_pile()
        # players[i].list_hand()

    return players, level_deck

def Load_level(level_n):
    # Number of level cards should scale up to 16 (##LATER: could be enemies?)
    num_cards = level_n*2 + 6
    # Draw cards from the level deck
    this_level_cards = level_deck.draw_from(num_cards)
    # Make sure an enemy comes before a weapon
    while this_level_cards[0].type == "Weapon" or (this_level_cards[1] == "Weapon" and this_level_cards[0].type != "Enemy"):
        shuffle(this_level_cards)

    # Create level grid
    level_grid = [[[] for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]
    i = 0
    x = 0
    y = 0
    coverx = []
    covery = []
    last_enemy_loc = [0,0]
    while i < len(this_level_cards):
        if this_level_cards[i].type == "Enemy" or this_level_cards[i].type == "Environment":
            level_grid[y][x] = Card(this_level_cards[i].name,this_level_cards[i].type,this_level_cards[i].subtype,this_level_cards[i].rows_in_range,
                                    this_level_cards[i].clip_size,this_level_cards[i].health,
                                    this_level_cards[i].num_targets,this_level_cards[i].damage,this_level_cards[i].text)
            # Keep track of which enemies are in cover due to the environment
            if this_level_cards[i].type == "Environment":
                coverx.append(x)
                covery.append(y)
            else:
                last_enemy_loc = [x,y]

            for j in range(0,len(coverx)):
                if y > covery[j] and x == coverx[j] and isinstance(level_grid[y][x],Card):
                    level_grid[y][x].in_cover_to = [1,1,1,1] # All players

            x += 1
            if x >= GRID_WIDTH:
                x = 0
                y += 1
        elif this_level_cards[i].type == "Weapon":
            # Record the number of the target that has the same space as the weapon
            level_grid[last_enemy_loc[1]][last_enemy_loc[0]].loot = Card(this_level_cards[i].name,this_level_cards[i].type,this_level_cards[i].subtype,this_level_cards[i].rows_in_range,
                                                                        this_level_cards[i].clip_size,this_level_cards[i].health,
                                                                        this_level_cards[i].num_targets,this_level_cards[i].damage,this_level_cards[i].text)
            level_grid[last_enemy_loc[1]][last_enemy_loc[0]].damage += this_level_cards[i].damage-1
        i += 1

    return level_grid

def Next_level_prep():
    x = 0
    #Heal up
    #Reload
    #Swap equipment
    #Define order

def Enemies_alive(level_grid):
    #Check the enemy grid for alive enemy cards
    for y in range(0,GRID_HEIGHT):
        for x in range(0,GRID_WIDTH):
            if isinstance(level_grid[y][x],Card):
                if level_grid[y][x].type == "Enemy" and level_grid[y][x].health > 0:
                    return True
    return False

#Game loop
while not quit:
    # Define number of players
    #num_players = input('How many players?')
    num_players = 2
    # Create the players and their decks, and the level deck
    players, level_deck = Setup_game(num_players)

    level_grid = Load_level(0)
    gui = GUI(players, level_grid)
    gui.DisplayAction("Choose card to play:")
    while 1:
        gui.Display_level_grid()
        gui.Display_player_hand()
        gui.window.update()

    #Begin the game at level 1
    level = 1
    while level <= MAX_LEVEL:
        level_grid = Load_level(level)
        while Enemies_alive(level_grid):
            for i in range(0,num_players):
                if Enemies_alive(level_grid):
                    gui.Display_level_grid(level_grid,i)
                    players[i].take_turn(level_grid,players,gui)
                    Enemy_turn(level_grid,players,GRID_WIDTH)
                    #if all_players_dead:
                    #    quit = True
        #If enemies dead, level is complete (##LATER: To be changed to when level+1 card is drawn)
        Next_level_prep()
        level = level+1
        print("Now at Level ", level)
        if input( "Continue?") == 'n':
            level = MAX_LEVEL+1
            quit = True

    #If level > max_level, players have won!
    print('You win!')
    quit = True