"""
Battleship game - by Albert Sun.  Python 3.5.1
10 x 10 grid game with 5 ships sizes 2, 3, 3, 4, 5
"""

import string
import random

class Battlegrid:
    def __init__(self):
        self.upper = string.ascii_uppercase[:10]
        self.letter2num = {self.upper[x]: x for x in range(len(self.upper))}
        self.mygrid = {self.upper[x]: [0 for y in range(10)] for x in range(len(self.upper))}
        self.enemygrid = {self.upper[x]: [0 for y in range(10)] for x in range(len(self.upper))}
        # [hits, size, sunk?, "name"] total of five ships
        self.myships = [[], [0, 2, False, "PT boat"], [0, 3, False, "Submarine"], [0, 3, False, "Destroyer"],
                        [0, 4, False, "Battleship"], [0, 5, False, "Aircraft Carrier"]]
        self.enemyships = [[], [0, 2, False, "PT boat"], [0, 3, False, "Submarine"], [0, 3, False, "Destroyer"],
                        [0, 4, False, "Battleship"], [0, 5, False, "Aircraft Carrier"]]
        self.hunting = False
        self.huntcoord = []
        self.adjacentships = 0
        self.adjacentcoords = []

    def showlegalpositions(self, somegrid, coords, shipsize):
        """
        given parameters, return a list of valid ship coordinates - check left = 0, right, up, down
        :param somegrid: specify which grid to check
        :param coords: starting coordinates to place ship [letter, number]
        :param shipsize: size of ship that is being checked
        :return: a list of potential valid ship ccordinates, from which "player" will choose one
        """
        valid_list = [True for x in range(4)]
        ret_list = []

        for x in range(shipsize):
            if coords[1]-x < 0:
                valid_list[0] = False
            elif somegrid[coords[0]][coords[1]-x] != 0:
                valid_list[0] = False
            if coords[1]+x > 9:
                valid_list[1] = False
            elif somegrid[coords[0]][coords[1]+x] != 0:
                valid_list[1] = False
            if self.letter2num[coords[0]] - x < 0:
                valid_list[2] = False
            elif somegrid[self.upper[self.letter2num[coords[0]] - x]][coords[1]]:
                valid_list[2] = False
            if self.letter2num[coords[0]] + x > 9:
                valid_list[3] = False
            elif somegrid[self.upper[self.letter2num[coords[0]] + x]][coords[1]]:
                valid_list[3] = False

        if valid_list[0]:
            ret_list.append([[coords[0], coords[1]-x] for x in range(shipsize)])
        if valid_list[1]:
            ret_list.append([[coords[0], coords[1]+x] for x in range(shipsize)])
        if valid_list[2]:
            ret_list.append([[self.upper[self.letter2num[coords[0]] - x], coords[1]] for x in range(shipsize)])
        if valid_list[3]:
            ret_list.append([[self.upper[self.letter2num[coords[0]] + x], coords[1]] for x in range(shipsize)])

        return ret_list

    def is_hit(self, coords, grid, shiplist, enemyobj):
        """
        checks if hit, updates relevant grids and shiplist
        :param coords: coordinates to check
        :param grid: grid to check
        :param shiplist: which shiplist to update
        :param enemyobj: enemy battlegrid, so hunting can be updated PRN, 99 = miss, 9 = hit
        :return:
        """
        if grid[coords[0]][coords[1]] == 0:
            grid[coords[0]][coords[1]] = 99
            print("Miss")
            enemyobj.enemygrid[coords[0]][coords[1]] = 99
            return False
        elif grid[coords[0]][coords[1]] % 10 == 0:
            print("Already hit there, so that's a 'Miss'")
            return False
        else:
            # hit - update ship status on grid, check if sunk
            print("Hit!!!!!")
            ship = grid[coords[0]][coords[1]]
            grid[coords[0]][coords[1]] *= 10
            shiplist[ship][0] += 1
            enemyobj.enemygrid[coords[0]][coords[1]] = 9
            enemyobj.hunting = True
            enemyobj.huntcoord.append(coords)
            if shiplist[ship][0] == shiplist[ship][1]:
                shiplist[ship][2] = True
                print(shiplist[ship][3] + " has been sunk.")
                if enemyobj.hunting:
                    if enemyobj.adjacentships > 0:
                        enemyobj.adjacentships -= 1
                        if enemyobj.adjacentships == 0:
                            enemyobj.adjacentcoords.clear()
                            enemyobj.hunting = False
                            enemyobj.huntcoord.clear()
                    else:
                        enemyobj.hunting = False
                        enemyobj.huntcoord.clear()
            return True

    def gameover(self, shiplist):
        """
        :param shiplist:
        :return: True if all ships in shiplist sunk
        """
        if all([shiplist[x][2] for x in range(1,6)]):
            return True
        else:
            return False

    def printgrid(self, grid):
        """
        prints out a grid_dictionary that is passed to it
        :param grid: grid dict - usually either self.mygrid or self.enemygrid
        :return: none
        current version prints just raw numeric code from grid - future implementation could use
        a function, e.g. convert(x) that would return a letter instead of number
        could also try using format to improve appearance
        """
        print("-"*23)
        print("|" + " " * 21 + "|")
        for letter in self.upper:
            templine = [letter + " "]
            for x in grid[letter]:
                if x == 9 or (x != 0 and x % 10 == 0):
                    templine.append("H" + " ")
                elif x == 99:
                    templine.append("M" + " ")
                elif x == 0:
                    templine.append(" " + " ")
                else:
                    templine.append(str(x) + " ")
            print("".join(templine) + "|")
            print("|" + " " * 21 + "|")
        templine = ["--"]
        for num in range(10):
            templine.append(str(num+1) + "-")
        print("".join(templine))

