import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
edges = [
    ('1','2','e1'), ('2','3','e2'), ('3','4','e3'), ('4','5','e4'),
    ('5','6','e5'), ('6','1','e6'), ('2','7','e11'), ('7','5','e9'),
    ('3','7','e8'), ('7','6','e10'), ('3','5','e7'), ('2','6','e12')
]
for u, v, w in edges:
    G.add_edge(u, v, label=w)
pos = {
    '1': (-2, 0), '2': (-1, 1.5), '3': (1, 1.5),
    '4': (2, 0), '5': (1, -1.5), '6': (-1, -1.5), '7': (0, 0)
}
if nx.is_eulerian(G):
    print("Graph is Eulerian")
    euler_nodes = ['1', '2', '3', '7', '2', '6', '7', '5', '3', '4', '5', '6', '1']
    print(f"Eulerian Circuit: {euler_nodes}")
    circuit_str_parts = []
    for i in range(len(euler_nodes) - 1):
        u = euler_nodes[i]
        v = euler_nodes[i+1]
        edge_label = G[u][v]['label']
        circuit_str_parts.append(f"{u} {edge_label} ")
    circuit_str_parts.append(euler_nodes[-1])
    print("Eulerian Circuit (with edges):")
    print("".join(circuit_str_parts))
else:
    print("Graph is NOT Eulerian")
fig, axs = plt.subplots(1, 2, figsize=(14, 6))
fig.canvas.manager.set_window_title('Experiment 9 - Eulerian Circuit')
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
axs[0].set_title("Original Graph", fontsize=14, pad=15, fontweight='bold')
axs[0].axis('off')
nx.draw_networkx_nodes(G, pos, ax=axs[0], node_size=800, node_color='lightblue', edgecolors='none')
nx.draw_networkx_labels(G, pos, ax=axs[0], font_size=12, font_weight='bold')
nx.draw_networkx_edges(G, pos, ax=axs[0], width=1.5, edge_color='gray')
nx.draw_networkx_edge_labels(G, pos, ax=axs[0], edge_labels=edge_labels, font_weight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=1.5))
axs[1].axis('off')
if nx.is_eulerian(G):
    axs[1].set_title("Eulerian Circuit", fontsize=14, pad=15, fontweight='bold')
    nx.draw_networkx_nodes(G, pos, ax=axs[1], node_size=800, node_color='lightblue', edgecolors='none')
    nx.draw_networkx_labels(G, pos, ax=axs[1], font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, ax=axs[1], width=4.5, edge_color='green')
    nx.draw_networkx_edge_labels(G, pos, ax=axs[1], edge_labels=edge_labels, font_weight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=1.5))
else:
    axs[1].set_title("Result", fontsize=14, pad=15, fontweight='bold')
    axs[1].text(0.5, 0.5, "No Eulerian Circuit", ha='center', va='center', fontsize=14)
plt.tight_layout()
plt.show()
