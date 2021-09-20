"""
puzzle.py
Joel Peckham 
September 15, 2021
8-Puzzle Search Algorithm Home Work
For Richard Halterman's CPTR-418-Artificial Intelligence
"""

import queue as Q
from sys import displayhook

def getPuzzleChildren(puzzle):
    blankIndex = puzzle.index("-")
    blankCoordinates = (blankIndex // 3, blankIndex % 3)
    potentialChildren = []
    for direction in [(1,0), (-1,0), (0,1), (0,-1)]:
        # Check if move is valid
        newBlankCoordinates = (blankCoordinates[0] + direction[0], blankCoordinates[1] + direction[1])
        if newBlankCoordinates[0] < 0 or newBlankCoordinates[0] > 2 or newBlankCoordinates[1] < 0 or newBlankCoordinates[1] > 2:
            continue
        # Move the blank
        newBlankIndex = newBlankCoordinates[0] * 3 + newBlankCoordinates[1]
        newPuzzle = list(puzzle)
        newPuzzle[blankIndex] = newPuzzle[newBlankIndex]
        newPuzzle[newBlankIndex] = "-"
        potentialChildren.append("".join(newPuzzle))
    return potentialChildren

def manhattanDistance(puzzle):
    distance = 0
    for i, val in enumerate(list(puzzle)):
        if val == "-":
            continue
        targetIndex = int(val) - 1
        targetCoordinates = (targetIndex // 3, targetIndex % 3)
        distance += abs(targetCoordinates[0] - (i // 3)) + abs(targetCoordinates[1] - (i % 3))
    return distance


def misplacedTiles(puzzle):
    target = "12345678-"
    return sum([1 for i, val in enumerate(list(puzzle)) if val != target[i]])

def breadth_first_search(startPuzzle, solutionPuzzle = "12345678-"):
    queue = Q.Queue()
    queue.put([startPuzzle])
    visitedPuzzles = set([startPuzzle])
    while not queue.empty():
        path = queue.get()
        currentPuzzle = path[-1]
        if currentPuzzle == solutionPuzzle:
            return path
        for child in getPuzzleChildren(currentPuzzle):
            if child not in visitedPuzzles:
                visitedPuzzles.add(child)
                queue.put(path + [child])
    return None

def best_first_search(heuristicFunction, startPuzzle, solutionPuzzle = "12345678-"):
    queue = Q.PriorityQueue()
    queue.put((heuristicFunction(startPuzzle), [startPuzzle]))
    visitedPuzzles = set([startPuzzle])
    while not queue.empty():
        _, path = queue.get()
        currentPuzzle = path[-1]
        if currentPuzzle == solutionPuzzle:
            return path
        for child in getPuzzleChildren(currentPuzzle):
            if child not in visitedPuzzles:
                visitedPuzzles.add(child)
                queue.put((heuristicFunction(child), path + [child]))
    return None

def a_star_search(heuristicFunction, startPuzzle, solutionPuzzle = "12345678-"):
    queue = Q.PriorityQueue()
    start_g = 0
    start_f = heuristicFunction(startPuzzle) + start_g
    visitedPuzzles = set(startPuzzle)
    queue.put((start_f, (start_g, [startPuzzle])))
    while not queue.empty():
        node = queue.get()
        _, current_node = node
        current_g, current_puzzle_path = current_node
        current_puzzle = current_puzzle_path[-1]
        if current_puzzle == solutionPuzzle:
            return current_puzzle_path
        for child in getPuzzleChildren(current_puzzle):
            if child not in visitedPuzzles:
                visitedPuzzles.add(child)
                child_g = current_g + 1
                child_f = heuristicFunction(child) + child_g
                queue.put((child_f, (child_g, current_puzzle_path + [child])))
    return None

if __name__ == "__main__":
    print("Run analyzeSearches.py for test cases.")