class PersonBattlegrid(Battlegrid):
    """
    inherits Battlegrid and adds player/person functionality
    """
    def placeships(self):
        print("Welcome to Battleship")
        print("---------------------\n")
        self.printgrid(self.mygrid)
        for x in range(1,6):
            print("Placing: {} Size{}.".format(self.myships[x][3], self.myships[x][1]))
            keepgoing = True
            while keepgoing:
                print("Enter a coordinate (letter A-J, number 1-10)")
                letter = input("Enter Letter: ").upper()
                try:
                    number = int(input("Then number: "))
                except ValueError:
                    print("make sure to enter a valid number")
                if (letter in self.upper) and (number in range(1, 11)):
                    keepgoing = False
                    if self.mygrid[letter][number-1] != 0:
                        keepgoing = True
                        print("That spot is occupied, try another coordinate.")
            print("Choose an orientation from the following list:")
            validpos = self.showlegalpositions(self.mygrid, [letter, number-1], self.myships[x][1])
            for posnumber in range(len(validpos)):
                tempstring = ""
                for tempcoord in validpos[posnumber]:
                    tempstring += "({}, {}), ".format(tempcoord[0], tempcoord[1]+1)
                print(str(posnumber) + ". " + tempstring)

            keepgoing = True
            while keepgoing:
                try:
                    choice = int(input("pick a number from the above list of valid ship positionings: "))
                    break
                except ValueError:
                    print("not a valid number, try again.")
                if choice in range(len(validpos)):
                    keepgoing = False
            for coord in validpos[choice]:
                self.mygrid[coord[0]][coord[1]] = x
            self.printgrid(self.mygrid)
            print("ok here's your grid after the ship placement.")

    def attack(self):
        """
        get coordinates - check if valid, return coords to caller
        :return: coords
        """
        keepgoing = True
        while keepgoing:
            print("Enter coordinates to attack:")
            letter = input("Enter letter (A-J): ").upper()
            try:
                number = int(input("Then number: "))
            except ValueError:
                print("make sure to enter a valid number")

            if (str(letter) in self.upper) and (number in range(1, 11)):
                keepgoing = False
            else:
                print("Not a valid coordinate choice, try again.")
            if self.enemygrid[letter][number-1] != 0:
                print("That spot has been attacked already, try another coordinate.")
                keepgoing = True
            return [letter, number-1]

    def gameover_message(self):
        posmessage = ["You win, nice shooting", "You win!!!",
                      "You have won this battle, but who will win the war?",
                      "Know thy enemy and know thyself and there is no danger in battle."]
        print(posmessage[random.randint(0, len(posmessage)-1)])

