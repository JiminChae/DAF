#!/usr/bin/env python3


import time
import sys
import util, dag, cs, backtrack, naive

def main():
    if len(sys.argv) != 3:
        sys.stderr.write(f"Usage: {sys.argv[0]} <data> <query>\n")
        exit(1)

    data = util.load_graph(sys.argv[1])
    query = util.load_graph(sys.argv[2])

    s_time = time.time()
    # 1. Build a rooted DAG
    query_dag = dag.DAG(query, data)

    # 2. Build the CS structure by using DAG-graph DP
    cand_space = cs.CS(query, query_dag, data)

    # 3. Backtrack using Adaptive Order & Failing Set
    matching = backtrack.backtrack(query_dag = query_dag, cs = cand_space)
    e_time = time.time()
    print("DAF gave " + str(len(matching)) + " answer in " + str(e_time-s_time) + "sec")

    s_time = time.time()
    naive_matching = naive.naive_algo(data=data, query=query)
    e_time = time.time()
    print("naive gave " + str(len(naive_matching)) + " answer in " + str(e_time-s_time) + "sec")

    print(util.diff(matching, naive_matching))

if __name__ == "__main__":
    main()
