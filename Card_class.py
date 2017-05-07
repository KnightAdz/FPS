from globals import *

#Main Card class
class Card:
    def __init__(self, name, type="Action",subtype=0,rows_in_range=[1,1,1,1],clip_size=0,health=99,num_targets=1,damage=0,text=""):
        # Return a Card object whose name is *name* etc.
        self.name = name
        self.type = type
        self.subtype = subtype
        self.rows_in_range = rows_in_range
        self.clip_size = clip_size
        self.damage = damage
        self.health = health
        self.num_targets = num_targets
        self.text=text

        #Enemy-specific variables
        self.in_cover_to = [0,0,0,0] # No players
        if self.name == "Shield guy":
            self.in_cover_to = [1,1,1,1] # All players
        self.retaliate = False
        self.target = 0
        self.loot = 0

    def take_damage(self,damage_taken):
        self.health = self.health - damage_taken
        return damage_taken

    def deal_damage(self, targets):
        targets.health = target.health - self.damage

    def __str__(self):
        if self.type == "Enemy":
            return self.name + " H:" + str(self.health) + " D:" + str(self.damage)
        else:
            return self.name

    def action(self,level_grid,players,this_player,GRID_WIDTH):
        # Perform the action of the card
        if self.name == "Shot" or self.name == "Precision Shot" or self.name == "Stealth shot":
            # Need to choose a weapon unless we only have 1
            weapon = players[this_player].weapon1
            if isinstance(players[this_player].weapon2,Card):
                print("You have 2 weapons: 1:",str(players[this_player].weapon1)," 2: ",str(players[this_player].weapon2))
                weapon_num = int(input("Choose which weapon:"))
                if weapon_num == 2:
                    weapon = players[this_player].weapon2
            target = choose_target(level_grid, GRID_WIDTH, this_player, weapon.rows_in_range)

            print("Firing ",self.name," at ",target.name," using ",weapon.name)
            damage_dealt = target.take_damage(weapon.damage)
            print(target.name," takes ",damage_dealt," damage and has ", max(0,target.health)," health remaining")
            # If enemy is still alive, set it to retaliate against this player
            if target.health > 0:
                target.retaliate = True
                target.target = this_player
            # Else if enemy is dead and had loot, gain the loot
            elif isinstance(target.loot,Card):
                print("You gain the enemy's ", target.loot.name)
                if target.loot.type == "Weapon":
                    if not isinstance(players[this_player].weapon2,Card):
                        players[this_player].weapon2 = target.loot
                    else:
                        print("You have 1. ",players[this_player].weapon1.name," and 2: ",players[this_player].weapon2.name)
                        switch = int(input("Which would you like to switch for?"))
                        if switch == 1:
                            players[this_player].weapon1 = target.loot
                        elif switch == 2:
                            players[this_player].weapon2 = target.loot
                        else:
                            print(target.loot.name," was not taken")
                target.loot = 0
        elif self.name == "Enter Cover":
            players[this_player].in_cover = True
            print("You are now behind cover")
        elif self.name == "Tactical Movement":
            target = choose_target(level_grid, GRID_WIDTH, this_player, affect_cover=True)
            target.in_cover_to[this_player] = 0
            print(target.name," is no longer behind cover to ", players[this_player].name)

    def following_state(self):
        # Return the next state to go to after this card is chosen to be played
        if self.name == "Shot" or self.name == "Precision Shot" or self.name == "Stealth shot":
            return "TARGET CHOICE"
        elif self.name == "Enter Cover":
            return "PLAY CARD"
        elif self.name == "Tactical Movement":
            return "TARGET CHOICE"