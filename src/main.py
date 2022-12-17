#!/usr/bin/env python3

import sys

import util
import dag, cs, backtrack

def main():
    if len(sys.argv) != 3:
        sys.stderr.write(f"Usage: {sys.argv[0]} <data> <query>\n")
        exit(1)

    data = util.load_graph(sys.argv[1])
    query = util.load_graph(sys.argv[2])

    # 1. Build a rooted DAG
    query_dag = dag.DAG(query, data)

    # 2. Build the CS structure by using DAG-graph DP
    cand_space = cs.CS(query, query_dag, data)

    # TODO



if __name__ == "__main__":
    main()
