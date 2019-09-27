from helperfnc.puzzle import eight_puzzle
from helperfnc.frank_generic import frank_function as ff
import sys
from decimal import Decimal
import csv

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
            return ("Unsolved",0)
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
                        print("move " + str(item))
                ff.customPrint("Solution path:"+str(solutionStep), 2)
                ff.customPrint("Solution length:"+str(puzzleNow.depth), 2)
                return "Solved",puzzleNow.depth
            else:
                ff.customPrint("Given a Solved board!", 4)
                return "Solved",0
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


def beam(boardClass, k,maxNodes):
    moves = 0
    childrenSorted = []
    allChildren = []
    empty = False
    best = [boardClass]
    while not empty:
        for child in best:
            #! Node Cap
            if(moves > maxNodes):
                ff.customPrint("Exceed allowed maxNodes!", 4)
                return ("Unsolved",0)
            #! Goal!
            if child.getState() == "b12345678":
                ff.customPrint(
                    "====================Solution====================", 6)
                solution = child.reverseTraversal([])
                solution.reverse()
                move_path = []
                for index, item in enumerate(solution):
                    if not index % 2 == 0:
                        move_path.append(item)

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
                return "Solved",(child.depth + 1)
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
        empty = False

# ========================================================================================
def maxNodesTest():
    with open('maxNodeTest.csv', mode='w') as maxNodeTest_file:
        current = eight_puzzle()
        for i in range(0, 100):
            for j in range(0,10):
                current.randomize(20)
                resulth1,steps1 = astar(current,"h1",i*100)
                resulth2,steps2 = astar(current,"h2",i*100)
                resultB,steps3 = beam(current,80,i*100)
                maxNodeTest_writer = csv.writer(maxNodeTest_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                maxNodeTest_writer.writerow(['A-Star h1',(i*100), resulth1, steps1])
                maxNodeTest_writer.writerow(['A-Star h2',(i*100), resulth2, steps2])                
                maxNodeTest_writer.writerow(['Beam 80',(i*100), resultB, steps3])        

def heruisticsOptionCompare():
    with open('heruisticsCompare.csv', mode='w') as heruisticsCompare_file:
        heruisticsCompare_writer = csv.writer(heruisticsCompare_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        current = eight_puzzle()
        for i in range(0, 100):
            current.randomize(20)
            resulth1,steps1 = astar(current,"h1",10000)
            resulth2,steps2 = astar(current,"h2",10000)
            heruisticsCompare_writer.writerow(['A-Star h1',resulth1, steps1])
            heruisticsCompare_writer.writerow(['A-Star h2',resulth2, steps2])

def solutionLengthCompare():
    with open('LengthCompare.csv', mode='w') as LengthCompare_file:
        LengthCompare_writer = csv.writer(LengthCompare_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        current = eight_puzzle()
        for i in range(0, 100):
            current.randomize(20)
            resulth1,steps1 = astar(current,"h1",10000)
            resulth2,steps2 = astar(current,"h2",10000)
            result3,steps3 = beam(current,80,1000)
            result4,steps4 = beam(current,20,1000)
            LengthCompare_writer.writerow(['A-Star h1',resulth1, steps1])
            LengthCompare_writer.writerow(['A-Star h2',resulth2, steps2])
            LengthCompare_writer.writerow(['Beam 20',result4, steps4])
            LengthCompare_writer.writerow(['Beam 80',result3, steps3])

def randomizeStressTest():
    current = eight_puzzle()
    with open('randomizeTest.csv', mode='w') as randomizeTest_File:
        RandomizeTest_writer = csv.writer(randomizeTest_File, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(0,10000):
            current.randomize(100)
            RandomizeTest_writer.writerow([current.getState()])

#=========================================================================================
#! Class initialization
#maxNodesTest()
#heruisticsOptionCompare()
#solutionLengthCompare()
randomizeStressTest()