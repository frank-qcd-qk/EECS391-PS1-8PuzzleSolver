import random
from helperfnc.frank_generic import frank_function as ff

class eight_puzzle:
    """
    8 puzzle class
    """

    def __init__(self, board, maxNodeCount):
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

    def setState(self, state):
        self.board = state
        ff.customPrint("State Set successfully!")
        self.printState()

    def maxNode(self, count):
        self.maxNode = count

    def findBlank(self):
        return self.board.find('b')

    def moveUp(self, ID, action):
        if (ID >= 3):
            if action:
                outcome = self.customSwap(ID, ID-3)
                self.setState(outcome)
            return 1
        else:
            return 3

    def moveDown(self, ID, action):
        if (ID <6 ):
            if action:
                outcome = self.customSwap(ID, ID+3)
                self.setState(outcome)
            return 1
        else:
            return 3

    def moveLeft(self, ID, action):
        if not (ID % 3 == 0):
            if action:
                outcome = self.customSwap(ID, ID-1)
                self.setState(outcome)
            return 1
        else:
            return 3

    def moveRight(self, ID, action):
        if not (ID % 3 == 2):
            if action:
                outcome = self.customSwap(ID, ID+1)
                self.setState(outcome)
            return 1
        else:
            return 3

    def move(self, command, ID, action):
        status = -1
        ff.customPrint("Moving: "+command)
        if(command == 'up'):
            status = self.moveUp(ID, action)
        if(command == 'down'):
            status = self.moveDown(ID, action)
        if(command == 'left'):
            status = self.moveLeft(ID, action)
        if(command == 'right'):
            status = self.moveRight(ID, action)
        if (status == 1):
            if action:
                ff.customPrint("Move Success", 1)
            else:
                ff.customPrint("Plan success",1)
            return 1
        elif (status == 3):
            ff.customPrint("Not a valid move due to already at boarder", 2)
            return 3
        else:
            ff.customPrint("Move failed for some unknown reason. Status: "+str(status),0)
            return 99

    def isGoal(self):
        if self.board == "b12345678":
            return True
        else:
            return False

    def randomize(self,count):
        action_step = ""
        for i in range(count):
            success = False
            action = random.choice(["up", "down", "left", "right"])
            while not success:
                if self.move(action,self.findBlank(),False) == 1:
                    self.move(action,self.findBlank(),True)
                    success = True
                    action_step = action_step+action+", "
                else:
                    action = random.choice(["up", "down", "left", "right"])
        ff.customPrint("Randomize complete. Steps are:"+action_step,1)