import random
class puzzle:
    """
    8 puzzle class
    """

    def __init__(self, board, maxNodeCount):
        self.board = board
        self.maxNode = 0
        self.MINIMAL = False
        self.DEBUG = True

    def customPrint(self, input_str, level=0):
        """
        Parameters
        ----------
        input_str : str
            The text string you want to print it out. It must be a string.

        level : int
            The information level of the string.
        """
        message = str(input_str)
        if level == 0:
            if self.DEBUG:
                print("[DEBUG]"+message)
        elif level == 1:
            if not self.MINIMAL:
                print("[INFO]"+message)
        elif level == 2:
            print("[WARNING]"+message)
        elif level == 3:
            print("[ERROR]"+message)
        elif level == 4:
            print("[CRITICAL]"+message)
        elif level == 5:
            print("[FATAL]"+message)
        else:
            print(message)

    def customSwap(self, i, j, input_str=""):
        """
        customSwap

        """
        if input_str == "":
            input_str = self.board
        input_str_list = list(input_str)
        input_str_list[i], input_str_list[j] = input_str_list[j], input_str_list[i]
        self.customPrint(
            "Swapped: |"+input_str_list[i]+"| and |"+input_str_list[j]+"|", 2)
        return ''.join(input_str_list)

    def printState(self):
        try:
            self.customPrint("Current Board State:", 1)
            self.customPrint("+-----------+", 6)
            self.customPrint(
                "| "+self.board[0]+" | "+self.board[1]+" | "+self.board[2]+" | ", 6)
            self.customPrint(
                "| "+self.board[3]+" | "+self.board[4]+" | "+self.board[5]+" | ", 6)
            self.customPrint(
                "| "+self.board[6]+" | "+self.board[7]+" | "+self.board[8]+" | ", 6)
            self.customPrint("+-----------+", 6)
        except:
            self.customPrint("Board State ERROR!", 5)
            exit(99)
        finally:
            self.customPrint("Board State Print completed")

    def setState(self, state):
        self.board = state
        self.customPrint("State Set successfully!")
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
        self.customPrint("Moving: "+command)
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
                self.customPrint("Move Success", 1)
            else:
                self.customPrint("Plan success",1)
            return 1
        elif (status == 3):
            self.customPrint("Not a valid move due to already at boarder", 2)
            return 3
        else:
            self.customPrint("Move failed for some unknown reason. Status: "+str(status),0)
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
        self.customPrint("Randomize complete. Steps are:"+action_step,1)




puzzle = puzzle("b12345678",10000)        
for i in range(10000):
    puzzle.randomize(100)
    puzzle.printState()
    puzzle.setState("b12345678")

                

