import networkx as nx
import matplotlib.pyplot as plt

G1 = nx.Graph()
G1.add_edges_from([
    (1, 2), (2, 3), (3, 4), (4, 1),
    (1, 9), (9, 10), (9, 8),
    (2, 12), (12, 5), (12, 10),
    (4, 5), (3, 8),
    (5, 6), (7, 8),
    (10, 11), (6, 7),
    (6, 11), (7, 11)
])

G2 = nx.Graph()
G2.add_edges_from([
    ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'),
    ('E', 'F'), ('F', 'G'), ('G', 'A'),
    ('G', 'H'), ('H', 'B'),
    ('F', 'L'), ('L', 'C'),
    ('H', 'I'), ('K', 'L'), ('I', 'K'),
    ('A', 'K'),
    ('I', 'J'), ('J', 'D'), ('E', 'J')
])

pos_G1 = {
    4: (0, 0), 3: (10, 0), 2: (10, 10), 1: (0, 10),
    10: (5, 5), 9: (2.5, 7.5), 12: (7.5, 7.5),
    5: (1.25, 5), 8: (8.75, 5),
    11: (5, 3.75), 6: (3.75, 2.75), 7: (6.25, 2.75)
}

pos_G2 = {
    'A': (5, 10), 'B': (10, 6.67), 'C': (10, 3.33),
    'D': (6.67, 0), 'E': (3.33, 0), 'F': (0, 3.33),
    'G': (0, 6.67),
    'H': (5, 7.5), 'I': (5, 5), 'J': (5, 2.5),
    'K': (3, 6.25), 'L': (3, 4.75)
}

def min_cycle_info(G):
    DG = nx.DiGraph(G)
    cycles = list(nx.simple_cycles(DG))
    unique = set(tuple(sorted(c)) for c in cycles)
    if not unique:
        return None, 0
    m = min(len(c) for c in unique)
    return m, sum(1 for c in unique if len(c) == m)

def invariants(G):
    m, c = min_cycle_info(G)
    return (
        G.number_of_nodes(),
        G.number_of_edges(),
        tuple(sorted([d for _, d in G.degree()], reverse=True)),
        m,
        c
    )


def build_adj(G):
    return {node: set(G[node]) for node in G.nodes()}


def node_signature(adj, node, degree):
    return (degree[node], tuple(sorted(degree[neigh] for neigh in adj[node])))


def is_isomorphic_custom(G1, G2):
    if G1.number_of_nodes() != G2.number_of_nodes() or G1.number_of_edges() != G2.number_of_edges():
        return False, None

    adj1 = build_adj(G1)
    adj2 = build_adj(G2)
    deg1 = {node: len(neighbors) for node, neighbors in adj1.items()}
    deg2 = {node: len(neighbors) for node, neighbors in adj2.items()}

    if sorted(deg1.values()) != sorted(deg2.values()):
        return False, None

    sig1 = {node: node_signature(adj1, node, deg1) for node in adj1}
    sig2 = {node: node_signature(adj2, node, deg2) for node in adj2}

    candidates = {
        u: [v for v, s in sig2.items() if s == sig1[u]]
        for u in adj1
    }

    order = sorted(adj1, key=lambda u: (len(candidates[u]), sig1[u]))

    mapping = {}
    used = set()

    def backtrack(index=0):
        if index == len(order):
            return True

        u = order[index]
        for v in candidates[u]:
            if v in used:
                continue

            valid = True
            for nbr in adj1[u]:
                if nbr in mapping and mapping[nbr] not in adj2[v]:
                    valid = False
                    break
            if not valid:
                continue

            mapping[u] = v
            used.add(v)
            if backtrack(index + 1):
                return True
            used.remove(v)
            del mapping[u]

        return False

    if backtrack():
        return True, dict(mapping)

    return False, None

inv1 = invariants(G1)
inv2 = invariants(G2)
custom_iso, custom_mapping = is_isomorphic_custom(G1, G2)

GM = nx.isomorphism.GraphMatcher(G1, G2)
library_iso = GM.is_isomorphic()
mapping = GM.mapping if library_iso else None

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
ax = axes.flatten()

nx.draw(G1, pos=pos_G1, with_labels=True, node_color='skyblue', node_size=800, ax=ax[0])
ax[0].set_title("G1")

nx.draw(G2, pos=pos_G2, with_labels=True, node_color='lightgreen', node_size=800, ax=ax[1])
ax[1].set_title("G2")

plt.suptitle(
    f"Custom Isomorphism: {custom_iso}\n"
    f"Library Isomorphism: {library_iso}\n"
    f"Mapping: {mapping}"
)

plt.show()

print("Custom Isomorphism:", custom_iso)
print("Library Isomorphism:", library_iso)
print("Mapping:", mapping)
print("G1 Invariants:", inv1)
print("G2 Invariants:", inv2)