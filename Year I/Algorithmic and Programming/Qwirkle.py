import random
from pysnooper import snoop
from termcolor import colored
import pickle

AI = False
players = []
player = 0
score = [0,0]
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
shapes = ["rectangle", "circle", "heart",
        "triangle", "note", "cross"]

grid = [[]]
tiles = []
playersNum = 0

def start():
    global AI, players, colors, shapes, grid, tiles, playersNum
    playersNum = int(input("How many players will there be ?\n"))  # 1-4
    if playersNum == 1:
        AI = True
    colorsNum = int(
        input("How many colors do you want to play with ?\n"))  # 3-6
    shapesNum = int(
        input("How many shapes do you want to play with ?\n"))  # 3-6
    idemsNum = int(
        input("How many identical tiles do you want to play with ?\n"))  # 1-3
    players = [{"name": input(f"Please enter the name of player {i+1}: "),
                "score": 0, "hand": []} for i in range(playersNum)]
    for i in range(colorsNum):
        for j in range(shapesNum):
            tiles.append({"color": colors[i], "shape": shapes[j]})
    tiles = idemsNum * tiles
    for i in range(len(players)):
        for j in range(6):
            a = random.randint(0, len(tiles)-1)
            players[i]["hand"].append(tiles[a])
            tiles.pop(a)

start()

def countAttribute(player):
    best = 0
    for color in colors:
        current = 0
        for tile in players[player]["hand"]:
            if tile["color"] == color:
                current += 1
        if best < current:
            best = current
    for shape in shapes:
        current = 0
        for tile in players[player]["hand"]:
            if tile["shape"] == shape:
                current += 1
        if best < current:
            best = current
    return best

def whoBegins():
    global playersNum
    bestAtt,bestPla = 0,0
    for i in range(playersNum):
        a = countAttribute(i)
        if a > bestAtt:
            bestAtt,bestPla = a,i
    return bestPla

def display_shape(tile):
    if tile["shape"] == "rectangle":
        return "|■|"
    if tile["shape"] == "circle":
        return "|●|"
    if tile["shape"] == "heart":
        return "|♥|"
    if tile["shape"] == "triangle":
        return "|▲|"
    if tile["shape"] == "note":
        return "|♪|"
    if tile["shape"] == "cross":
        return "|✝|"

def display_color(tile):
    color = tile["color"]
    if color == "orange":
        color = "white"
    if color == "purple":
        color = "magenta"
    return color

def display_tile(tile):
    return colored(display_shape(tile),display_color(tile))

def display_hand(hand):
    display = ""
    for i in range(len(hand)):
        display += display_tile(hand[i])
    print(display)

def turn(player):
    n,p = 0,0
    player = (player + 1) % playersNum
     
    display_grid(grid)
    while p != 1:
        n = int(input(players[player]["name"] + ", what do you wish to do this turn ?\nEnter 1 to play,\n2 to trade some of your tiles for other ones,\n3 if you want to save your game.\n4 if you want to load a save.\n"))
        if n == 1:
            play(player,score)
            p = 1
        elif n == 2:
            trading(player)
            p = 1
        elif n == 3:
            save(players,grid,tiles)
            p = 1
        elif n == 4:
            load()
            p = 1

def display_grid(grid):
    coords,r = "",1
    for i in range(len(grid)+1):
        coords += str(i) + " "*r
        r = 2
    print(coords)
    i = 1
    for column in grid:
        s = ""
        for item in column:
            s += display_tile(item)
        print(str(i)+s)
        i+=1

def trading(player):
    trade,numbertiles,verification,tilechoice,p = "0",9,"3",9,0
    while p != 1: 
        trade = input("Do you want to trade (y/n) ?\n")
        if trade == "y":
            p = 1
        elif trade == "n":
            p = 1
    if trade == "n":
        turn(player)
    else:
        while tilechoice < 0 and tilechoice > 6:
            p = 0
            numbertiles = int(input("How many tiles do you want to trade ?\n"))
            while p != 1:
                verification = input("Are you sure (y/n)?\n")
                if verification == "y":
                    p = 1
                elif verification == "n":
                    p = 1                   
            if verification == "n":
                numbertiles = "9"
        for i in range(numbertiles):
            while  tilechoice < 0 and tilechoice > 5: 
                tilechoice = int(input("Which tile do you want to trade (0-5)?\n"))
            tiles.append(players[player]["hand"][tilechoice])
            players[player]["hand"].pop(tilechoice)
        for i in range(numbertiles):
            a = random.randint(0, len(tiles)-1)
            players[player]["hand"].append(tiles[a])
            tiles.pop(a)
        turn(player)

def play(player,score):
    v,tilechoice,c,end,mudae,line,p = 10,9,"f",False,0,[],0
    display_hand(players[player]["hand"])
    while p != 1:
        v = int(input("Please choose if you want to play with a color (1) or with a shape(2).\n"))
        if v == 1:
            p = 1
        elif v == 2:
            p = 1
    if v == 1:
        while end == False:
            p  = 0 
            while p != 1: 
                tilechoice = int(input("Which tile do you want to play (0-5)?\n"))
                if 0 <= tilechoice <= 5:
                    p = 1
            p = 0
            x = int(input("Where do you want to place your tile (x) ?\n"))
            y = int(input("Where do you want to place your tile (y) ?\n"))
            tile = players[player]["hand"][tilechoice]["color"]
            players[player]['hand'].pop(tilechoice)
            if (tile == grid[x-1][y]['shape'] or tile == grid[x+1][y]['shape'] or tile == grid[x][y-1]['shape'] or tile == grid[x][y+1]['shape']) and len(grid[x][y]) == 0:
                grid[x][y] = tile
            display_grid(grid)
            mudae += 1
            line.append(tile)
            while p != 0:
                c = str(input("Do you want to play more tiles (y/n) ?"))
                if c == "y":
                    p = 1
                elif c == "n":
                    p = 1   
            if c == "n" or len(players[player]["hand"]) == 0:
                end = True
    if v == 2:
        while end == False:
            p = 0
            while  p != 1: 
                tilechoice = int(input("Which tile do you want to play (0-5)?\n"))
                if 0 <= tilechoice <= 5:
                    p = 1
            p = 0                
            x = int(input("Where do you want to place your tile (x) ?\n"))
            y = int(input("Where do you want to place your tile (y) ?\n"))
            tile = players[player]["hand"][tilechoice]["shape"]
            players[player]['hand'].pop(tilechoice)
            if (tile == grid[x-1][y]['shape'] or tile == grid[x+1][y]['shape'] or tile == grid[x][y-1]['shape'] or tile == grid[x][y+1]['shape']) and len(grid[x][y]) == 0  :
                grid[x][y] = tile
            display_grid(grid)
            mudae += 1
            line.append(tile)
            while p != 1:
                c = str(input("Do you want to play more tiles (y/n) ?"))
                if c == "y":
                    p = 1
                elif c == "n":
                    p = 1   
            if c == "n" or len(players[player]["hand"]) == 0:
                end = True  
    for i in range(mudae):
        a = random.randint(0, len(tiles)-1)
        players[player]["hand"].append(tiles[a])
        tiles.pop(a)
    
    turn(player)   


def save(players,grid,tiles):
    pickle.dump((players,grid,tiles),open("save","wb"))

def load():
    players,grid,tiles = pickle.load(open("save","rb"))
    turn()


grid = []
display_grid(grid)
turn(player)
