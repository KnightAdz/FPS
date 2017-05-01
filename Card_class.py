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
        self.in_cover = False
        if self.name == "Shield guy":
            self.in_cover = True
        self.retaliate = False
        self.target = 0

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
            target = choose_target(level_grid, GRID_WIDTH, weapon.rows_in_range)

            print("Firing ",self.name," at ",target.name," using ",weapon.name)
            damage_dealt = target.take_damage(weapon.damage)
            print(target.name," takes ",damage_dealt," damage and has ", max(0,target.health)," health remaining")
            # If enemy is still alive, set it to retaliate against this player
            if target.health > 0:
                target.retaliate = True
                target.target = this_player
        elif self.name == "Enter Cover":
            players[this_player].in_cover = True
            print("You are now behind cover")
        elif self.name == "Tactical Movement":
            target = choose_target(level_grid, GRID_WIDTH)
            target.in_cover = False
            print(target.name," is no longer behind cover")

def choose_target(level_grid,GRID_WIDTH,rows_in_range=[1,1,1,1]):
    target = 0
    while target == 0:
        target_num = int(input("Choose a target:"))
        target_y = int(target_num / GRID_WIDTH)
        target_x = target_num - (target_y * GRID_WIDTH)
        target = level_grid[target_y][target_x]
        if isinstance(target,Card):
            if rows_in_range[target_y] == 0:
                print("Target is out of range of weapon, please choose another")
                target = 0
            else:
                if target.health <= 0:
                    print("Target is already dead, please choose another")
                    target = 0
        else:
            print("No target here, please select a target")
            target = 0
    return target