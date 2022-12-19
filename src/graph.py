#
# Directed labeled graph
#
class Graph:
    def __init__(self):
        self.label_stat = {}
        self.vertices = {}

    def size(self):
        return len(self.get_vertices())

    def get_label_stat(self):
        return self.label_stat

    def get_vertices(self):
        return self.vertices.keys()

    def get_vertex_label(self, vid):
        return self.vertices[vid][0]

    def get_vertex_neighbors(self, vid):
        return self.vertices[vid][1]

    def set_vertex(self, vid, label):
        try:
            self.label_stat[label] += 1
        except KeyError:
            self.label_stat[label] = 1
        self.vertices[vid] = (label, set())

    def has_edge(self, src, dst):
        assert src in self.vertices and dst in self.vertices
        return dst in self.vertices[src][1]

    def set_edge(self, src, dst):
        assert src in self.vertices and dst in self.vertices
        self.vertices[src][1].add(dst)

    # For debugging
    def print(self):
        for vid in self.get_vertices():
            print(f"{vid} -> {self.get_vertex_neighbors(vid)}")
        print()
