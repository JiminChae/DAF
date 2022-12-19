import graph
from itertools import permutations
from itertools import product

def check_embedding(data, query, emb):
    for u in emb.keys():
        v = emb[u]

        # different label
        if query.get_vertex_label(u) != data.get_vertex_label(v):
            # print("False : Label not match")
            return False

        # more degree in query
        if len(query.get_vertex_neighbors(u)) > len(data.get_vertex_neighbors(v)):
            # print("False : more edge in query")
            return False

    for u in emb.keys():
        v = emb[u]

        u_neighbor = query.get_vertex_neighbors(u)
        v_neighbor = data.get_vertex_neighbors(v)
        for u_n in u_neighbor:
            if emb[u_n] not in v_neighbor:
                # print("False : not edge in data")
                return False
    return True

def naive_algo(data, query):
    label = list(query.get_label_stat().keys())

    query_label_dict = {}
    for q_label in label:
        query_label_dict[q_label] = []
    for q_vertex in query.get_vertices():
        query_label_dict[query.get_vertex_label(q_vertex)].append(q_vertex)
    query_label_size = [len(query_label_dict[i]) for i in label]
    query_vertex = []
    for l in label:
        query_vertex += query_label_dict[l]

    data_label_dict = {}
    for d_label in label:
        data_label_dict[d_label] = []
    for d_vertex in data.get_vertices():
        data_label_dict[data.get_vertex_label(d_vertex)].append(d_vertex)
    data_label_list = [data_label_dict[l] for l in label]

    if False:
        print(label)
        print(query_label_dict)
        print(query_label_size)
        print(query_vertex)
        print(data_label_dict)
        print(data_label_list)

    matches = [list(permutations(data_label_list[i], query_label_size[i])) for i in range(len(label))]
    for i in range(len(matches)):
        matches[i] = [list(j) for j in matches[i]]
    matches = list(product(*matches))
    for i in range(len(matches)):
        tmp = []
        for j in matches[i]:
            tmp += j
        matches[i] = tmp

    answer = []
    for match in matches:
        emb = {}
        for i in range(len(query_vertex)):
            emb[query_vertex[i]] = match[i]

        if check_embedding(data = data, query = query, emb = emb):
            answer.append(emb)

    return answer




