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
CT_ARIFLE = 3
CT_BRIFLE = 4
CT_SRIFLE = 5
CT_ROCKET = 6
CT_FRAG = 7
CT_FLASHBANG = 8
CT_SMOKE = 9
CT_HELMET = 10
CT_ARMOUR = 11
CT_GRUNT = 12
CT_GRENADIER = 13
CT_SHIELDGUY = 14
CT_COMMANDER = 15
CT_WALL = 16
CT_BARREL = 17
CT_SNIPER = 18
CT_SHOT = 19
CT_PREC = 20
CT_ENTCOV = 21
CT_TACT = 22
CT_1STAID = 23
CT_ADRI = 24
CT_HIDE = 25
CT_RELOAD = 26
CT_TAKECOVER = 27
CT_COORDINATION = 28
CT_STEALTH = 29
CT_MARKTARGET = 30


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
                          cards_df.loc[i, "Text"],cards_df.loc[i, "Following State"]))
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
    level_deck.add_to_top(card_types[CT_WALL], num_players)
    level_deck.shuffle()

    # Create the weapons and skills deck
    weapon_deck = Deck("Weapon deck")
    weapon_deck.add_to_top(card_types[CT_SHOTGUN], num_players)
    weapon_deck.add_to_top(card_types[CT_SHOT], num_players*5)
    weapon_deck.add_to_top(card_types[CT_1STAID], num_players*5)
    weapon_deck.add_to_top(card_types[CT_TACT], num_players*5)
    weapon_deck.add_to_top(card_types[CT_ENTCOV], num_players*3)
    weapon_deck.shuffle()

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

    return players, level_deck, weapon_deck

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
                                    this_level_cards[i].num_targets,this_level_cards[i].damage,this_level_cards[i].text,this_level_cards[i].following_state)
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

            if len(weapon_deck.cards)>0 and not(this_level_cards[i].type=="Environment" and i==0):
                # While the weapon & skills deck isn't empty, give enemies loot
                level_grid[last_enemy_loc[1]][last_enemy_loc[0]].loot = Card(weapon_deck.cards[0].name,
                                                                             weapon_deck.cards[0].type,
                                                                             weapon_deck.cards[0].subtype,
                                                                             weapon_deck.cards[0].rows_in_range,
                                                                             weapon_deck.cards[0].clip_size,
                                                                             weapon_deck.cards[0].health,
                                                                             weapon_deck.cards[0].num_targets,
                                                                             weapon_deck.cards[0].damage,
                                                                             weapon_deck.cards[0].text,
                                                                             weapon_deck.cards[0].following_state)
                level_grid[last_enemy_loc[1]][last_enemy_loc[0]].damage += weapon_deck.cards[0].damage
                del(weapon_deck.cards[0])
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
    players, level_deck, weapon_deck = Setup_game(num_players)

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