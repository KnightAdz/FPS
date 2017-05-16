import tkinter as tk
from Player_class import Player
from Card_class import Card
from globals import *

class GUI:
    def __init__(self, players, level_grid):
        # Create a window to display GUI in
        self.window = tk.Tk()
        # Create some labels for displaying various parts of the game
        self.level_grid_lbl = tk.Label(self.window, text="Level")
        self.level_grid_lbl.pack()

        # Actions are a bit more complicated because we want to show a history
        self.action_scrollbar = tk.Scrollbar(self.window)
        self.action_text = tk.Text(self.window, height=8, width=50)
        self.action_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.action_text.pack(side=tk.LEFT, fill=tk.Y)
        self.action_scrollbar.config(command=self.action_text.yview)
        self.action_text.config(yscrollcommand=self.action_scrollbar.set)

        self.action_strs = []
        self.action_strs.append("Welcome to FPS")
        self.action_text.insert(tk.END,self.action_strs[len(self.action_strs)-1])

        #Game states to control what the button does
        self.game_state = "PLAYER TURN"
        self.turn_state = "CARD CHOICE"
        self.current_player = 0

        self.players = players
        self.level_grid = level_grid

        #Entry box
        self.entry = tk.Entry(self.window)
        self.entry.pack()

        self.entry.delete(0, tk.END)
        self.entry.insert(0, "Enter choice")

        self.button = tk.Button(self.window, text="OK", command=self.ButtonEntry)
        self.button.pack()

        self.player_lbl = tk.Label(self.window,text="Player info")
        self.player_lbl.pack()

        self.card_to_play = 0
        self.target = 0

    def Display_level_grid(self):
        # print("Level Grid:")

        allstr = ""
        for y in range(GRID_HEIGHT - 1, -1, -1):
            lootstr = "\t"
            pstr = ""
            for x in range(0, GRID_WIDTH):
                id = y * GRID_WIDTH + x
                pstr += str(id) + " "
                if not isinstance(self.level_grid[y][x], Card):
                    # Print empty space
                    pstr += "[\t]"
                    lootstr += "\t"
                else:
                    if self.level_grid[y][x].in_cover_to[self.current_player]:
                        pstr += "("
                    pstr += str(self.level_grid[y][x])
                    if self.level_grid[y][x].in_cover_to[self.current_player]:
                        pstr += ")"
                    if self.level_grid[y][x].type != "Enemy":
                        lootstr += "\t"
                    if isinstance(self.level_grid[y][x].loot, Card):
                        #lootstr += "Enemy " + str(id) + " has a " + self.level_grid[y][x].loot.name + "\n"
                        lootstr += self.level_grid[y][x].loot.name + "\t\t\t"
                if x < GRID_WIDTH - 1:
                    pstr += "\t\t"
            #pstr += "\n\n"
            allstr += pstr + "\n" + lootstr + "\n\n"

        #pstr = pstr + lootstr
        self.level_grid_lbl.configure(text=allstr)
        self.window.update()

    def DisplayAction(self,str):
        self.action_strs.append(str)
        self.action_text.insert(tk.END, "\n" + self.action_strs[len(self.action_strs)-1])
        self.action_text.see(tk.END)
        self.window.update()

    def Display_player_hand(self):
        self.player_lbl.configure(text = self.players[self.current_player].list_hand())
        self.player_lbl.pack()
        self.window.update()

    def ButtonEntry(self):
        card_num = -1
        target_num = -1
        # Grab the text from the text box
        input = self.entry.get()
        # Clear the text box
        self.entry.delete(0, tk.END)
        # Validate input
        if input != "Enter choice":
            input_value = int(input)

            if self.game_state == "PLAYER TURN":
                if self.turn_state == "CARD CHOICE":
                    card_num = input_value
                    if card_num >= len(self.players[self.current_player].hand.cards):
                        self.turn_state = "END TURN"
                    else:
                        self.card_to_play = self.players[self.current_player].hand.cards[card_num]
                        self.DisplayAction(self.card_to_play.name + " card chosen")
                        self.turn_state = self.card_to_play.following_state
                        if self.turn_state == "PLAY CARD":
                            self.Play_Card()
                        # If we should choose a weapon but only have one, skip straight to target choice
                        elif self.turn_state == "WEAPON CHOICE" and len(self.players[self.current_player].weapons)==1:
                            self.turn_state = "TARGET CHOICE"
                elif self.turn_state == "WEAPON CHOICE":
                    weapon_choice = input_value
                    self.Choose_weapon(weapon_choice)
                elif self.turn_state == "TARGET CHOICE":
                    target_num = input_value
                    self.target = self.Validate_target(target_num, self.players[self.current_player].weapon_equipped.rows_in_range)
                    if isinstance(self.target,Card):
                        self.Play_Card()
                elif self.turn_state == "PLAY CARD":
                    self.Play_Card()
                elif self.turn_state == "SWITCH WEAPON":
                    print("You have 1. ", self.players[self.current_player].weapons[0].name, " and 2: ",
                          self.players[self.current_player].weapons[1].name)
                    switch = int(input("Which would you like to switch for?"))
                    if switch == 1:
                        players[this_player].weapon1 = target.loot
                    elif switch == 2:
                        players[this_player].weapon2 = target.loot
                    else:
                        print(target.loot.name, " was not taken")
                if len(self.players[self.current_player].hand.cards) == 0:
                    self.turn_state = "END TURN"
                if self.turn_state == "END TURN":
                    self.Next_turn()
        self.Set_new_state()


    def Next_turn(self):
        # gather loot

        # discard hand and redraw
        self.players[self.current_player].discard_hand()
        self.players[self.current_player].draw_new_hand()

        # Let enemies retaliate
        self.Enemy_turn()

        # remove player from cover
        self.players[self.current_player].in_cover = False

        # Advance to next player
        self.current_player += 1
        if self.current_player >= len(self.players):
            self.current_player = 0
        self.DisplayAction(self.players[self.current_player].name + "'s turn")
        self.turn_state = "CARD CHOICE"

        # check end of level


    def Validate_target(self, target_num, rows_in_range=[1,1,1,1]):
        affect_cover = False
        if self.card_to_play.name == "Tactical Movement":
            affect_cover = True

        target_y = int(target_num / GRID_WIDTH)
        target_x = target_num - (target_y * GRID_WIDTH)
        target = self.level_grid[target_y][target_x]
        if isinstance(target, Card) and target.type == "Enemy":
            if rows_in_range[target_y] == 0:
                self.DisplayAction("Target is out of range of weapon, please choose another")
            elif not affect_cover and target.in_cover_to[self.current_player]:
                self.DisplayAction("Target is in cover and cannot be hit, please choose another")
            elif target.health <= 0:
                self.DisplayAction("Target is already dead, please choose another")
            else:
                # Target is accepted
                self.DisplayAction("Target " + str(target_num) + " chosen")
                self.turn_state = "PLAY CARD"
                return target
        else:
            self.DisplayAction("No target here, please select a target")

        return False

    def Choose_weapon(self, weapon_choice):
        weapon_choice -= 1
        if weapon_choice < 0:
            weapon_choice = 0
        elif weapon_choice >= len(self.players[self.current_player].weapons):
            weapon_choice = len(self.players[self.current_player].weapons)-1
        self.players[self.current_player].weapon_equipped = self.players[self.current_player].weapons[weapon_choice]
        self.turn_state = "TARGET CHOICE"

    def Set_new_state(self):
        if self.game_state == "PLAYER TURN":
            if self.turn_state == "CARD CHOICE":
                self.DisplayAction("Choose a card:")
            elif self.turn_state == "WEAPON CHOICE":
                self.DisplayAction("Choose a weapon to fire:")
                self.DisplayAction("1. "+self.players[self.current_player].weapons[0].name)
                self.DisplayAction("2. " + self.players[self.current_player].weapons[1].name)
            elif self.turn_state == "TARGET CHOICE":
                self.DisplayAction("Choose a target:")
            elif self.turn_state == "PLAY CARD":
                x=0
            elif self.turn_state == "SWITCH WEAPON":
                self.DisplayAction("Choose a weapon to switch:")
            if len(self.players[self.current_player].hand.cards) == 0:
                self.DisplayAction("Next players turn")

    def Play_Card(self):
        #Do the action of the card
        self.turn_state = self.card_to_play.action(self,self.level_grid,self.target,self.players,self.current_player)
        # Add card to player's discard pile
        self.players[self.current_player].discard_deck.cards.append(self.card_to_play)
        # Remove players from hand
        self.players[self.current_player].hand.cards.remove(self.card_to_play)
        if len(self.players[self.current_player].hand.cards) == 0:
            self.turn_state = "END TURN"

    def Enemy_turn(self):
        for y in range(GRID_HEIGHT - 1, -1, -1):
            for x in range(0, GRID_WIDTH):
                if isinstance(self.level_grid[y][x], Card):
                    if self.level_grid[y][x].retaliate and self.level_grid[y][x].health > 0:
                        target = self.players[self.level_grid[y][x].target]
                        self.DisplayAction(self.level_grid[y][x].name+ " retaliates against "+ target.name)
                        if target.in_cover:
                            self.DisplayAction(target.name+" is in cover and takes no damage")
                        else:
                            target.health -= self.level_grid[y][x].damage
                            self.DisplayAction(target.name+ " takes "+ str(self.level_grid[y][x].damage)+
                                               " damage and has "+ str(target.health)+" health remaining")
                        self.level_grid[y][x].retaliate = False