from helperfnc.puzzle import eight_puzzle
from helperfnc.frank_generic import frank_function as ff

class runner:
    def __init__(self):
        pass

    def ingest(self,fileLocation):
        pass





puzzle = eight_puzzle()        
puzzle.printState()
puzzle.setState("724 5b6 831")
ff.customPrint("Heuristic test: "+str(puzzle.calculateHeuristic2()))
puzzle.listAvailable()