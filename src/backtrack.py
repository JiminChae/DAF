import graph
from copy import deepcopy

def backtrack(query_dag, cs, emb = None, ext = None, visited = None):
    if emb is None:
        (failing, answer) = backtrack(query_dag, cs, emb = {}, ext = {query_dag.get_root()}, visited = set())
        return answer

    # print("emb : " + str(emb) + ", ext : " +str(ext) + ", visited : " + str(visited))
    # Exit Condition, Assume embedding is valid
    if len(emb) >= query_dag.size():
        # print("Embedding Made")
        return (set(), [emb])
    if len(ext) <= 0:
        return (set(), set())

    # Find u in query to match by candidate-size order
    u = None
    u_c = None
    for vertex in ext:
        ext_c = cs.extendable_candidate(emb, vertex)
        # print("vertex : " + str(vertex) + ", ext_c : " + str(ext_c))

        # Failing Set : Emptyset-class
        if ext_c is None or len(ext_c) == 0:
            # print("Emptyset Class")
            return (query_dag.get_ancestor(vertex), set())

        if u_c is None or len(u_c) > len(ext_c):
            u = vertex
            u_c = ext_c

    child_visited = deepcopy(visited)
    child_visited.add(u)
    failing = set()
    answer = []

    emb_exist = False
    for v in u_c: # for v in C(u)
        # Failing Set : Conflict-class
        if v in emb.values():
            u_conflict = list(emb.keys())[list(emb.values()).index(v)]
            failing = query_dag.get_ancestor(u).union(query_dag.get_ancestor(u_conflict))
            return (failing,set())

        child_emb = deepcopy(emb)
        child_emb[u] = v

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
            answer += child_answer
        elif len(child_failing) == 0 or len(child_answer) > 0:
            # Failing Set : Embedding-class
            emb_exist = True
            failing = set()
            answer += child_answer
        elif u not in child_failing:
            failing = child_failing
            answer = []
        else:
            failing.union(child_failing)

    return (failing, answer)
