import networkx as nx
import matplotlib.pyplot as plt

edges_G1 = [
    (1, 2), (2, 3), (3, 4), (4, 1),
    (1, 9), (9, 10), (9, 8),
    (2, 12), (12, 5), (12, 10),
    (4, 5), (3, 8),
    (5, 6), (7, 8),
    (10, 11), (6, 7),
    (6, 11), (7, 11)
]

edges_G2 = [
    ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'),
    ('E', 'F'), ('F', 'G'), ('G', 'A'),
    ('G', 'H'), ('H', 'B'),
    ('F', 'L'), ('L', 'C'),
    ('H', 'I'), ('K', 'L'), ('I', 'K'),
    ('A', 'K'),
    ('I', 'J'), ('J', 'D'), ('E', 'J')
]

def build_adj(edges, nodes):
    adj = {node: set() for node in nodes}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj

def get_nodes(edges):
    return sorted({u for edge in edges for u in edge})

nodes_G1 = get_nodes(edges_G1)
nodes_G2 = get_nodes(edges_G2)

adj_G1 = build_adj(edges_G1, nodes_G1)
adj_G2 = build_adj(edges_G2, nodes_G2)

def find_all_simple_cycles(adj):
    cycles = set()
    
    def dfs(start, current, visited, parent):
        for neighbor in adj[current]:
            if neighbor == parent:
                continue
            if neighbor == start and len(visited) >= 3:
                cycle = list(visited)
                min_node = min(cycle)
                while cycle[0] != min_node:
                    cycle = cycle[1:] + cycle[:1]
                rev = list(reversed(cycle))
                if tuple(rev) < tuple(cycle):
                    cycle = rev
                cycles.add(tuple(cycle))
            elif neighbor not in visited:
                visited.append(neighbor)
                dfs(start, neighbor, visited, current)
                visited.pop()
    
    for start in sorted(adj):
        dfs(start, start, [start], None)
    
    return cycles

def min_cycle_info(adj):
    cycles = find_all_simple_cycles(adj)
    if not cycles:
        return None, 0
    min_len = min(len(c) for c in cycles)
    return min_len, sum(1 for c in cycles if len(c) == min_len)

def invariants(adj, nodes):
    num_nodes = len(nodes)
    num_edges = sum(len(neighbors) for neighbors in adj.values()) // 2
    degree_seq = tuple(sorted([len(adj[node]) for node in nodes], reverse=True))
    min_cycle, cycle_count = min_cycle_info(adj)
    
    return (num_nodes, num_edges, degree_seq, min_cycle, cycle_count)

def node_signature(adj, node):
    degree = len(adj[node])
    neighbor_degrees = tuple(sorted([len(adj[neigh]) for neigh in adj[node]]))
    return (degree, neighbor_degrees)

def is_isomorphic_custom(adj1, adj2, nodes1, nodes2):
    if len(nodes1) != len(nodes2):
        return False, None
    if sum(len(neighbors) for neighbors in adj1.values()) != sum(len(neighbors) for neighbors in adj2.values()):
        return False, None
    
    deg1 = {node: len(adj1[node]) for node in nodes1}
    deg2 = {node: len(adj2[node]) for node in nodes2}
    
    if sorted(deg1.values()) != sorted(deg2.values()):
        return False, None
    
    sig1 = {node: node_signature(adj1, node) for node in nodes1}
    sig2 = {node: node_signature(adj2, node) for node in nodes2}
    
    candidates = {u: [v for v in nodes2 if sig2[v] == sig1[u]] for u in nodes1}
    
    for u in nodes1:
        if not candidates[u]:
            return False, None
    
    order = sorted(nodes1, key=lambda u: (len(candidates[u]), sig1[u]))
    
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
            for neighbor in adj1[u]:
                if neighbor in mapping and mapping[neighbor] not in adj2[v]:
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

inv1 = invariants(adj_G1, nodes_G1)
inv2 = invariants(adj_G2, nodes_G2)
custom_iso, custom_mapping = is_isomorphic_custom(adj_G1, adj_G2, nodes_G1, nodes_G2)

pos_G1 = {
    4: (0, 0), 3: (10, 0), 2: (10, 10), 1: (0, 10),
    10: (5, 5), 9: (2.5, 7.5), 12: (7.5, 7.5),
    5: (1.25, 5), 8: (8.75, 5),
    11: (5, 3.75), 6: (3.75, 2.75), 7: (6.25, 2.75)
}

pos_G2 = {
    'A': (5, 10), 'B': (10, 6.67), 'C': (10, 3.33),
    'D': (6.67, 0), 'E': (3.33, 0), 'F': (0, 3.33), 'G': (0, 6.67),
    'H': (5, 7.5), 'I': (5, 5), 'J': (5, 2.5),
    'K': (3, 6.25), 'L': (3, 4.75)
}

def build_nx_graph(nodes, adj):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for u in nodes:
        for v in adj[u]:
            if u < v:
                G.add_edge(u, v)
    return G

G1_plot = build_nx_graph(nodes_G1, adj_G1)
G2_plot = build_nx_graph(nodes_G2, adj_G2)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes = axes.flatten()

nx.draw(G1_plot, pos=pos_G1, ax=axes[0], with_labels=True, node_color='skyblue', node_size=800)
axes[0].set_title("G1")

nx.draw(G2_plot, pos=pos_G2, ax=axes[1], with_labels=True, node_color='lightgreen', node_size=800)
axes[1].set_title("G2")

plt.suptitle(f"Custom Isomorphism: {custom_iso}\nMapping: {custom_mapping}")
plt.tight_layout()
plt.show()

print("Custom Isomorphism:", custom_iso)
print("Mapping:", custom_mapping)
print("G1 Invariants:", inv1)
print("G2 Invariants:", inv2)

