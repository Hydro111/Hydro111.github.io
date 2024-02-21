#default python libraries
import random as r
import math
import time









rooms: set = set()
dir_to_xy: list = [(0, 1), (1, 0), (0, -1), (-1, 0)]
xy_to_dir: dict = {(0, 1):0, (1, 0):1, (0, -1):2, (-1, 0):3}

def entrances_to_symbol(enters: list):
  if enters == [0,0,0,0]: return "▢"
  if enters == [1,0,0,0]: return "╹"
  if enters == [0,1,0,0]: return "╺"
  if enters == [1,1,0,0]: return "┗"
  if enters == [0,0,1,0]: return "╻"
  if enters == [1,0,1,0]: return "┃"
  if enters == [0,1,1,0]: return "┏"
  if enters == [1,1,1,0]: return "┣"
  if enters == [0,0,0,1]: return "╸"
  if enters == [1,0,0,1]: return "┛"
  if enters == [0,1,0,1]: return "━"
  if enters == [1,1,0,1]: return "┻"
  if enters == [0,0,1,1]: return "┓"
  if enters == [1,0,1,1]: return "┫"
  if enters == [0,1,1,1]: return "┳"
  if enters == [1,1,1,1]: return "╋"
  raise BaseException("Entrances not formatted correctly, saw: \"" + str(enters) + "\"")




# Add in the collection of RoomElements
from RoomElements import *

# Create a function for ease of probability creation
def prob(diff, start, growSlope, maximum, end, shrinkSlope):
  return max( min( min( max( 0, (growSlope * diff) - start), maximum), -shrinkSlope * (diff-end) + maximum), 0)

# Create the list of elements and associated probabilities
def update_probs(diff):
  global elmsAndProbs
  global elmProbs
  global roomElms
  elmsAndProbs = {
    0:150,
    Gold:16,
    Wolf:            prob( diff, 4,   2,  30, 10, 2),
    Skeleton:        prob( diff, 5,   2,  30, 14, 2),
    Troll:           prob( diff, 5,   2,  30, 14, 2),
    LivingArmor:     prob( diff, 8,   2,  30, 20, 2),
    Dragon:          prob( diff, 20,  2,  30, 24, 2),
    Worm:            prob( diff, 1,   15, 15, 3, 15),
    Wurm:            prob( diff, 20,  2,  20, 24, 2),
    Wyrm:            prob( diff, 26,  2,  30, 30, 2),
    Wrm:             prob( diff, 30,  1,  90, 99, -9),
    SimpleSword:     prob( diff, -10, 2,  20, 4,  1),
    GoodSword:       prob( diff, 0,   1,  20, 16, 1),
    GreatSword:      prob( diff, 8,   1,  20, 24, 1),
    PerfectSword:    prob( diff, 10,  .3, 30, 99, -9),
    SimpleArmor:     prob( diff, -10, 2,  20, 4,  1),
    GoodArmor:       prob( diff, 0,   1,  20, 16, 1),
    GreatArmor:      prob( diff, 8,   1,  20, 24, 1),
    PerfectArmor:    prob( diff, 10,  .3, 30, 99, -9),
    HealthPotion:    prob( diff, 0,   1,  40, 99, -9),
    MaxHealthPotion: prob( diff, 8,   1,  40, 99, -9)
  }
  elmProbs = list(elmsAndProbs.values())
  roomElms = list(elmsAndProbs.keys())

update_probs(0)


