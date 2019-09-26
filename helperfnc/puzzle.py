import random
from helperfnc.frank_generic import frank_function as ff


class eight_puzzle:
    """
    8 puzzle class
    """

    def __init__(self, board="b12345678"):
        self.board = board
        self.maxNode = 0

    def customSwap(self, i, j, input_str=""):
        """
        customSwap

        """
        if input_str == "":
            input_str = self.board
        input_str_list = list(input_str)
        input_str_list[i], input_str_list[j] = input_str_list[j], input_str_list[i]
        ff.customPrint(
            "Swapped: |"+input_str_list[i]+"| and |"+input_str_list[j]+"|", 2)
        return ''.join(input_str_list)

    def printState(self):
        try:
            ff.customPrint("Current Board State:", 1)
            ff.customPrint("+-----------+", 6)
            ff.customPrint(
                "| "+self.board[0]+" | "+self.board[1]+" | "+self.board[2]+" | ", 6)
            ff.customPrint(
                "| "+self.board[3]+" | "+self.board[4]+" | "+self.board[5]+" | ", 6)
            ff.customPrint(
                "| "+self.board[6]+" | "+self.board[7]+" | "+self.board[8]+" | ", 6)
            ff.customPrint("+-----------+", 6)
        except:
            ff.customPrint("Board State ERROR!", 5)
            exit(99)
        finally:
            ff.customPrint("Board State Print completed")

    #! Function used for easy method of setting the state of the board
    def setState(self, state):
        new_state = state.replace(" ", "")
        self.board = new_state
        ff.customPrint("State Set successfully!")
        self.printState()

    def maxNode(self, count):
        self.maxNode = count

    def findBlank(self):
        return self.board.find('b')

    def moveUp(self, ID, action):
        if (ID >= 3):
            outcome = self.customSwap(ID, ID-3)
            if action:
                self.setState(outcome)
            return 1, outcome
        else:
            return 3, ""

    def moveDown(self, ID, action):
        if (ID < 6):
            outcome = self.customSwap(ID, ID+3)
            if action:
                self.setState(outcome)
            return 1, outcome
        else:
            return 3, ""

    def moveLeft(self, ID, action):
        if not (ID % 3 == 0):
            outcome = self.customSwap(ID, ID-1)
            if action:
                self.setState(outcome)
            return 1, outcome
        else:
            return 3, ""

    def moveRight(self, ID, action):
        if not (ID % 3 == 2):
            outcome = self.customSwap(ID, ID+1)
            if action:
                self.setState(outcome)
            return 1, outcome
        else:
            return 3, ""

    def move(self, command, ID, action):
        status = -1
        ff.customPrint("Moving: "+command)
        if(command == 'up'):
            status, boardUpdated = self.moveUp(ID, action)
        if(command == 'down'):
            status, boardUpdated = self.moveDown(ID, action)
        if(command == 'left'):
            status, boardUpdated = self.moveLeft(ID, action)
        if(command == 'right'):
            status, boardUpdated = self.moveRight(ID, action)
        if (status == 1):
            if action:
                ff.customPrint("Move Success", 1)
            else:
                ff.customPrint("Plan success", 1)
            return 1,boardUpdated
        elif (status == 3):
            ff.customPrint("Not a valid move due to already at boarder", 2)
            return 3,""
        else:
            ff.customPrint(
                "Move failed for some unknown reason. Status: "+str(status), 0)
            return 99,""

    def isGoal(self):
        if self.board == "b12345678":
            return True
        else:
            return False

    def randomize(self, count):
        action_step = ""
        for i in range(count):
            success = False
            action = random.choice(["up", "down", "left", "right"])
            while not success:
                if self.move(action, self.findBlank(), False) == 1:
                    self.move(action, self.findBlank(), True)
                    success = True
                    action_step = action_step+action+", "
                else:
                    action = random.choice(["up", "down", "left", "right"])
        ff.customPrint("Randomize complete. Steps are:"+action_step, 1)

    def calculateHeuristic1(self,board=""):
        """
        h1 = the number of misplaced tiles.
        """
        heuristic1 = 0
        u = zip(self.board, "b12345678")
        for i, j in u:
            if (not i == j) and (not i == 'b'):
                heuristic1 = heuristic1 + 1
        ff.customPrint("Current Heuristic is "+str(heuristic1))
        return heuristic1

    def calculateHeuristic2(self,board=""):
        """
        h2 = the sum of the distances of the tiles from their goal positions.
        """
        heuristic2 = 0
        row_tracker = 1
        column_tracker = 0
        for i in self.board:
            if column_tracker != 3:
                column_tracker = column_tracker + 1
            else:
                column_tracker = 1
                if row_tracker != 3:
                    row_tracker = row_tracker + 1
                else:
                    row_tracker = 1

            #ff.customPrint("Current item "+str(i) + " Current row " +str(row_tracker)+" Current column "+str(column_tracker))

            if i != 'b':
                target_row = int(int(i)/3) + 1
                target_column = int(i) % 3 + 1
                #sff.customPrint("Current item "+str(i) + " Current row " +str(target_row)+" Current column "+str(target_column))
                heuristic2 = heuristic2 + \
                    abs(target_row-row_tracker) + \
                    abs(target_column-column_tracker)

            #ff.customPrint("Current Heuristic "+str(abs(target_row-row_tracker)+abs(target_column-column_tracker)))
        ff.customPrint("Current Heuristic is "+str(heuristic2))
        return heuristic2

    def listAvailable(self):
        potential = ["", "", "", ""]
        status1,potential[0] =self.move('up',self.findBlank(), False)
        status2,potential[1] =self.move('down',self.findBlank(), False)
        status3,potential[2] =self.move('left',self.findBlank(), False)
        status4,potential[3] =self.move('right',self.findBlank(), False)
        ff.customPrint("Available Option are: "+str(potential))
        return potential
