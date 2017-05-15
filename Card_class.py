from globals import *

#Main Card class
class Card:
    def __init__(self, name, type="Action",subtype=0,rows_in_range=[1,1,1,1],clip_size=0,health=99,num_targets=1,damage=0,text="", following_state=0):
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
        self.following_state = following_state

        #Enemy-specific variables
        self.in_cover_to = [0,0,0,0] # No players
        if self.name == "Shield guy":
            self.in_cover_to = [1,1,1,1] # All players
        self.retaliate = False
        self.target = 0
        self.loot = 0

    def take_damage(self,damage_taken):
        self.health = self.health - damage_taken
        if self.health < 0:
            self.health = 0
        return damage_taken

    def deal_damage(self, targets):
        targets.health = targets.health - self.damage

    def __str__(self):
        if self.type == "Enemy":
            return self.name + " H:" + str(self.health) + " D:" + str(self.damage)
        else:
            return self.name

    def action(self,gui,level_grid,target,players,this_player):
        # Perform the action of the card
        if self.name == "Shot" or self.name == "Precision Shot" or self.name == "Stealth shot":
            gui.DisplayAction("Firing "+self.name+" at "+target.name+" using "+players[this_player].weapon_equipped.name)
            damage_dealt = target.take_damage(players[this_player].weapon_equipped.damage)
            gui.DisplayAction(target.name+" takes "+str(damage_dealt)+" damage and has "+str(max(0,target.health))+" health remaining")
            # If enemy is still alive, set it to retaliate against this player
            if target.health > 0:
                target.retaliate = True
                target.target = this_player
            # Else if enemy is dead and had loot, gain the loot
            elif isinstance(target.loot,Card):
                gui.DisplayAction("You gain the enemy's "+target.loot.name)
                if target.loot.type == "Weapon":
                    if len(players[this_player].weapons)==1:
                        players[this_player].weapons.append(target.loot)
                    else:
                        gui.turn_state = "WEAPON SWITCH"
                        return target.loot
            return "CARD CHOICE"
        elif self.name == "Enter Cover":
            players[this_player].in_cover = True
            gui.DisplayAction("You are now behind cover")
        elif self.name == "Tactical Movement":
            target.in_cover_to[this_player] = 0
            gui.DisplayAction(target.name+" is no longer behind cover to "+players[this_player].name)
        elif self.name == "Adrenaline Injection":
            players[this_player].heal(self.damage)
            gui.DisplayAction(players[this_player].name + " now has " + str(players[this_player].health) + " health.")
        elif self.name == "First Aid":
            target.heal(self.damage)
            gui.DisplayAction(target.name + " now has " + str(players[this_player].health) + " health.")

        return "CARD CHOICE"