class Room ():


  def __init__(self, x, y, entrances = [-1, -1, -1, -1], randGenConts = True):
    #remember args are passed by refrence
    self.contents = []
    self.adjacents = []
    self.entrances = entrances.copy()
    

    if self.entrances == [-1, -1, -1, -1]:
      netPosFlag = False
    else:
      netPosFlag = True
    
    indexList = list(range(0,4))
    r.shuffle(indexList)
    for i in indexList:
      if self.entrances[i] == -1:
        if netPosFlag:
          self.entrances[i] = r.randint(0,1)
        else:
          self.entrances[i] = math.ceil(r.randint(0,5)/10.0)
          if self.entrances[i] == 1:
            netPosFlag = True
    

    # V Testing code, should not be in final version
    #self.entrances = [1,1,1,1]
    

    for i in range(0,4):
      adj = Room.get_room(
        x + dir_to_xy[i][0], 
        y + dir_to_xy[i][1], 
        False)
      if adj != -1:
        self.adjacents.append(adj)
        adj.adjacents[ (i+2) % 4 ] = self

        #ensures proper connections
        self.entrances[i] = adj.entrances[ (i+2) % 4 ]
      else:
        self.adjacents.append(-1)
    
    self.x = x
    self.y = y

    if randGenConts:
      update_probs(abs(self.x) + abs(self.y))
      for i in range(8):
        choice = r.choices(roomElms, elmProbs)[0]
        if choice != 0:
          self.contents.append(choice())
          if choice == Dragon or choice == Wurm or choice == Wyrm or choice == Wrm:
            break

    self.update_description()
    
    rooms.add(self)
  

  def get_room(x, y, error_out = True, checkOnly = False):
    for ro in rooms:
      if ro.x == x and ro.y == y:
        if checkOnly:
          return 1
        else:
          return ro
    if error_out:
      raise IndexError("No such room exists at (" + str(x) + ", " + str(y) + ")")
    else:
      return -1
  

  def update_description(self):
    self.description = "You see a room containing "
    if len(self.contents) == 0:
      self.description += "nothing"
    else:
      words = self.contents.copy()
      for i in range(len(words)):
        words[i] = words[i].description
      if len(self.contents) >= 2:
        words[-1] = "and " + words[-1]
      self.description += ", ".join(words)
    self.description += "."

  
  def map_string():
    xFromCenter = 0
    yFromCenter = 0
    roomArray = [[" "]]
    resultString = ""

    def room_op(room):
      nonlocal xFromCenter
      nonlocal yFromCenter
      nonlocal roomArray
      while room.x < xFromCenter:
        for i in range(len(roomArray)):
          roomArray[i] = [" "] + roomArray[i]
        xFromCenter -= 1
      while room.y < yFromCenter:
        roomArray = [[" "]*len(roomArray[0])] + roomArray
        yFromCenter -= 1
      
      while len(roomArray) + yFromCenter <= room.y:
        roomArray.append([" "] * len(roomArray[0]))
      while len(roomArray[0]) + xFromCenter <= room.x:
        for row in roomArray:
          row.append(" ")

      # Test if the room has the player in it and color accoridngly
      if player.room is room:
        room_symb = "\033[92m"+ entrances_to_symbol(room.entrances) +"\033[0m"
      else:
        room_symb = entrances_to_symbol(room.entrances)
      roomArray[room.y - yFromCenter][room.x - xFromCenter] = room_symb

    room_op(orgin)

    for room in rooms:
      if not (room.x == 0 and room.y == 0):
        room_op(room)
    
    roomArray.reverse()

    for row in roomArray:
      for room in row:
        resultString += room
      resultString += "\n"
    
    return resultString









