import dag
import util

#
# Candidate Space
#
class CS:
    def __init__(self, query, query_dag, data):
        self.query_dag = query_dag
        self.data = data

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


        self.optimize()

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

    # Refine CS structure
    #
    # @return   True if the CS structure has been reduced
    #           False o.w.
    def refine(self, graph, order):
        dirty = False

        for u in reversed(order):
            deleted = set()

            for v in self.cand_sets[u]:
                survived = True

                for u_c in graph.get_vertex_neighbors(u):
                    passed = False

                    for v_c in self.cand_sets[u_c]:
                        if self.data.has_edge(v, v_c):
                            passed = True
                            break

                    if not passed:
                        survived = False
                        break
                
                if not survived:
                    deleted.add(v)

            old_len = len(self.cand_sets[u])
            self.cand_sets[u].difference_update(deleted)
            new_len = len(self.cand_sets[u])
            if new_len < old_len:
                dirty = True

        return dirty

    # Optimize CS structure
    def optimize(self):
        dag_graph = self.query_dag.get_dag()
        dag_inv_graph = self.query_dag.get_dag_inv()

        # Do topological sort
        order = util.topological_sort(dag_graph)
        order_inv = list(reversed(order))

        # State Machine
        # 0: Running
        # 1: One more chance
        # 2: Stopped
        state = 0
        while True:
            if self.refine(dag_inv_graph, order_inv):
                state = 0
            else:
                state += 1
                if state == 2:
                    break

            if self.refine(dag_graph, order):
                state = 0
            else:
                state += 1
                if state == 2:
                    break

    # Get C_M(u) where M is a partial embedding
    def extendable_candidate(self, emb, u):
        try:
            if len(self.query_dag.get_parent(u)) == 0:
                ext_cand = self.get_cand_set(u)
            else:
                for p in self.query_dag.get_parent(u):
                    q = emb[p]
                    s = self.edges[p, u][q]
                    try:
                        ext_cand.intersection_update(s)
                    except UnboundLocalError:
                        ext_cand = set(s)
            return ext_cand
        except KeyError:
            return None

    # For debugging
    def print(self):
        print("<Candidate Sets>")
        for u, s in self.cand_sets.items():
            print(f"{u}: {s}")
        print()

        print("<Candidate Edges>")
        for e, d in self.edges.items():
            print(f"  Query Edge {e} corresponds to:")
            for v, s in d.items():
                print(f"    Data Edge {v} -> {s}")
