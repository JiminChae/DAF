import dag

#
# Candidate Space
#
class CS:
    def __init__(self, query, query_dag, data):
        self.vertex = {}
        # { u : C(u) }
        # u : query vertex idx
        # C(u) : set

        self.edge = {}
        # { e : {v : {v_c}} }
        # e = (u, u_c)
        # v : vertex in C(u)
        # v_c : vertex in C(u_c)

        self.query = None

        # TODO
        pass

    def get_vertex(self, u):
        # TODO : get a set C(u)
        pass

    def has_vertex(self, u, v):
        # TODO : does v in C(u)
        pass

    def get_edge(self, e):
        # TODO : get {v:{v_c}}
        pass

    def get_edge(self, u, u_c):
        # TODO : get edge of (u,u_c)
        # return empty set if no edge btw (u,u_c)
        pass

    def extendable_candidate(self, M, u):
        # get C_M(u)
        pass