class Player ():


  def __init__(self, x: int, y: int):
    self.room = Room.get_room(x, y)
    self.x = self.room.x
    self.y = self.room.y
    self.inv = []
    self.baseStats = [1,1]
    self.atk = self.baseStats[0]
    self.defn = self.baseStats[1]
    self.maxHp = 100
    self.hp = self.maxHp
    self.xp = 0
    self.xpGoal = 2
    self.level = 0
    


  def combat(self):
    print("\n\nYou enter combat!\n")
    while 1:
      # Player turn
      while 1:
        inp = input("What do you do? (attack) (use) (run) (help) ")
        
        if inp == "help" or inp == "h":
          enmStrs = []
          for elm in self.room.contents:
            if issubclass(type(elm), Enemy):
              enmStrs.append(elm.name)
          
          print("Enemies: " + ", ".join(enmStrs))
          print("An attack deals a random ammount of damage, some of the time, to an enemy of your choice. How much damage and how likely you are to hit is dependent on your attack score. You can also use an item, with varying results depending on the item. If you choose to run, there is a random chance you are succesful, leaving the room. After you take an action, each enemy in the room attacks you. You must input the direction they are attacking from in time to block the attack. You can use items durring combat.")
          continue

        elif inp == "run" or inp == "r":
          if r.randint(1,3) == 3:
            print("You succesfully escape!")
            while 1:
              inp = input("Where do you run to? (wasd) ").lower()
              result = 0
              if inp == "w":
                result = player.move_dir(0)
              
              if inp == "d":
                result = player.move_dir(1)
            
              if inp == "s":
                result = player.move_dir(2)
              
              if inp == "a":
                result = player.move_dir(3)
  
              if result == -1:
                print("There is no door this way.")
              elif result == 0:
                print("Invalid command.")
              else:
                return
          else:
            print("You are not able to escape this time.")

        elif inp == "use" or inp == "u":
          itemsStr = ""
          itemsConts = {}
          for elm in player.inv:
            if elm.isUseable:
              itemsStr += f"({elm.name}) "
              itemsConts[elm.name.lower()] = elm

          backFlag = False
          while True:
            print("What do you use? ")
            useInp = input(itemsStr + "(back) ").lower()
            if useInp == "back":
              backFlag = True
              break
            try:
              useItem = itemsConts[useInp]
              break
            except KeyError:
              print("You have no such item to use.")
          if backFlag:
            continue
          useItem.use(player)
        
        elif inp == "attack" or inp == "a":
          enmsStr = ""
          enmConts = {}
          for elm in player.room.contents:
            if issubclass(type(elm), Enemy):
              enmsStr += f"({elm.name}) "
              enmConts[elm.name.lower()] = elm

          backFlag = False
          while True:
            print("What do you attack? ")
            atkInp = input(enmsStr + "(back) ").lower()
            if atkInp == "back":
              backFlag = True
              break
            try:
              target = enmConts[atkInp]
              break
            except KeyError:
              print("There is no such enemy to attack.")
          if backFlag:
            continue
          hit = False
          for i in range(player.atk):
            if r.randint(0,target.defn) == 0:
              hit = True
              break
          if hit:
            damage = 0
            for i in range(player.atk):
              damage += r.randint(1,6)
            target.hp -= damage
            print(f"You hit and dealt {damage} damage{(target.hp <= 0) * ', eliminating your target'}!")
            if target.hp <= 0:
              target.on_death(player)
              player.room.contents.remove(target)
              player.xp += target.xp
              player.update_stats()
          else:
            print("You missed!")
          
              
          
        else:
          continue
        break


      for elm in player.room.contents:
        if issubclass(type(elm), Enemy):
          print(f"The {elm.name} prepares to attack...")
          atkDir = ["top", "right", "left", "center"][r.randint(0,3)]
          time.sleep(r.randint(10, 30)/10.0)
          start = time.time()
          block = input(f"The attack comes from the {atkDir}! ({atkDir}) ").lower()
          stop = time.time()
          if block == atkDir and stop - start < (player.defn / elm.atk)+1:
            print("You block succesfully!")
          else:
            damage = 0
            for i in range(elm.atk):
              damage += r.randint(1,6)
            player.hp -= damage
            print(f"You are hit and take {damage} damage!")
            if player.hp <= 0:
              print("You succumb to your wounds...")
              time.sleep(1.5)
              print("Thank you for playing!")
              quit()
              

      #print(player.room.contents)
      enemyExists = False
      for elm in player.room.contents:
        if issubclass(type(elm), Enemy):
          #print("enemy!")
          enemyExists = True
          break
      if not enemyExists:
        #print("breaking!")
        break
            
        
  
  
  def inventory(self):
    self.update_stats()
    invStrs = []
    for item in self.inv:
      invStrs.append(item.name)
    print(f"You have: "+", ".join(invStrs))
    print(f"Attack score: {self.atk}")
    print(f"Defense score: {self.defn}")
    print(f"Health: {self.hp}/{self.maxHp}")
    print(f"Experience: {self.xp}/{self.xpGoal}")
  

  def move_dir(self, dir: int):
    return self.move_vec(dir_to_xy[dir])


  def move_vec(self, movement: tuple):

    if (self.room.entrances[xy_to_dir[movement]] != 1):
      return -1

    if self.room.adjacents[xy_to_dir[movement]] == -1:
      new_room = Room(
        self.x + movement[0],
        self.y + movement[1]
        )
    else:
      new_room = Room.get_room(
        self.x + movement[0],
        self.y + movement[1])
    
    new_room.entrances[(xy_to_dir[movement]+2) % 4] = 1
    self.room = new_room
    self.update_xy()

    
  

  def update_stats(self):
    while self.xp >= self.xpGoal:
      self.baseStats[0] += 1
      self.baseStats[1] += 1
      self.xp -= self.xpGoal
      self.xpGoal = math.ceil(1.2 * self.xpGoal)
      self.hp += 10
      self.maxHp += 10
      self.level += 1
      print()
      print("You leveled up!")
      print(f"You are now level {self.level}")
      print(f"New base attack: {self.baseStats[0]}")
      print(f"New base defense: {self.baseStats[1]}")
      print(f"New health: {self.hp}/{self.maxHp}")
      print(f"XP needed for next level: {self.xpGoal}")
      print()
    self.atk = self.baseStats[0]
    self.defn = self.baseStats[1]
    typesUsed = set()
    for item in self.inv:
      assert issubclass(type(item), Item)
      if item.isBuff and not type(item) in typesUsed:
        typesUsed.add(type(item))
        self.atk += item.buff[0]
        self.defn += item.buff[1]

  def update_xy(self):
    self.x = self.room.x
    self.y = self.room.y





  


  






