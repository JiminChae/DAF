#!/usr/bin/env python3

import sys

import algorithm, graph

def load_graph(filename):
    g = graph.Graph()

    with open(filename) as f:
        # t <num_vertices> <num_edges>
        line = f.readline().split()
        assert line[0] == "t"
        num_vertices = int(line[1])
        num_edges = int(line[2])

        # v <vid> <label>
        for i in range(num_vertices):
            line = f.readline().split()
            assert line[0] == "v"
            vid = int(line[1])
            label = int(line[2])
            g.set_vertex(vid, label)

        # e <vid1> <vid2>
        for i in range(num_edges):
            line = f.readline().split()
            assert line[0] == "e"
            vid1 = int(line[1])
            vid2 = int(line[2])
            g.set_edge(vid1, vid2)
            g.set_edge(vid2, vid1)

    return g



def main():
    if len(sys.argv) != 3:
        sys.stderr.write(f"Usage: {sys.argv[0]} <data> <query>\n")
        exit(1)

    data = load_graph(sys.argv[1])
    query = load_graph(sys.argv[2])

    query_dag = algorithm.build_dag(query, data)

    # TODO



if __name__ == "__main__":
    main()
