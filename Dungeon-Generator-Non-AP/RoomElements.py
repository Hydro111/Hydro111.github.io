#defualt python libraries
import random as r
import time



#buffs are in the form (ATK, DEF)
class Item:

  isBuff = False
  isUseable = False
  def __init__(self):
    pass

  def use(self, user):
    raise BaseException("The \"use\" method was called on an unuseable item or on the base Item class.")

  def on_pickup(self, player):
    pass



class RoomElement:

  description = ""
  name = ""
  def __init__(self):
    pass



class Enemy(RoomElement):

  xp:int = 0
  atk:float = 0.0
  defn:int = 0
  def __init__(self):
    pass

  def attack(self):
    pass

  def on_death(self, attacker):
    pass



class Object(RoomElement):

  item:Item = Item()
  canPickup:bool = True
  def __init__(self):
    pass














# Specific classes
class Gold(Object):

  description = "a pile of \33[92mgold\33[0m coins"
  name = "Gold"
  canPickup = True
  class Item(Item):

    name = "Gold"
    def __init__(self):
      pass

    def on_pickup(self, player):
      player.xp += 3
      player.update_stats()

  def __init__(self):
    pass



class SimpleSword(Object):

  description = "a simple, cast \33[92miron sword\33[0m"
  name = "Simple Sword"
  canPickup = True
  class Item(Item):

    name = "Simple Sword"
    isBuff = True
    buff = (3, 1)
    def __init__(self):
      pass

  def __init__(self):
    pass



class GoodSword(Object):
  description = "a regular, \33[92msteel sword\33[0m"
  name = "Good Sword"
  canPickup = True
  class Item(Item):

    name = "Good Sword"
    isBuff = True
    buff = (5, 2)
    def __init__(self):
      pass

  def __init__(self):
    pass



class GreatSword(Object):
  description = "a large, \33[92mchanneled steel sword\33[0m"
  name = "Greatsword"
  canPickup = True
  class Item(Item):

    name = "Greatsword"
    isBuff = True
    buff = (9, 3)
    def __init__(self):
      pass

  def __init__(self):
    pass



class PerfectSword(Object):
  description = "a \33[92mmysterious sword\33[0m, covered in glowing runes"
  name = "Magic Sword"
  canPickup = True
  class Item(Item):

    name = "Magic Sword"
    isBuff = True
    buff = (17, 7)
    def __init__(self):
      pass

  def __init__(self):
    pass



class SimpleArmor(Object):
  description = "a simple set of \33[92mchainmail\33[0m"
  name = "Chainmail"
  canPickup = True
  class Item(Item):

    name = "Chainmail"
    isBuff = True
    buff = (0, 2)
    def __init__(self):
      pass

  def __init__(self):
    pass



class GoodArmor(Object):
  description = "a set of \33[92mhalf-plate armor\33[0m"
  name = "Half-Plate"
  canPickup = True
  class Item(Item):

    name = "Half-Plate"
    isBuff = True
    buff = (1, 4)
    def __init__(self):
      pass

  def __init__(self):
    pass



class GreatArmor(Object):
  description = "a set of \33[92mfull plate armor\33[0m"
  name = "Plate Armor"
  canPickup = True
  class Item(Item):

    name = "Plate Armor"
    isBuff = True
    buff = (1, 9)
    def __init__(self):
      pass

  def __init__(self):
    pass



class PerfectArmor(Object):
  description = "a \33[92mcloak of metal scales\33[0m, emanating a blue glow"
  name = "Magic Armor"
  canPickup = True
  class Item(Item):

    name = "Magic Armor"
    isBuff = True
    buff = (5, 17)
    def __init__(self):
      pass

  def __init__(self):
    pass



class HealthPotion(Object):
  description = "a deep \33[92mred, glowing potion\33[0m"
  name = "Health Potion"
  canPickup = True
  class Item(Item):

    name = "Health Potion"
    isUseable = True
    
    def __init__(self):
      pass

    def use(self, user):
      user.hp = min(user.hp + 25, user.maxHp)
      print("You drink the health potion.")
      print(f"You now have {user.hp}/{user.maxHp} health!")
      user.inv.remove(self)

  def __init__(self):
    pass



class MaxHealthPotion(Object):
  description = "a \33[92mvial filled with gray, swirling liquid\33[0m"
  name = "Fortitude Potion"
  canPickup = True
  class Item(Item):

    name = "Fortitude Potion"
    isUseable = True
    
    def __init__(self):
      pass

    def use(self, user):
      user.hp += 25
      user.maxHp += 25
      print("You drink the fortitude potion.")
      print(f"You now have {user.hp}/{user.maxHp} health!")
      user.inv.remove(self)

  def __init__(self):
    pass



class WurmHeart(Item):
  
  name = "Wurm Heart"
  isBuff = True
  buff = (10, 10)

  def __init__(self):
    pass