orgin = Room(0, 0, [1,1,1,1], False)


      
player = Player(0,0)

while 1:
  player.update_xy()
  #print(player.x)
  #print(player.y)
  #print(entrances_to_symbol(player.room.entrances))
  print()
  print(Room.map_string())
  print(player.room.description)
  print()
  for elm in player.room.contents:
      if issubclass(type(elm), Enemy):
        player.combat()
        player.room.update_description()
        print()
        print(Room.map_string())
        print(player.room.description)
        break
  inp = input("What do you do? (wasd) (pickup) (inventory) (use) ").lower()
  
  # test code
  if inp == "wrrrrrm":
    player.inv.append(SimpleArmor.Item())
    player.inv.append(SimpleSword.Item())
    player.inv.append(GoodArmor.Item())
    player.inv.append(GoodSword.Item())
    player.inv.append(GreatArmor.Item())
    player.inv.append(GreatSword.Item())
    player.inv.append(PerfectArmor.Item())
    player.inv.append(PerfectSword.Item())
    player.inv.append(WurmHeart())
    player.inv.append(WyrmHeart())
    player.xp += 10000
    player.maxHp += 125
    player.hp += 125
    player.update_stats()
    #player.atk += 100000
    player.room.contents.append(Wrm())
  result = 0
  if inp == "w":
    result = player.move_dir(0)
  
  if inp == "d":
    result = player.move_dir(1)

  if inp == "s":
    result = player.move_dir(2)
  
  if inp == "a":
    result = player.move_dir(3)

  if inp == "inventory" or inp == "i":
    result = 1
    player.inventory()

  if inp == "use" or inp == "u":
    result = 1
    itemsStr = ""
    itemsConts = {}
    for elm in player.inv:
      if elm.isUseable:
        itemsStr += f"({elm.name}) "
        itemsConts[elm.name.lower()] = elm

    backFlag = False
    while True:
      print("What do you use? ")
      useInp = input(itemsStr + "(back) ").lower()
      if useInp == "back":
        backFlag = True
        break
      try:
        useItem = itemsConts[useInp]
        break
      except KeyError:
        print("You have no such item to use.")
    if backFlag:
      continue
    useItem.use(player)
  
  if inp == "pickup" or inp == "p":
    result = 1
    contsStr = ""
    pickConts = {}
    allConts = []
    for elm in player.room.contents:
      if issubclass(type(elm), Object) and elm.canPickup:
        contsStr += f"({elm.name}) "
        pickConts[elm.name.lower()] = elm
        allConts.append(elm)
    if len(pickConts) == 0:
      print("There's nothing to pick up here.")
    else:
      contsStr += "(all) (back) "
      while True:
        print("What do you pick up? ")
        pickupInp = input(contsStr).lower()
        if pickupInp == "back":
          break
        if pickupInp == "all" or pickupInp == "a":
          
          for cont in allConts:
            item = cont.Item()
            player.inv.append(item)
            player.room.contents.remove(cont)
            item.on_pickup(player)
          player.room.update_description()
          player.update_stats()
          break
        try:
          item = pickConts[pickupInp].Item()
          player.inv.append(item)
          player.room.contents.remove(pickConts[pickupInp])
          item.on_pickup(player)
          player.room.update_description()
          player.update_stats()
          break
        except KeyError:
          print("There is no such item to pickup.")
      
    
        

  if result == -1:
    print("There is no door this way.")
  elif result == 0:
    print("Invalid command.")


