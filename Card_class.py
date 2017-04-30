#Main Card class
class Card:
    def __init__(self, name, type="Action",subtype=0,rows_in_range=[1,1,1,1],clip_size=0,health=99,num_targets=1,damage=0,text="",):
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

    def take_damage(self,damage_taken):
        self.health = self.health - damage_taken

    def deal_damage(self, targets):
        targets.health = target.health - self.damage

    def __str__(self):
        return self.name

    #def load_from_file(self):
        # Load card attributes from csv file

#Enemy card is a subclass of Card
#class EnemyCard(Card):
#    def __init__(self,name,damage=1,health=1):
#        Card.__init__(self,name,0,damage,health,type="Enemy")
#        self.col_location=0
#        self.row_location=0
#        self.col_target=0

#    def assign_location(self,row,col):
#        self.row_location = row
#        self.col_location = col

#Equipment card
#class EquipCard(Card):
#    def __init__(self,name,type,damage=1, clip_size=0,armour=0):
#        Card.__init__(self, name, 0, damage, type)
#        self.rows_in_range = [1,1,0,0]
        #Guns will have clip_size > 0 to determine how many cards are drawn
#        self.clip_size = clip_size
#        self.armour = armour

    #Armour card

    #Grenade card



#Action card
#class ActionCard(Card):
#    def __init__(self,name,cost):
#        Card.__init__(self,name,cost,0,0,type="Action")



#Shot

#Precision shot


#isinstance(varaible,Action_card)