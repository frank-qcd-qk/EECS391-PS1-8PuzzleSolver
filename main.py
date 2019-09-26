from helperfnc.puzzle import eight_puzzle
from helperfnc.frank_generic import frank_function as ff
import sys


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

def astar(states, heruistics, result):
    pass


#! Start of the program:
commandfile = sys.argv[1]
commandList = ingest(commandfile)
#! Class initialization
current = eight_puzzle()
initialized = False
#! Command Operation
for command in commandList:
    operation = command.split()
    if operation[0] == "setState":
        ff.customPrint("setState Operation called", 1)
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
        ff.customPrint("printState operation called", 1)
        checkInit(initialized)
        current.printState()
    elif operation[0] == "move":
        if operation[1] == "up" or operation[2] == "down" or operation[2] == "left" or operation[2] == "right":
            checkInit(initialized)
            current.move(operation[1],True)
    elif operation[0] == "randomizeState":
        ff.customPrint("reqeusted to automatically randomize",1)
        try:
            count = int(operation[1])
        except:
            ff.customPrint("Randomize state did not specify step count!",5)
            exit(99)
        else:
            checkInit(initialized)
            current.randomizeState(count)
    elif operation[0] == "solve":




puzzle.printState()
#puzzle.setState("b12 345 678")
puzzle.setState("724 5b6 831")
ff.customPrint("Heuristic test: "+str(puzzle.calculateHeuristic2()))
puzzle.listAvailable()
