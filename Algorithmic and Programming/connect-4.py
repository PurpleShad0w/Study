import sys
print("Please enter the length of desired grid")
n = int(input())
p = 1

while n < 4:
    print("Really, how do you want to play on this kind of grid ?")
    n = int(input())


def make_grid(n):
    grid = [[-1 for i in range(n)] for j in range(n)]
    return(grid)


def display_grid(grid):
    for i in range(n):
        dis = " "
        for j in range(n):
            if grid[i][j] == 1:
                dis = dis + "X"
            elif grid[i][j] == 2:
                dis = dis + "O"
            else:
                dis = dis + "•"
            dis = dis + " "
        print(dis)


grid = make_grid(n)
display_grid(grid)

def turn(grid):
    global p, h
    print("")
    print("Time for player {} to play".format(p))
    d = int(input())-1
    h = n-1
    if 0 <= d < n:
        while grid[h][d] != -1 and h != 0:
            h -= 1
        if grid[h][d] != -1 and h == 0:
            print("You cannot place a disc here")
            display_grid(grid)
            turn(grid)
        else:
            if p == 1:
                grid[h][d] = 1
                display_grid(grid)
                grid = rot(grid, n)
                wiener(n, grid)
                p = 2
                return(grid, turn(grid))
            else:
                grid[h][d] = 2
                display_grid(grid)
                grid = rot(grid, n)
                wiener(n, grid)
                p = 1
                return(grid, turn(grid))
    else:
        print("Please retry")
        return(turn(grid))

def wiener(n, grid):
    l = n-1
    for i in range(n):
        for j in range(n-3):
            if grid[i][j] == grid[i][j+1] == grid[i][j+2] == grid[i][j+3] and grid[i][j] != -1:
                sys.exit("Good job player {} !\nSayonara~~".format(p))
    for i in range(n-3):
        for j in range(n):
            if grid[i][j] == grid[i+1][j] == grid[i+2][j] == grid[i+3][j] and grid[i][j] != -1:
                sys.exit("Good job player {} !\nThank you for playing !".format(p))
    for i in range(n-3):
        for j in range(n-3):
            if grid[i][j] == grid[i+1][j+1] == grid[i+2][j+2] == grid[i+3][j+3] and grid[i][j] != -1:
                sys.exit("Good job player {} !\nSee you next time~~".format(p))
    while l > 2:
        for j in range(n-3):
            if grid[l][j] == grid[l-1][j+1] == grid[l-2][j+2] == grid[l-3][j+3] and grid[l][j] != -1:
                sys.exit("Good job player {} !\nDid you like your spaghettis?".format(p))
        l -= 1

def rot(grid, n):
    r = int(input("Choose the number of rotation:\n"))
    grid2 = grid
    if r != 0:
        for u in range(r):  # pates
            if u > 0:  # bolognaise
                grid = grid2
            grid2 = make_grid(n)
            for j in range(n):
                for i in range(n):
                    grid2[i][j] = grid[n - j - 1][i]
            for muda in range(n):  # boulettes
                for i in range(len(grid2)-1):
                    for j in range(len(grid2[i])):
                        if grid2[i+1][j] == -1 and grid2[i][j] != -1:
                            grid2[i+1][j] = grid2[i][j]
                            grid2[i][j] = -1
    display_grid(grid2)
    return grid2

turn(grid)
