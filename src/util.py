import graph

def load_graph(filename):
    g = graph.Graph()

    with open(filename) as f:
        line = f.readline().split()
        assert line[0] == "t"

        while True:
            line = f.readline()
            if not line:
                break

            line = line.split()

            if line[0] == "v":
                # v <vid> <label>
                vid = int(line[1])
                label = int(line[2])
                g.set_vertex(vid, label)
            elif line[0] == "e":
                # e <vid1> <vid2>
                vid1 = int(line[1])
                vid2 = int(line[2])
                label = int(line[3])
                assert label == 0
                g.set_edge(vid1, vid2)
                g.set_edge(vid2, vid1)
            else:
                assert False

    return g
