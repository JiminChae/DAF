import graph


def backtrack(query_dag, cs, emb = None, ext = None, visited = None):
    if emb is None:
        (failing, answer) = backtrack(query_dag, cs, emb = {}, ext = {cs.query_dag.get_root()}, visited = set())
        return answer


    # Exit Condition, Assume embedding is valid
    if len(emb) >= query_dag.size():
        return (set(), {emb})

    u = None
    u_c = None
    for vertex in ext:
        ext_c = cs.ext_candidate(emb, vertex)

        if u_c is None or len(u_c) > len(ext_c):
            u = vertex
            u_c = ext_c

    child_visited = visited + {u}
    failing_set = set()

    for v in u_c: # for v in C(u)
        # check conflict

        # TODO : update embedding, ext, visited
        child_emb = emb + {(u, v)}

        child_ext = copy.deepcopy(ext)
        child_ext.remove(u)
        for ext_cand in query_dag.get_child(u):
            parent_all_matched = True
            for par in query_dag.get_parent(ext_cand):
                if par not in child_visited:
                    parent_all_matched = False
                    break
            if parent_all_matched:
                child_ext.add(ext_cand)

        (failing, answer) = backtrack(query_dag, cs, child_emb, child_ext, child_visited)

        if u not in failing:
            # Stop visiting
            break
        else:
            failing_set += failing

    return (failing, answer)
