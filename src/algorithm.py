import graph

def build_dag(query, data):
    query_dag = graph.Graph()

    query_vids = query.get_label_stat()
    data_vids = data.get_label_stat()

    for vid in query_vids:
        query_dag.set_vertex(vid, query.get_vertex_label(vid))

    C_ini_size = {}
    for u in query_vids:
        u_label = query.get_vertex_label(u)
        u_deg = len(query.get_vertex_neighbors(u))

        C_ini_size[u] = 0
        for v in data_vids:
            if data.get_vertex_label(v) == u_label and \
                len(data.get_vertex_neighbors(v)) >= u_deg:
                C_ini_size[u] += 1

    # find root
    root = sorted(query_vids, key = lambda u: C_ini_size[u]/len(query.get_vertex_neighbors(u)))[0]

    bfs_unvisited = {}
    for u in query_vids:
        bfs_unvisited[u] = True
    bfs_unvisited[root] = False

    bfs_to_traverse = [root]
    while bfs_to_traverse:
        cur_vid = bfs_to_traverse.pop(0)
        bfs_unvisited[cur_vid] = False

        child_to_traverse = [child for child in query.get_vertex_neighbors(cur_vid) if bfs_unvisited[child]]
        child_to_traverse = sorted(child_to_traverse, key = lambda v:
            (data.get_label_stat()[v], -len(query.get_vertex_neighbors(v))))

        for child in child_to_traverse:
            query_dag.set_edge(cur_vid, child)
            bfs_to_traverse.append(child)

    return query_dag



def build_cs(query, query_dag, data):
    # TODO
    pass



def backtrack(query, query_dag, cs, emb):
    # TODO
    pass
