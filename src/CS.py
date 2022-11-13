#
# Candidate Set
#

class CS:
    def __init__(self):
        self.vertex = {}
        # { u : C(u) }
        # u : query vertex idx

        self.edge = {}
        # { e : {v : [v_c]} }
        # e = (u, u_c)
        # v : vertex in C(u)
        # v_c : vertex in C(u_c)

        self.query = None
