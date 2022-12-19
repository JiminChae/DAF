import dag

#
# Candidate Space
#
class CS:
    def __init__(self, query, query_dag, data):
        self.query_dag = query_dag

        # { u : C(u) }
        # u : query vertex idx
        # C(u) : set
        self.cand_sets = {}

        # { e : {v : {v_c}} }
        # e = (u, u_c)
        # v : vertex in C(u)
        # v_c : vertex in C(u_c)
        self.edges = {}

        query_vertices = query.get_vertices()
        data_vertices = data.get_vertices()

        # Construct the candidate set for each query vertex
        for u in query_vertices:
            cand_set = set()
            for v in data_vertices:
                query_label = query.get_vertex_label(u)
                data_label = data.get_vertex_label(v)
                query_degree = len(query.get_vertex_neighbors(u))
                data_degree = len(data.get_vertex_neighbors(v))
                if query_label == data_label and query_degree <= data_degree:
                    cand_set.add(v)
            self.cand_sets[u] = cand_set

        # Add edges between the candidates
        for u in query_vertices:
            for u_c in query_vertices:
                for v in self.cand_sets[u]:
                    for v_c in self.cand_sets[u_c]:
                        if data.has_edge(v, v_c):
                            assert data.has_edge(v_c, v)

                            # v -> v_c
                            if (u, u_c) not in self.edges:
                                self.edges[u, u_c] = {}
                            if v not in self.edges[u, u_c]:
                                self.edges[u, u_c][v] = set()
                            self.edges[u, u_c][v].add(v_c)

                            # v_c -> v
                            if (u_c, u) not in self.edges:
                                self.edges[u_c, u] = {}
                            if v_c not in self.edges[u_c, u]:
                                self.edges[u_c, u][v_c] = set()
                            self.edges[u_c, u][v_c].add(v)

        # TODO: Optimize CS

    # Get the candidate set for node u
    def get_cand_set(self, u):
        return self.cand_sets[u]

    # Does v belong to C(u)
    def has_vertex(self, u, v):
        return v in self.cand_sets[u]

    # Get {v : {v_c}} for edge (u, u_c)
    # It returns None if there is no edge between C(u) and C(u_c)
    def get_edge(self, e):
        assert type(e) == tuple

        query_vertices = self.cand_sets()
        assert e[0] in query_vertices and e[1] in query_vertices

        try:
            return self.edges[e]
        except KeyError:
            return None

    # Get C_M(u) where M is a partial embedding
    def extendable_candidate(self, emb, u):
        try:
            if len(self.query_dag.get_parent(u)) == 0:
                ext_cand = self.get_cand_set(u)
            else:
                ext_cand = set()
                for p in self.query_dag.get_parent(u):
                    q = emb[p]
                    s = self.edges[p, u][q]
                    ext_cand.intersection_update(s)
            return ext_cand
        except KeyError:
            return None

    # For debugging
    def print(self):
        print("<Candidate Sets>")
        for u, s in self.cand_sets.items():
            print(f"{u}: {s}")
        print()
