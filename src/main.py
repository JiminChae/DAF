#!/usr/bin/env python3

import sys

import algorithm, util

def main():
    if len(sys.argv) != 3:
        sys.stderr.write(f"Usage: {sys.argv[0]} <data> <query>\n")
        exit(1)

    data = util.load_graph(sys.argv[1])
    query = util.load_graph(sys.argv[2])

    query_dag = algorithm.build_dag(query, data)

    query_dag_v = query_dag.get_vertices()
    for v in query_dag_v:
        print(v, end= " : ")
        print(query_dag.get_vertex_neighbors(v))

    # TODO



if __name__ == "__main__":
    main()
