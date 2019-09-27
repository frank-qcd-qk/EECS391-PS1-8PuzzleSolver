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
    moves = 0
    openList = [boardClass]
    closeList = []

    while(len(openList) > 0):
        puzzleNow = openList.pop(0)
        moves += 1
        #! Node Cap
        if(moves > maxNodes):
            ff.customPrint("Exceed allowed maxNodes!", 4)
            return ("Unsolved", 0)
        #! Completion Check
        if puzzleNow.getState() == "b12345678":
            ff.customPrint(
                "====================Solution====================", 6)
            if len(closeList) > 0:
                solution = puzzleNow.reverseTraversal([])
                solution.reverse()
                solutionStep = []
                # ? Get solution step
                for index, item in enumerate(solution):
                    if not index % 2 == 0:
                        solutionStep.append(item)
                # ? Get solution
                for index, item in enumerate(solution):
                    if index == 0:
                        ff.customPrint("Starting state", 6)
                        item.printState()
                    elif index % 2 == 0:
                        item.printState()
                    else:
                        ff.customPrint("move " + str(item), 6)
                ff.customPrint("Solution path:"+str(solutionStep), 2)
                ff.customPrint("Solution length:"+str(puzzleNow.depth), 2)
                return "Solved", puzzleNow.depth
            else:
                ff.customPrint("Given a Solved board!", 4)
                return "Solved", 0
        #! Search by getting babies!
        Options = puzzleNow.listAvailable()
        for option in Options:
            if option != '':
                state = eight_puzzle(option)
                if heruisticsOption == "h1":
                    state.herusticValue = state.calculateHeuristic1()
                else:
                    state.herusticValue = state.calculateHeuristic2()
                state.depth = puzzleNow.depth + 1
                state.functionValue = state.herusticValue + state.depth
                state.parent = puzzleNow
                # ? Check existance
                openID = ff.find_index(openList, state)
                closeID = ff.find_index(closeList, state)
                if openID == -1 and closeID == -1:
                    # * Not searched
                    openList.append(state)
                elif openID > -1:
                    already_seen = openList[openID]
                    if state.functionValue < already_seen.functionValue:
                        already_seen.functionValue = state.functionValue
                        already_seen.herusticValue = state.herusticValue
                        already_seen.parent = state.parent
                        already_seen.depth = state.depth
                elif closeID > -1:
                    already_seen = closeList[closeID]
                    if state.functionValue < already_seen.functionValue:
                        state.herusticValue = already_seen.herusticValue
                        state.functionValue = already_seen.functionValue
                        state.depth = already_seen.depth
                        state.parent = already_seen.parent
                        closeList.remove(already_seen)
                        openList.append(state)
        closeList.append(puzzleNow)
        openList = sorted(openList, key=lambda p: p.functionValue)


def beam(boardClass, k, maxNodes):
    moves = 0
    childrenSorted = []
    allChildren = []
    best = [boardClass]
    while True:
        for child in best:
            #! Node Cap
            if(moves > maxNodes):
                ff.customPrint("Exceed allowed maxNodes!", 4)
                return ("Unsolved", 0)
            #! Goal!
            if child.getState() == "b12345678":
                ff.customPrint(
                    "====================Solution====================", 6)
                solution = child.reverseTraversal([])
                solution.reverse()
                move_path = []
                # ? Get solution step
                for index, item in enumerate(solution):
                    if not index % 2 == 0:
                        move_path.append(item)
                # ? Get solution
                for index, item in enumerate(solution):
                    if index == 0:
                        ff.customPrint("Starting state", 6)
                        item.printState()
                    elif index % 2 == 0:
                        item.printState()
                    else:
                        ff.customPrint("move " + str(item), 6)
                ff.customPrint("Solution length:"+str(child.depth + 1), 2)
                ff.customPrint("Solution path:"+str(move_path), 2)
                return "Solved", (child.depth + 1)
            else:
                currentPuzzle = child
                options = currentPuzzle.listAvailable()
                for option in options:
                    if option != '':
                        moves += 1
                        state = eight_puzzle(option)
                        state.herusticValue = state.calculateHeuristic2()
                        state.parent = currentPuzzle
                        state.depth = currentPuzzle.depth + 1
                        if ff.find_index(allChildren, state) == -1:
                            allChildren.append(state)
                            childrenSorted.append(state)

        #! Select the best
        childrenSorted = sorted(childrenSorted, key=lambda p: p.herusticValue)
        best = []
        if len(childrenSorted) >= k:
            for i in range(0, k):
                best.append(childrenSorted.pop(0))
        elif len(childrenSorted) < k:
            for i in range(0, len(childrenSorted)):
                best.append(childrenSorted.pop(0))
        childrenSorted = []


# ========================================================================================
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
            ff.customPrint("Moving "+str(operation[1])+"!", 2)
            checkInit(initialized)
            current.move(operation[1], current.findBlank(), True)
    elif operation[0] == "randomizeState":
        ff.customPrint("randomizeState command called", 2)
        try:
            count = int(operation[1])
            ff.customPrint("Request: "+str(count)+" steps", 2)
        except:
            ff.customPrint("Randomize state did not specify step count!", 5)
            exit(99)
        else:
            checkInit(initialized)
            current.randomize(count)
    elif operation[0] == "solve":
        beforeBoard = current
        before = current.getState()
        if operation[1] == "A-star":
            ff.customPrint("solve A-star command called", 2)
            if operation[2] == "h1":
                ff.customPrint("using h1 heuristic", 2)
                astar(current, "h1", maxNodes)
            if operation[2] == "h2":
                ff.customPrint("using h2 heuristic", 2)
                astar(current, "h2", maxNodes)
        if operation[1] == "beam":
            ff.customPrint("solve beam command called", 2)
            beam(current, int(operation[2]), maxNodes)

    elif operation[0] == "maxNodes":
        try:
            maxNodes = int(operation[1])
        except:
            ff.customPrint("Given MaxNodes is not a value!", 5)
