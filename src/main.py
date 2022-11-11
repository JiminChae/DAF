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

    # TODO



if __name__ == "__main__":
    main()