class WyrmHeart(Item):
  
  name = "Wyrm Heart"
  isBuff = True
  buff = (50, 50)

  def __init__(self):
    pass



class WrmHeart(Item):
  
  name = "Wrm Heart"
  isBuff = True
  isUseable = True
  buff = (1000, 1000)

  def __init__(self):
    pass

  def on_pickup(self, player):
    print("Congratulations! You won the game!")
    time.sleep(2)
    while 1:
      inp = input("Would you like to continue? (yes) (no) ").lower()
      if inp == "yes":
        break
      elif inp == "no":
        print("Thank you for playing!")
        time.sleep(1.5)
        quit()
      else:
        print("Invalid command")

  def use(self, user):
    self.on_pickup(user)
    






class Wolf(Enemy):

  description = "a hungry, grey-furred \33[31mwolf\33[0m"
  name = "Wolf"
  xp = 2
  atk = 2
  defn = 2
  hp = 40

  def __init__(self):
    pass



class Troll(Enemy):

  description = "a hulking, mad-eyed \33[31mtroll\33[0m"
  name = "Troll"
  xp = 6
  atk = 7
  defn = 3
  hp = 125

  def __init__(self):
    pass



class Skeleton(Enemy):

  description = "a thin, chanmail clad living \33[31mskeleton\33[0m"
  name = "Skeleton"
  xp = 6
  atk = 5
  defn = 5
  hp = 60

  def __init__(self):
    pass

  def on_death(self, attacker):
    attacker.inv.append(SimpleSword.Item())
    attacker.inv.append(SimpleArmor.Item())
    attacker.update_stats()
    print("You take the skeleton's sword and chainmail")



class LivingArmor(Enemy):

  description = "a set of \33[31mliving plate armor\33[0m"
  name = "Living Armor"
  xp = 20
  atk = 8
  defn = 8
  hp = 150

  def __init__(self):
    pass

  def on_death(self, attacker):
    attacker.inv.append(GoodSword.Item())
    attacker.inv.append(GreatArmor.Item())
    attacker.update_stats()
    print("You take the now dormant armor and sword")



class Dragon(Enemy):

  description = "a massive, green scaled \33[31mdragon\33[0m sitting atop a pile of treasure"
  name = "Dragon"
  xp = 250
  atk = 26
  defn = 20
  hp = 1000

  lootTable = {
    Gold:4,
    HealthPotion:3,
    MaxHealthPotion:4,
    GoodSword:2,
    GreatSword:4,
    PerfectSword:3,
    GoodArmor:2,
    GreatArmor:4,
    PerfectArmor:3
  }
  lootItems = list(lootTable.keys())
  lootProbs = list(lootTable.values())

  def __init__(self):
    pass

  def on_death(self, attacker):
    loot = []
    for _ in range(12):
      choice = r.choices(self.lootItems, self.lootProbs)[0]
      #print(choice)
      loot.append(choice.Item())
    attacker.inv.extend(loot)
    attacker.update_stats()
    print("You take dragon's hoard, which consists of:")
    for item in loot:
      item.on_pickup(attacker)
      print(item.name)



class Worm(Enemy):

  description = "a pale skinned, tiny \33[31mworm\33[0m"
  name = "Worm"
  xp = 1
  atk = 1
  defn = 0
  hp = 5

  def __init__(self):
    pass



class Wurm(Enemy):

  description = "a gray scaled, large \33[31mwurm\33[0m with rough, pebbled skin"
  name = "Wurm"
  xp = 250
  atk = 20
  defn = 26
  hp = 1000

  def __init__(self):
    pass

  def on_death(self, attacker):
    deathItem = WurmHeart()
    attacker.inv.append(deathItem)
    deathItem.on_pickup(attacker)
    attacker.update_stats()
    print("You take the Wurm's heart")



class Wyrm(Enemy):

  description = "a massive, mile long \33[31mWyrm\33[0m, whose roars crumble the earth on which you stand"
  name = "Wyrm"
  xp = 1000
  atk = 45
  defn = 55
  hp = 3000

  def __init__(self):
    pass

  def on_death(self, attacker):
    deathItem = WyrmHeart()
    attacker.inv.append(deathItem)
    deathItem.on_pickup(attacker)
    attacker.update_stats()
    print("You take the Wyrm's heart")



class Wrm(Enemy):

  description = "a city-sized \33[31mWrm\33[0m, with jagged teeth the size of giants and a mouth the width of a river, long enough to encircle the earth"
  name = "Wrm"
  xp = 10000
  atk = 125
  defn = 140
  hp = 20000

  def __init__(self):
    pass

  def on_death(self, attacker):
    deathItem = WrmHeart()
    attacker.inv.append(deathItem)
    deathItem.on_pickup(attacker)
    attacker.update_stats()
    print("You take the Wrm's heart")