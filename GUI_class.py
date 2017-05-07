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
        for i in range(0, len(players)):
            self.player_lbl = tk.Label(self.window, text="Player" + str(i + 1))
            self.player_lbl.pack()

        #Actions are a bit more complicated because we want to show a history
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

        self.input = -1
        self.button_pressed = False

    def Display_level_grid(self):
        # print("Level Grid:")
        lootstr = ""
        pstr = ""
        for y in range(GRID_HEIGHT - 1, -1, -1):
            for x in range(0, GRID_WIDTH):
                id = y * GRID_WIDTH + x
                pstr += str(id) + " "
                if not isinstance(self.level_grid[y][x], Card):
                    # Print empty space
                    pstr += "[\t]"
                else:
                    if self.level_grid[y][x].in_cover_to[self.current_player]:
                        pstr += "("
                    pstr += str(self.level_grid[y][x])
                    if self.level_grid[y][x].in_cover_to[self.current_player]:
                        pstr += ")"
                    if isinstance(self.level_grid[y][x].loot, Card):
                        lootstr += "Enemy " + str(id) + " has a " + self.level_grid[y][x].loot.name + "\n"
                if x < GRID_WIDTH - 1:
                    pstr += "\t\t"
            pstr += "\n\n"

        pstr = pstr + lootstr
        self.level_grid_lbl.configure(text=pstr)
        self.window.update()

    def DisplayAction(self,str):
        self.action_strs.append(str)
        self.action_text.insert(tk.END, "\n" + self.action_strs[len(self.action_strs)-1])
        self.window.update()

    def Display_player_hand(self):
        self.player_lbl.configure(text = self.players[self.current_player].list_hand())
        self.player_lbl.pack()
        self.window.update()

    def ButtonEntry(self):
        self.DisplayAction("Button pressed")
        card_num = -1
        target_num = -1
        self.input = self.entry.get()
        if self.input != "Enter choice":
            input_value = int(self.input)
            if self.game_state == "PLAYER TURN":
                if self.turn_state == "CARD CHOICE":
                    card_num = input_value
                    card_to_play = self.players[self.current_player].hand.cards[card_num]
                    self.DisplayAction(card_to_play.name + " card chosen")
                    self.turn_state = card_to_play.following_state()
                    if self.turn_state == "PLAY CARD":
                        #do card action
                        x=0
                    elif self.turn_state == "TARGET CHOICE":
                        self.DisplayAction("Choose target:")
                elif self.turn_state == "TARGET CHOICE":
                    target_num = input_value
                    self.DisplayAction("Target " + str(target_num) + " chosen")
                    #self.turn_state = play_card(player,card,target)
                elif self.turn_state == "END TURN":
                    #gather loot

                    #discard hand and redraw

                    #Advance to next player
                    self.current_player += 1
                    if self.current_player >= len(self.players):
                        player_num = 0
                    #check end of level
                    #enemy_turn()

        #self.Display_level_grid()
        #self.Display_player_hand()

    def GetInput(self,question_str="Enter choice"):
        #self.DisplayAction(question_str)
        if self.input != -1:
            value = self.input
            self.input = -1
            return value
        else:
            self.window.after(1000,self.GetInput(question_str))