class AIBattleGrid(Battlegrid):
    """
    computer object - random selections of ship and AI directed ship attacking
    """

    probabilitygrid = [[['E', 5], ['E', 4], ['F', 5], ['F', 4]],
                       [['D', 3], ['D', 4], ['D', 5], ['D', 6], ['G', 3], ['G', 4], ['G', 5], ['G', 6],
                        ['E', 3], ['F', 3], ['E', 6], ['F', 6]],
                       [['C', 2], ['C', 3], ['C', 4], ['C', 5], ['C', 6], ['C', 7],
                        ['H', 2], ['H', 3], ['H', 4], ['H', 5], ['H', 6], ['H', 7],
                        ['D', 2], ['E', 2], ['F', 2], ['G', 2],
                        ['D', 7], ['E', 7], ['F', 7], ['G', 7]],
                       [['B', 1], ['B', 2], ['B', 3], ['B', 4], ['B', 5], ['B', 6], ['B', 7], ['B', 8],
                        ['I', 1], ['I', 2], ['I', 3], ['I', 4], ['I', 5], ['I', 6], ['I', 7], ['I', 8],
                        ['C', 1], ['D', 1], ['E', 1], ['F', 1], ['G', 1], ['H', 1],
                        ['C', 8], ['D', 8], ['E', 8], ['F', 8], ['G', 8], ['H', 8]],
                       [['A', 0], ['A', 1], ['A', 2], ['A', 3], ['A', 4], ['A', 5], ['A', 6], ['A', 7], ['A', 8],
                        ['A', 9], ['J', 0], ['J', 1], ['J', 2], ['J', 3], ['J', 4], ['J', 5], ['J', 6], ['J', 7],
                        ['J', 8], ['J', 9], ['B', 0], ['C', 0], ['D', 0], ['E', 0], ['F', 0], ['G', 0], ['H', 0],
                        ['I', 0], ['B', 9], ['C', 9], ['D', 9], ['E', 9], ['F', 9], ['G', 9], ['H', 9], ['I', 9],
                        ]]

    def placeships(self):

        for ship in range(1, 6):
            notdone = True
            while notdone:
                letter = self.upper[random.randint(0, 9)]
                number = random.randint(0, 9)
                if self.mygrid[letter][number] == 0:
                    choices = self.showlegalpositions(self.mygrid, [letter, number], self.myships[ship][1])
                    if choices != []:
                        selection = choices[random.randint(0, len(choices)-1)]
                        notdone = False
                        for coord in selection:
                            self.mygrid[coord[0]][coord[1]] = ship

    def attack(self):
        """
        if hunting, then search around huntcoord for orientation vertical or horizontal
        function returns [coordinates]
        """
        if self.hunting:
            if self.adjacentships > 0:
                while True:
                    coord = self.adjacentcoords.pop()
                    if self.enemygrid[coord[0]][coord[1]] == 0:
                        return [coord[0], coord[1]]

            if len(self.huntcoord) > 1:
                if self.huntcoord[0][0] == self.huntcoord[1][0]:
                    letter = self.huntcoord[0][0]
                    numlist = [self.huntcoord[x][1] for x in range(len(self.huntcoord))]
                    numlist.sort()
                    lowest = numlist[0]
                    highest = numlist[-1]
                    if lowest - 1 >= 0:
                        if self.enemygrid[letter][lowest - 1] == 0:
                            print("Hunting - Attacking: ({}, {})".format(letter, lowest))
                            return [letter, lowest - 1]
                    if highest + 1 <= 9:
                        if self.enemygrid[letter][highest + 1] == 0:
                            print("Hunting - Attacking: ({}, {})".format(letter, highest+2))
                            return [letter, highest + 1]
                    else:
                        # adjcent ship problem
                        print("Hunting... hmm... extra ships present.")
                        self.adjacentships += 1
                        self.adjacentcoords = [[[self.upper[self.letter2num[letter] + 1], x] for x in numlist
                          if self.letter2num[letter] + 1 <= 9], [[self.upper[self.letter2num[letter] - 1], x]
                                                                 for x in numlist if self.letter2num[letter] - 1 >= 0]]
                        while True:
                            coord = self.adjacentcoords.pop()
                            if self.enemygrid[coord[0]][coord[1]] == 0:
                                print("attacking ({}, {})".format(coord[0], coord[1] + 1))
                                return coord
                else:
                    numlist = [self.letter2num[self.huntcoord[x][0]] for x in range(len(self.huntcoord))]
                    numlist.sort()
                    lowest = numlist[0]
                    highest = numlist[-1]
                    number = self.huntcoord[0][1]
                    if lowest - 1 >= 0:
                        if self.enemygrid[self.upper[lowest - 1]][number] == 0:
                            print("Hunting - Attacking: ({}, {})".format(self.upper[lowest - 1], number + 1))
                            return [self.upper[lowest - 1], number]
                    if highest + 1 <= 9:
                        if self.enemygrid[self.upper[highest + 1]][number] == 0:
                            print("Hunting - Attacking: ({}, {})".format(self.upper[highest + 1], number + 1))
                            return [self.upper[highest + 1], number]
                    else:
                        # adjcent ship problem
                        print("Hunting... hmm... extra ships present.")
                        self.adjacentships += 1
                        self.adjacentcoords = [[[self.upper[x], number + 1] for x in numlist if number + 1 <= 9],
                                              [[self.upper[x], number - 1] for x in numlist if number - 1 >= 0]]
                        while True:
                            coord = self.adjacentcoords.pop()
                            if self.enemygrid[coord[0]][coord[1]] == 0:
                                print("attacking ({}, {})".format(coord[0], coord[1] + 1))
                                return coord

            else:
                letter = self.huntcoord[0][0]
                number = self.huntcoord[0][1]
                if number-1 >= 0:
                    if self.enemygrid[letter][number-1] == 0:
                        print("Hunting - Attacking: ({0}, {1})".format(letter, number))
                        return [letter, number-1]
                if self.letter2num[letter] - 1 >= 0:
                    if self.enemygrid[self.upper[self.letter2num[letter] - 1]][number] == 0:
                        print("Hunting - Attacking: ({0}, {1})".format(self.upper[self.letter2num[letter] - 1], number+1))
                        return [self.upper[self.letter2num[letter] - 1], number]
                if number+1 <= 9:
                    if self.enemygrid[letter][number+1] == 0:
                        print("Hunting - Attacking: ({0}, {1})".format(letter, number+2))
                        return [letter, number+1]
                if self.letter2num[letter] + 1 <= 9:
                    if self.enemygrid[self.upper[self.letter2num[letter] + 1]][number] == 0:
                        print("Hunting - Attacking: ({0}, {1})".format(self.upper[self.letter2num[letter] + 1], number+1))
                        return [self.upper[self.letter2num[letter] + 1], number]
                else:
                    print("something is wrong with hunting procedure.")
        else:
            notdone = True
            while notdone:
                number = random.randint(0, 4)
                coord = self.probabilitygrid[number][random.randint(0, len(self.probabilitygrid[number])-1)]
                if self.enemygrid[coord[0]][coord[1]] != 99 and self.enemygrid[coord[0]][coord[1]] != 9:
                    notdone = False
            print("Attacking: ({0}, {1})".format(coord[0],coord[1]+1))
            return coord

    def gameover_message(self):
        posmessage = ["Silicon dominates meat!", "Brutality!  Witness computer domination.",
                      "I win again.  Do you acknowledge my superiority?",
                      "When Alexander saw the breadth of his domain, he wept, for there were no more worlds to conquer."]
        print(posmessage[random.randint(0, len(posmessage)-1)])

