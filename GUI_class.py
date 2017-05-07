import tkinter as tk
from Player_class import Player
from Card_class import Card
from globals import *

class GUI:
    def __init__(self, num_players=2):
        # Create a window to display GUI in
        self.window = tk.Tk()
        # Create some labels for displaying various parts of the game
        self.level_grid_lbl = tk.Label(self.window, text="Level")
        self.level_grid_lbl.pack()
        for i in range(0, num_players):
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

        #Entry box
        self.entry = tk.Entry(self.window)
        self.entry.pack()

        self.entry.delete(0, tk.END)
        self.entry.insert(0, "Enter choice")

        self.button = tk.Button(self.window, text="OK", command=self.ButtonEntry)
        self.button.pack()

        self.input = -1
        self.button_pressed = False

    def Display_level_grid(self, level_grid, this_player):
        # print("Level Grid:")
        lootstr = ""
        pstr = ""
        for y in range(GRID_HEIGHT - 1, -1, -1):
            for x in range(0, GRID_WIDTH):
                id = y * GRID_WIDTH + x
                pstr += str(id) + " "
                if not isinstance(level_grid[y][x], Card):
                    # Print empty space
                    pstr += "[\t]"
                else:
                    if level_grid[y][x].in_cover_to[this_player]:
                        pstr += "("
                    pstr += str(level_grid[y][x])
                    if level_grid[y][x].in_cover_to[this_player]:
                        pstr += ")"
                    if isinstance(level_grid[y][x].loot, Card):
                        lootstr += "Enemy " + str(id) + " has a " + level_grid[y][x].loot.name + "\n"
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

    def Display_player_hand(self, player):
        self.player_lbl.configure(text = player.list_hand())
        self.player_lbl.pack()
        self.window.update()

    def ButtonEntry(self):
        self.input = self.entry.get()
        self.button_pressed = True

    def GetInput(self,question_str="Enter choice"):
        self.DisplayAction(question_str)
        while self.button_pressed == False:
            self.window.mainloop()
        self.button_pressed = True
        return self.input