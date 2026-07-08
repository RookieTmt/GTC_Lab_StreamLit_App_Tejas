import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
def find_hamiltonian_circuit(nodes, edges, start_node):
    adj = defaultdict(list)
    for u, v, _ in edges:
        adj[u].append(v)
        adj[v].append(u)
    n = len(nodes)
    def backtrack(path):
        if len(path) == n:
            if path[0] in adj[path[-1]]:
                return path + [path[0]]
            return None
        current = path[-1]
        for neighbor in adj[current]:
            if neighbor not in path:
                result = backtrack(path + [neighbor])
                if result:
                    return result
        return None
    return backtrack([start_node])
nodes = ['1', '2', '3', '4', '5', '6', '7']
edges = [
    ('1','2','e1'), ('2','3','e2'), ('3','4','e3'), ('4','5','e4'),
    ('5','6','e5'), ('6','1','e6'), ('2','7','e11'), ('7','5','e9'),
    ('3','7','e8'), ('7','6','e10'), ('3','5','e7'), ('2','6','e12')
]
G = nx.Graph()
for u, v, w in edges:
    G.add_edge(u, v, label=w)
pos = {
    '1': (-2, 0), '2': (-1, 1.5), '3': (1, 1.5),
    '4': (2, 0), '5': (1, -1.5), '6': (-1, -1.5), '7': (0, 0)
}
circuit = find_hamiltonian_circuit(nodes, edges, '1')
if circuit is None:
    print("Hamiltonian Circuit NOT Present")
else:
    print("Hamiltonian Circuit Present")
    edge_labels_dict = {(u, v): w for u, v, w in edges}
    result_str = []
    for i in range(len(circuit) - 1):
        u, v = circuit[i], circuit[i+1]
        e_label = edge_labels_dict.get((u, v)) or edge_labels_dict.get((v, u))
        result_str.append(f"{u} {e_label} ")
    result_str.append(circuit[-1])
    print("Hamiltonian Circuit:")
    print("".join(result_str))
fig, axs = plt.subplots(1, 2, figsize=(14, 6))
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
axs[0].set_title("Original Graph", fontsize=14, pad=15, fontweight='bold')
axs[0].axis('off')
nx.draw_networkx_nodes(G, pos, ax=axs[0], node_size=800, node_color='lightgray', edgecolors='gray')
nx.draw_networkx_labels(G, pos, ax=axs[0], font_size=12, font_weight='bold')
nx.draw_networkx_edges(G, pos, ax=axs[0], width=1.5, edge_color='gray')
nx.draw_networkx_edge_labels(G, pos, ax=axs[0], edge_labels=edge_labels, font_weight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))
axs[1].set_title("Hamiltonian Circuit", fontsize=14, pad=15, fontweight='bold')
axs[1].axis('off')
if circuit:
    nx.draw_networkx_nodes(G, pos, ax=axs[1], node_size=800, node_color='lightyellow', edgecolors='orange')
    nx.draw_networkx_labels(G, pos, ax=axs[1], font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, ax=axs[1], width=1.0, edge_color='lightgray')
    circuit_edges = list(zip(circuit, circuit[1:]))
    nx.draw_networkx_edges(G, pos, ax=axs[1], edgelist=circuit_edges, width=5.0, edge_color='darkred')
    nx.draw_networkx_edge_labels(G, pos, ax=axs[1], edge_labels=edge_labels, font_weight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))
else:
    axs[1].text(0.5, 0.5, "No Hamiltonian Circuit Found", ha='center', va='center', fontsize=14)
plt.tight_layout(pad=3.0)
plt.show()