def gameloop(me, you):
    """
    main game loop, takes 2 battlegrid objects as parameters
    is_hit method updates necessary grids
    :param me: the object that is being attacked
    :param you: the object doing the attacking - sending the attack coordinates
    :return: True if game-over
    """
    coord = you.attack()
    if me.is_hit(coord, me.mygrid, me.myships, you):
        if me.gameover(me.myships):
            me.gameover_message()
            print("-"*20)
            print("Thank you for playing Battleship.  See you next time.")
            return True
        else:
            return False
    else:
        return False

def main():
    """
    the main game loop
    create battlegrids, 2 for each 'player' - self and working grid
    get coordinates, check if hit, if game over
    """
    print("Welcome to Battleship - implemented by Albert Sun in Python 3.5.1")
    print("-----------------------------------------------------------------")
    print("1. player1 vs player2")
    print("2. player1 vs AI")
    print("3. AI vs AI")
    notdone = True
    while notdone:
        try:
            gametype = int(input("what type of game do you want (1-3): "))
        except ValueError:
            print("not valid, try again.")
        if gametype in range(1,4):
            notdone = False

    if gametype == 1:
        player1 = PersonBattlegrid()
        player2 = PersonBattlegrid()

        print("Player 1 goes... other player look away.")
        dummy = input("press a key to continue...")
        player1.placeships()

        print("Player 2 goes... other player look away.")
        dummy = input("press a key to continue...")
        player2.placeships()

        gameround = 1
        print("***********Round 1***********")
        if random.randint(1,2) == 1:
            print("Player 1 wins the coin toss and goes first... other player look away.")
            dummy = input("press a key to continue...")
            print("\n"*100)
            gameloop(player2, player1)
            print("enemy grid - representation of known player 1 field")
            player1.printgrid(player1.enemygrid)
            print("my grid - my ships and known events.")
            player1.printgrid(player1.mygrid)

        while True:
            print("Player 2 goes... other player look away.")
            dummy = input("press a key to continue...")
            print("\n"*100)
            if gameloop(player1, player2):
                print("Player 2 won!!")
                break
            print("enemy grid - representation of known player 1 field")
            player1.printgrid(player2.enemygrid)
            print("my grid - my ships and known events.")
            player1.printgrid(player2.mygrid)

            print("Player 1 goes... other player look away.")
            dummy = input("press a key to continue...")
            print("\n"*100)
            if gameloop(player2, player1):
                print("Player 2 won!!")
                break
            print("enemy grid - representation of known player 1 field")
            player1.printgrid(player1.enemygrid)
            print("my grid - my ships and known events.")
            player1.printgrid(player1.mygrid)

            gameround += 1
            print("This is round: {0}".format(gameround))
            print("*"*20)

    elif gametype == 2:
        player = PersonBattlegrid()
        player.placeships()
        computer = AIBattleGrid()
        computer.placeships()
        gameround = 1
        if random.randint(1,2) == 1:
            print("This is round: {0}".format(gameround))
            print("I win the coin flip - computer goes first")
            gameloop(player, computer)
            print("*"*20)
            print("My battlegrid with my ship placements")
            player.printgrid(player.mygrid)
        else:
            print("player wins the coin toss - you go first")
        while True:
            print("*"*20)
            print("Player goes...")
            if gameloop(computer, player):
                print("Player won!!")
                break
            print("*"*20)
            print("Enemy grid - representation of enemy battlegrid that you know so far")
            player.printgrid(player.enemygrid)
            print("*"*20)
            print("Computer AI goes...")
            dummy = input("press a key to continue...")
            if gameloop(player, computer):
                print("Computer won!!")
                break
            print("*"*20)
            print("My battlegrid with my ship placements")
            player.printgrid(player.mygrid)
            gameround += 1
            print("This is round: {0}".format(gameround))
            print("*"*30)

    else:
        computer1 = AIBattleGrid()
        computer1.placeships()
        computer2 = AIBattleGrid()
        computer2.placeships()

        if random.randint(1, 2) == 1:
            print("I win the coin flip - computer1 goes first")
            gameloop(computer2, computer1)
        else:
            print("computer 2 wins the coin toss and goes first")
        gameround = 1
        while True:
            print("computer 2 moves...")
            if gameloop(computer1, computer2):
                print("computer 2 won!!!!")
                break
            print("computer1 grid after comp2 moves")
            computer1.printgrid(computer1.mygrid)
            print("*" * 20)
            print("computer 1 moves...")
            if gameloop(computer2, computer1):
                print("Computer 1 won!!!")
                break
            print("Computer 2 grid after comp1 moves")
            computer2.printgrid(computer2.mygrid)
            print("-"*20)
            gameround += 1
            print("This is round: {0}".format(gameround))

if __name__ == "__main__":
    main()
