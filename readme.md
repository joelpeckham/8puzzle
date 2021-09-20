# 8-Puzzle | Joel Peckham | For CPTR-418-A

## Analysis Output
This is the output from the largest test I ran. The test used 500 randomly generated puzzles. Each algorithm was tested 3 times per puzzle and their times were averaged.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        Solver analysis from 500 puzzles with 3 identical trials per algorithm sorted by speedup.        │
├──────────────────────┬────────────────────┬─────────────┬───────────┬───────────┬─────────────┬─────────┤
│ Solver               │ Heuristic          │ Avg. Length │ Avg. Time │ Std. Dev. │ % Std. Dev. │ Speedup │
├──────────────────────┼────────────────────┼─────────────┼───────────┼───────────┼─────────────┼─────────┤
│ Best First Search    │ Manhattan Distance │ 63.748      │ 0.00605   │ 0.00336   │ 55.6        │ 149.9   │
│ Best First Search    │ Misplaced Tiles    │ 129.024     │ 0.01179   │ 0.00916   │ 77.7        │ 76.9    │
│ A* Search            │ Manhattan Distance │ 23.16       │ 0.03935   │ 0.05039   │ 128.1       │ 23.0    │
│ A* Search            │ Misplaced Tiles    │ 23.16       │ 0.28869   │ 0.34775   │ 120.5       │ 3.1     │
│ Breadth First Search │ None               │ 23.16       │ 0.9063    │ 1.16472   │ 128.5       │ 1.0     │
└──────────────────────┴────────────────────┴─────────────┴───────────┴───────────┴─────────────┴─────────┘
┌─────────────────────────────────────────────────┬───────────────────────────────────────────┐
│ Category                                        │ Category Winner                           │
├─────────────────────────────────────────────────┼───────────────────────────────────────────┤
│ Fastest Solver (Averaging over heursitcs used)  │ Best First Search                         │
│ Fastest Heuristic (Averaging over solvers used) │ Manhattan Distance                        │
│ Most Consistent (Min. % Std. Dev.)              │ Best First Search with Manhattan Distance │
│ Fastest Overall Search                          │ Best First Search with Manhattan Distance │
│ Fastest Optimal Search                          │ A* Search with Manhattan Distance         │
└─────────────────────────────────────────────────┴───────────────────────────────────────────┘
```

To run the test yourself use:

`python analyzeSearches.py -n 500 -t 3`

To view my results run:

`python analyzeSearches.py -f 'testDataFiles/largeTest.json'`
## AnalyzeSearches usage

```
usage: analyzeSearches.py [-h] [-t TRIALS] [-n NUMBER] [-s SOLVER] [-o OUTPUT] [-f FILE]

Analyze the performance of the search algorithms.

optional arguments:
  -h, --help            show this help message and exit
  -t TRIALS, --trials TRIALS
                        Number of trials per puzzle (1-25). Default: 3.
  -n NUMBER, --number NUMBER
                        Number of puzzles to test (1-500). Default: 25.
  -s SOLVER, --solver SOLVER
                        Search algorithm to use. Options are 'all', 'bfs', 'best_fs_md', 'best_fs_mt', 'a*_md', 'a*_mt'. Default: 'all'.
  -o OUTPUT, --output OUTPUT
                        Output file name. Default: 'output.json'.
  -f FILE, --file FILE  File containing previous raw analysis data. Example: 'output.json'.
  ```