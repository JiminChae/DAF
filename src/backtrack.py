import graph
from copy import deepcopy

def backtrack(query_dag, cs, emb = None, ext = None, visited = None):
    if emb is None:
        (failing, answer) = backtrack(query_dag, cs, emb = {}, ext = {cs.query_dag.get_root()}, visited = set())
        return answer

    # Exit Condition, Assume embedding is valid
    if len(emb) >= query_dag.size():
        return (set(), {emb})
    if len(ext) <= 0:
        return (set(), set())

    # Find u in query to match by candidate-size order
    u = None
    u_c = None
    for vertex in ext:
        ext_c = cs.ext_candidate(emb, vertex)

        # Failing Set : Emptyset-class
        if u_c is None:
            return (set(query_dag.get_ancestor(u)), set())

        if len(u_c) > len(ext_c):
            u = vertex
            u_c = ext_c

    child_visited = visited + {u}
    failing = set()
    answer = set()

    emb_exist = False
    for v in u_c: # for v in C(u)
        # Failing Set : Conflict-class
        if v in emb.values():
            u_conflict = list(emb.keys())[list(emb.values()).index(v)]
            failing = set(query_dag.get_ancestor(u) + query_dag.get_ancestor(u))
            return (failing,set())

        child_emb = emb + {(u, v)}

        child_ext = deepcopy(ext)
        child_ext.remove(u)

        # find candidate for extendable vertices
        for ext_cand in query_dag.get_child(u):
            parent_all_matched = True
            for par in query_dag.get_parent(ext_cand):
                if par not in child_visited:
                    parent_all_matched = False
                    break
            if parent_all_matched:
                child_ext.add(ext_cand)

        (child_failing, child_answer) = backtrack(query_dag, cs, child_emb, child_ext, child_visited)

        if emb_exist:
            answer.union(child_answer)
        elif len(child_failing) == 0 or len(child_answer) > 0:
            # Failing Set : Embedding-class
            emb_exist = True
            failing = set()
            answer.union(child_answer)
        elif u not in child_failing:
            failing = child_failing
            answer = set()
        else:
            failing.union(child_failing)

    return (failing, answer)
