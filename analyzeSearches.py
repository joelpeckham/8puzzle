from puzzle import *
from helpers import *
import json
import argparse
import time
import sys

with open('puzzleData.json') as data_file:
    puzzle_data = json.load(data_file) #puzzle_data is a list of dictionaries {"puzzle":puzzle,"bfs_time": executeTime, "path": path, "path_length": len(path)}
testCases = [puzzle["puzzle"] for puzzle in puzzle_data]

#Parse command line arguments
parser = argparse.ArgumentParser(description='Analyze the performance of the search algorithms.')
parser.add_argument('-t','--trials', type=int, default=3, help='Number of trials per puzzle (1-25). Default: 3.')
parser.add_argument('-n','--number', type=int, default=25, help='Number of puzzles to test (1-500). Default: 25.')
parser.add_argument('-s','--solver', type=str, default="all", help="Search algorithm to use. Options are 'all', 'bfs', 'best_fs_md', 'best_fs_mt', 'a*_md', 'a*_mt'. Default: 'all'.")
parser.add_argument('-o','--output', type=str, default="output.json", help="Output file name. Default: 'output.json'.")
parser.add_argument('-f', '--file', type=str, default=None, help="File containing previous raw analysis data. Example: 'output.json'.")
args = parser.parse_args()

args = parser.parse_args()
trialsPerTest = max(1, min(args.trials, 25))
numberOfPuzzles = max(1, min(args.number, 500))
solversDict = {
    "bfs" : {"functionName": "Breadth First Search", "function": breadth_first_search, "heuristicName":None, "heuristicFunction":None},
    "best_fs_md" : {"functionName": "Best First Search", "function": best_first_search, "heuristicName": "Manhattan Distance", "heuristicFunction":manhattanDistance},
    "best_fs_mt" : {"functionName": "Best First Search", "function": best_first_search, "heuristicName": "Misplaced Tiles", "heuristicFunction":misplacedTiles},
    "a*_md" : {"functionName": "A* Search", "function": a_star_search, "heuristicName": "Manhattan Distance", "heuristicFunction":manhattanDistance},
    "a*_mt" :{"functionName": "A* Search", "function": a_star_search, "heuristicName": "Misplaced Tiles", "heuristicFunction":misplacedTiles}
}

resultsByPuzzle = []
if args.file is None:
    if args.solver != "all":
        solversDict = {k:v for k,v in solversDict.items() if args.solver.lower() == k or "bfs" == k}
    progress = 1
    outputLines = 4
    sys.stdout.write("\n"*(outputLines-1))
    sys.stdout.flush()


    for puzzleIndex, puzzle in enumerate(testCases[:numberOfPuzzles]):
        solverResults = []
        for solver_key, solver in solversDict.items():
            trialResults = []
            for trial in range(trialsPerTest):
                progressPercent = (progress/(numberOfPuzzles*trialsPerTest*len(solversDict)))*100
                sys.stdout.write("\033[A".join("\x1b[2K\r" for i in range(outputLines)))
                sys.stdout.write(f"{progressBarString(25,progressPercent)}({progressPercent:0.1f}%)({progress}/{numberOfPuzzles*trialsPerTest*len(solversDict)})\n")
                sys.stdout.write(f"Testing puzzle: '{puzzle}' Identical Trial: {trial+1:02d}\n")
                sys.stdout.write(f"Solver: {solver['functionName']}\n")
                sys.stdout.write(f"Heuristic: {solver['heuristicName']}")
                sys.stdout.flush()

                startTime = time.time()
                if solver["heuristicName"] is not None:
                    path = solver["function"](solver["heuristicFunction"], puzzle)
                else:
                    path = solver["function"](puzzle)
                endTime = time.time()


                trialResults.append({"trial": trial, "time": endTime-startTime, "path": path, "path_length": len(path)})
                progress += 1
            solverResults.append({"trials": trialResults, "shortName":solver_key, "solver": solver["functionName"], "heuristic":solver["heuristicName"], "average_time": sum([result["time"] for result in trialResults])/trialsPerTest})
        resultsByPuzzle.append({"puzzle": puzzle, "results": solverResults})

    sys.stdout.write("\033[A".join("\x1b[2K\r" for i in range(outputLines)))
    sys.stdout.flush()
    with open(args.output, 'w') as outfile:
        json.dump(resultsByPuzzle, outfile, indent=2)
    print(f"\nSaved raw analysis data to '{args.output}'.")
else:
    with open(args.file) as data_file:
        resultsByPuzzle = json.load(data_file)
    print(f"Loaded raw analysis data from '{args.file}'.")


