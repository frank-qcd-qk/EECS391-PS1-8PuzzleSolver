from helperfnc.puzzle import eight_puzzle
from helperfnc.frank_generic import frank_function as ff
import sys
from decimal import Decimal

def ingest(fileLocation):
    operation = []
    try:
        with open(fileLocation, 'r') as schema:
            for line in schema:
                operation.append(line)
    except:
        ff.customPrint("File command not found! Please check path", 5)
        exit(99)
    finally:
        ff.customPrint("Commands open successfully.")
    return operation

def checkInit(initialized):
    if not initialized:
        ff.customPrint(
            "Board still not initialized! Using default!", 4)

def astar(boardClass, heruisticsOption, maxNodes):
    start = boardClass.getState()
    actionSquence = []
    actionRecall = []
    visited = []
    while not boardClass.isGoal():
        if len(actionRecall)>maxNodes:
            ff.customPrint("Error! Exceed Max Nodes!")
            exit(99)
        options = boardClass.listAvailable()
        heruistics = []
        indextable = ["left","right","up","down"]
        for option in options:
            if(option != "") and (not option in actionRecall):
                if heruisticsOption =='h1':
                    heruistics.append(boardClass.calculateHeuristic1(option))
                else:
                    heruistics.append(boardClass.calculateHeuristic2(option))
            else:
                heruistics.append(Decimal('Infinity'))
        ff.customPrint("option heruistics are: "+str(heruistics),1)
        ff.customPrint("optional choice are: "+str(options),1)
        
        #! Handle same heruistics problem
        newOptions = []
        newHeuristics = []
        newIndexTable = []
        for i in range(4):
            if heruistics[i] == min(heruistics):
                newOptions.append(options[i])
                newHeuristics.append(heruistics[i])
                newIndexTable.append(indextable[i])

        ff.customPrint("Current Potential Option: "+str(newOptions),1)
        ff.customPrint("Current Potential heruistics: "+str(newHeuristics),1)
        ff.customPrint("Current Step Index: "+str(newIndexTable),1)

        if len(newOptions)>1:
            for i in range(len(newOptions)):
                testSuccessor = eight_puzzle()
                testSuccessor.setState(newOptions[i])
                try:
                    tbd = testSuccessor.listAvailable()
                except:
                    return[0]
                testHeuristics = []
                for testcase in options:
                    if(testcase != "") and (not testcase in actionRecall):
                        if heruisticsOption =='h1':
                            testHeuristics.append(boardClass.calculateHeuristic1(option))
                        else:
                            testHeuristics.append(boardClass.calculateHeuristic2(option))
                    else:
                        testHeuristics.append(Decimal('Infinity'))
                newHeuristics[i] = min(testHeuristics)
                ff.customPrint("Current test heruistics for : "+str(i)+" is "+str(testHeuristics),1)


        ff.customPrint("Current New heruistics: "+str(newHeuristics),1)
        nextOptionID = newHeuristics.index(min(newHeuristics))
        actionSquence.append(newIndexTable[nextOptionID])
        try:
            boardClass.setState(newOptions[nextOptionID])
        except:
            return [0]
        ff.customPrint("State Changed! Now:"+str(options[nextOptionID]))
        actionRecall.append(newOptions[nextOptionID])

    ff.customPrint("Steps: "+ str(len(actionSquence)) +" Action is:"+str(actionSquence),2)
    return actionSquence

def beam(boardClass,k):
    openList =[]
    visitedList = []
    parents = []
    successorTester = eight_puzzle()
    movementCost = 0

    openList.append(boardClass.getState())
    visitedList.append(boardClass.getState())


    while len(openList)>0:
        movementCost += 1
        board = openList.pop(0)

        if board=="b12345678":
            break;

        if (len(visitedList)>maxNodes):
            ff.customPrint("Exceed Maximum allowed exploration! Quit!",5)
            exit(99)
        
        successorTester.setState(board)
        potential = successorTester.listAvailable()
        for option in potential:
            if option != '':
                successorTester.calculateHeuristic2(option)
            
                if((option not in visitedList) and (option not in openList)):
                    openList.append(option)
                    visitedList.append(option)

def demo(before,actionSquence):
    ff.customPrint("====================Result Demo====================",6)
    demoBoard = eight_puzzle(before)
    ff.customPrint("Start with: ",6)
    demoBoard.printState()
    for action in actionSquence:
        if action == 0:
            ff.customPrint("NO result solved!",4)
            return
        ff.customPrint("Moving "+str(action),6)
        demoBoard.move(action,demoBoard.findBlank(),True)
        demoBoard.printState()

#! Start of the program:
try:
    commandfile = sys.argv[1]
except:
    commandfile = ".\command.txt"

commandList = ingest(commandfile)
#! Class initialization
current = eight_puzzle()
initialized = False
maxNodes = 181440
#! Command Operation
for command in commandList:
    operation = command.split()
    if operation == []:
        continue
    if operation[0] == "setState":
        ff.customPrint("setState Operation called", 2)
        if (len(operation[1]) == 9):
            current.setState(operation[1])
            initialized = True
        elif (len(operation[1]) == 3):
            try:
                state = ""+operation[1]+operation[2]+operation[3]
            except:
                ff.customPrint(
                    "setState command failed. Provided state missing component!", 5)
            current.setState(state)
            initialized = True
        else:
            ff.customPrint(
                "setState command provided a state not recognized!", 5)
            exit(99)
    elif operation[0] == "printState":
        ff.customPrint("printState operation called", 2)
        checkInit(initialized)
        current.printState()
    elif operation[0] == "move":
        if operation[1] == "up" or operation[1] == "down" or operation[1] == "left" or operation[1] == "right":
            ff.customPrint("Moving "+str(operation[1])+"!",2)
            checkInit(initialized)
            current.move(operation[1],current.findBlank(),True)
    elif operation[0] == "randomizeState":
        ff.customPrint("randomizeState command called",2)
        try:
            count = int(operation[1])
            ff.customPrint("Request: "+str(count)+" steps",2)
        except:
            ff.customPrint("Randomize state did not specify step count!",5)
            exit(99)
        else:
            checkInit(initialized)
            current.randomize(count)
    elif operation[0] == "solve":
        before = current.getState()
        if operation[1]=="A-star":
            ff.customPrint("solve A-star command called",2)
            if operation[2]=="h1":
                ff.customPrint("using h1 heuristic",2)
                action = astar(current, "h1",maxNodes)
                demo(before,action)
            if operation[2]=="h2":
                ff.customPrint("using h2 heuristic",2)
                action = astar(current, "h2",maxNodes)
                demo(before,action)
        if operation[1]=="beam":
            ff.customPrint("solve beam command called",2)
            pass

    elif operation[0] == "maxNodes":
        try:
            maxNodes = int(operation[1])
        except:
            ff.customPrint("Given MaxNodes is not a value!",5)