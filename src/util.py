import graph

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