#Get Results by solver
resultsBySolver = {}
for puzzle in resultsByPuzzle:
    for solver in puzzle["results"]:
        if solver["shortName"] not in resultsBySolver.keys():
            resultsBySolver[solver["shortName"]] = {"results":[]}
        numTrials = len(solver["trials"])
        pathLength = solver["trials"][0]["path_length"]
        averageTime = solver["average_time"]
        path = solver["trials"][0]["path"]
        resultsBySolver[solver["shortName"]]["solver"] = solver["solver"]
        resultsBySolver[solver["shortName"]]["heuristic"] = solver["heuristic"]
        resultsBySolver[solver["shortName"]]["results"].append({"puzzle": puzzle["puzzle"], "numTrials": numTrials, "pathLength": pathLength, "averageTime": averageTime, "path": path})

analysis={}
#Analyze Results by solver and store to analysis dict entry.
for key, solver in resultsBySolver.items():
    if key not in analysis.keys():
        analysis[key] = {"solver":solver["solver"], "heuristic":solver["heuristic"]}
    results = solver["results"]
    #Calculate average path length
    averagePathLength = sum([result["pathLength"] for result in results])/len(results)
    #Calculate average time
    averageTime = sum([result["averageTime"] for result in results])/len(results)
    #Calculate variance in time
    varianceTime = sum([(result["averageTime"]-averageTime)**2 for result in results])/len(results)
    #Calculate standard deviation in time
    standardDeviationTime = math.sqrt(varianceTime)
    #Percent standdev from average
    percentStandardDeviationTime = standardDeviationTime/averageTime*100
    #Add to resultsBySolver dict entrys
    analysis[key]["averagePathLength"] = averagePathLength
    analysis[key]["averageTime"] = averageTime
    analysis[key]["standardDeviationTime"] = standardDeviationTime
    analysis[key]["percentStandardDeviationTime"] = percentStandardDeviationTime

for k,v in analysis.items():
    #Calculate speedup compared to average time of BFS
    speedup = analysis["bfs"]["averageTime"]/v["averageTime"]
    analysis[k]["speedup"] = speedup

solversTable = Table()
solversTable.title = f"Solver analysis from {len(resultsByPuzzle)} puzzles with {list(resultsBySolver.values())[0]['results'][0]['numTrials']} identical trials per algorithm sorted by speedup."
solversTable.columnNames = ["Solver", "Heuristic", "Avg. Length", "Avg. Time", "Std. Dev.", "% Std. Dev.", "Speedup"]
for k,v in analysis.items():
    #Add rows to table for each solver. Round to 3 decimal places.
    solversTable.add_row([v["solver"], v["heuristic"], round(v["averagePathLength"], 3), round(v["averageTime"], 5), round(v["standardDeviationTime"], 5), round(v["percentStandardDeviationTime"], 1), round(v["speedup"], 1)])
solversTable.sort(6, reverse=True)
print(solversTable)

#Best in Category table
bicTable = Table()
bicTable.columnNames = ["Category", "Category Winner"]
#Get fastest solver
averageSolverTimes = {}
averageHeuristicTimes = {}
for solver in solversTable.rows:
    #Get average time for each solver
    if solver[0] not in averageSolverTimes.keys():
        averageSolverTimes[solver[0]] = solver[3]
    else:
        averageSolverTimes[solver[0]] = (averageSolverTimes[solver[0]] + solver[3])/2
    #Get average time for each heuristic
    if solver[1] not in averageHeuristicTimes.keys():
        averageHeuristicTimes[solver[1]] = solver[3]
    else:
        averageHeuristicTimes[solver[1]] = (averageHeuristicTimes[solver[1]] + solver[3])/2
    
fastestSolver = min(averageSolverTimes, key=lambda k: averageSolverTimes[k])
fastestHeuristic = min(averageHeuristicTimes, key=lambda k: averageHeuristicTimes[k])

solversTable.sort(5, reverse=False)
mostConsistentSolver = solversTable.rows[0][0]
mostConsistentHeuristic = solversTable.rows[0][1]
solversTable.sort(3, reverse=False)
fastestTotalSover = solversTable.rows[0][0]
fastestTotalHeuristic = solversTable.rows[0][1]

optimalPathLength = round(analysis["bfs"]["averagePathLength"],2)

fastestOptimalSolver = None
fastestOptimalHeuristic = None
for solver in solversTable.rows:
    if solver[2] == optimalPathLength:
        fastestOptimalSolver = solver[0]
        fastestOptimalHeuristic = solver[1]
        break

bicTable.add_row(["Fastest Solver (Averaging over heursitcs used)",fastestSolver])
bicTable.add_row(["Fastest Heuristic (Averaging over solvers used)",fastestHeuristic])
bicTable.add_row(["Most Consistent (Min. % Std. Dev.)", mostConsistentSolver + ((" with "+mostConsistentHeuristic) if mostConsistentHeuristic else "")])
bicTable.add_row(["Fastest Overall Search", fastestTotalSover + ((" with "+fastestTotalHeuristic) if fastestTotalHeuristic else "")])
bicTable.add_row(["Fastest Optimal Search", fastestOptimalSolver + ((" with "+fastestOptimalHeuristic) if fastestOptimalHeuristic else "")])

print(bicTable)