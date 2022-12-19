# DAF

## How to run
```
$ src/main.py <data> <query>
```

## Implementation
```
src/
  backtrack.py      : backtracking algorithm
  cs.py             : candidate space class
  dag.py            : directed acyclic graph class
  graph.py          : graph class
  main.py           : main routine
  naive.py          : naive subgraph matching algorithm for testing (very slow)
  util.py           : miscellaneous things
  
sample/             : sample data & query graphs
  01/               : graph in the paper
  02/               : graph introduced in presentation
  yeast/            : yeast dataset
```

## Reference
- Han, Myoungji, et al. "Efficient subgraph matching: Harmonizing dynamic programming, adaptive matching order, and failing set together." *Proceedings of the 2019 International Conference on Management of Data.* 2019.
