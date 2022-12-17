import graph
from copy import deepcopy

#
# Directed Acyclic Graph
#
class DAG:
    def __init__(self, query, data):
        self.dag = graph.Graph()
        self.dag_inv = graph.Graph()

        vids = query.get_vertices()
        data_vids = data.get_vertices()

        for vid in vids:
            self.dag.set_vertex(vid, query.get_vertex_label(vid))
            self.dag_inv.set_vertex(vid, query.get_vertex_label(vid))

        C_ini_size = {}
        for u in vids:
            u_label = query.get_vertex_label(u)
            u_deg = len(query.get_vertex_neighbors(u))

            C_ini_size[u] = 0
            for v in data_vids:
                if data.get_vertex_label(v) == u_label and \
                        len(data.get_vertex_neighbors(v)) >= u_deg:
                    C_ini_size[u] += 1

        # find root
        self.root = sorted(vids, key=lambda u: C_ini_size[u] / len(query.get_vertex_neighbors(u)))[0]

        bfs_unvisited = {}
        for u in vids:
            bfs_unvisited[u] = True

        bfs_to_traverse = [self.root]
        while bfs_to_traverse:
            cur_vid = bfs_to_traverse.pop(0)
            bfs_unvisited[cur_vid] = False

            child_to_traverse = [child for child in query.get_vertex_neighbors(cur_vid) if bfs_unvisited[child]]
            child_to_traverse = sorted(child_to_traverse, key=lambda v:
            (data.get_label_stat()[v], -len(query.get_vertex_neighbors(v))))

            for child in child_to_traverse:
                self.dag.set_edge(cur_vid, child)
                self.dag_inv.set_edge(child, cur_vid)
                bfs_to_traverse.append(child)

    def size(self):
        return self.dag.size()

    def get_child(self, u):
        return self.dag.get_vertex_neighbors(u)

    def get_parent(self, u):
        return self.dag_inv.get_vertex_neighbors(u)

    def get_ancestor(self, u):
        queue = [u]
        ancestor = set()

        while queue:
            curAnc = queue.pop(0)
            ancestor.add(curAnc)

            anc_parents = deepcopy(self.get_parent(curAnc))

            while anc_parents:
                anc_parnet = anc_parents.pop()

                if anc_parnet not in ancestor:
                    queue.append(anc_parnet)

        return ancestor

    def get_root(self):
        return self.root






