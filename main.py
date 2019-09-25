from helperfnc.puzzle import eight_puzzle
from helperfnc.frank_generic import frank_function as ff

puzzle = eight_puzzle()        
puzzle.printState()
puzzle.setState("724 5b6 831")
ff.customPrint("Heuristic test: "+str(puzzle.calculateHeuristic2()))

