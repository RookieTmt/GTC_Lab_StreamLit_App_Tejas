import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
def path_to_edges(path):
    return [(str(path[i]), str(path[i+1])) for i in range(len(path)-1)]
def print_terminal_sequence(name, G, nodes):
    sequence_str = []
    for i in range(len(nodes) - 1):
        u, v = str(nodes[i]), str(nodes[i+1])
        if G.is_multigraph():
            edge_data = G[u][v]
            first_key = next(iter(edge_data))
            edge_label = edge_data[first_key]['label']
        else:
            edge_label = G[u][v]['label']
        sequence_str.append(f"V{u}")
        sequence_str.append(edge_label)
    sequence_str.append(f"V{nodes[-1]}")
    print(f"{name:<13}: {' '.join(sequence_str)}")
def draw_graph(ax, G, pos, highlight_edges=None, color='red', title=""):
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.axis('off')
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1000, node_color='#9cd3f0', edgecolors='black', linewidths=1.5)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=14, font_weight='bold', font_color='black')
    if G.is_multigraph():
        edge_rads = {}
        rad_values = [0.2, -0.2, 0.4, -0.4, 0.6, -0.6]
        pair_edges = {}
        for u, v, k in G.edges(keys=True):
            pair = tuple(sorted((u, v)))
            pair_edges.setdefault(pair, []).append((u, v, k))
        for pair, items in pair_edges.items():
            if len(items) == 1:
                edge_rads[(pair, items[0][2])] = 0.0
            else:
                for idx, item in enumerate(items):
                    edge_rads[(pair, item[2])] = rad_values[idx]
        for u, v, k in G.edges(keys=True):
            pair = tuple(sorted((u, v)))
            nx.draw_networkx_edges(
                G, pos, ax=ax, edgelist=[(u, v, k)], width=1.5,
                edge_color='#cccccc', connectionstyle=f'arc3,rad={edge_rads[(pair, k)]}'
            )
    else:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=G.edges(), width=1.5, edge_color='#cccccc')
    if highlight_edges:
        if G.is_multigraph():
            highlight_list = []
            for u, v in highlight_edges:
                if G.has_edge(u, v):
                    for key in G[u][v].keys():
                        highlight_list.append((u, v, key))
                elif G.has_edge(v, u):
                    for key in G[v][u].keys():
                        highlight_list.append((v, u, key))
            for u, v, k in highlight_list:
                pair = tuple(sorted((u, v)))
                nx.draw_networkx_edges(
                    G, pos, ax=ax, edgelist=[(u, v, k)], width=6.0, edge_color=color,
                    connectionstyle=f'arc3,rad={edge_rads[(pair, k)]}'
                )
        else:
            valid_edges = []
            for u, v in highlight_edges:
                if G.has_edge(u, v):
                    valid_edges.append((u, v))
                elif G.has_edge(v, u):
                    valid_edges.append((v, u))
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=valid_edges, width=6.0, edge_color=color)
    if G.is_multigraph():
        edge_labels = {(u, v, k): d['label'] for u, v, k, d in G.edges(keys=True, data=True) if d['label']}
    else:
        edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True) if d['label']}
    nx.draw_networkx_edge_labels(
        G, pos, ax=ax, edge_labels=edge_labels, font_size=10, font_color='black', font_weight='bold',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=1.5)
    )
G1 = nx.MultiGraph()
edges1 = [
    ('A','D','e1'), ('A','D','e2'),
    ('D','C','e3'), ('D','C','e4'),
    ('A','B','e5'), ('D','B','e6'), ('C','B','e7')
]
for u, v, w in edges1:
    G1.add_edge(u, v, label=w)
pos1 = {
    'A': (0, 8),
    'D': (0, 5),
    'C': (0, 2),
    'B': (5, 5)
}
# example sequences using letters
# Closed walk allows repeated edges; closed trail uses distinct edges, path is simple
g1_walk = ['A', 'D', 'A', 'B', 'D', 'C', 'B', 'A']
g1_trail = ['A', 'D', 'C', 'B', 'D', 'A']
g1_path = ['A', 'B', 'D', 'C']
G2 = nx.Graph()
edges2 = [('1','2','e1'), ('2','3','e2'), ('3','4','e3'), ('4','5','e4'), ('5','6','e5'), ('6','1','e6'), ('2','7','e11'), ('7','5','e9'), ('3','7','e8'), ('7','6','e10'), ('3','5','e7'), ('2','6','e12')]
for u, v, w in edges2:
    G2.add_edge(u, v, label=w)
pos2 = {'1': (-2, 0), '2': (-1, 1.5), '3': (1, 1.5), '4': (2, 0), '5': (1, -1.5), '6': (-1, -1.5), '7': (0, 0)}
g2_walk = [1, 2, 3, 4, 5, 7, 3, 2, 1]
g2_trail = [1, 2, 7, 3, 5, 7, 6, 1]
g2_path = [1, 2, 3, 4, 5, 6, 1]
print("\n" + "="*50 + "\nGRAPH G1\n" + "="*50)
print_terminal_sequence("Closed Walk", G1, g1_walk)
print_terminal_sequence("Closed Trail", G1, g1_trail)
print_terminal_sequence("Closed Path", G1, g1_path)
print("\n" + "="*50 + "\nGRAPH G2\n" + "="*50)
print_terminal_sequence("Closed Walk", G2, g2_walk)
print_terminal_sequence("Closed Trail", G2, g2_trail)
print_terminal_sequence("Closed Path", G2, g2_path)
print("="*50 + "\n")
fig1, axs1 = plt.subplots(2, 2, figsize=(10, 10))
fig1.canvas.manager.set_window_title('Experiment 8 - Graph G1')
draw_graph(axs1[0,0], G1, pos1, title="G1: Original Graph")
draw_graph(axs1[0,1], G1, pos1, highlight_edges=path_to_edges(g1_walk), color='#8b0000', title="G1: Closed Walk")
draw_graph(axs1[1,0], G1, pos1, highlight_edges=path_to_edges(g1_trail), color='#006400', title="G1: Closed Trail")
draw_graph(axs1[1,1], G1, pos1, highlight_edges=path_to_edges(g1_path), color='#00008b', title="G1: Closed Path")
plt.tight_layout()
fig2, axs2 = plt.subplots(2, 2, figsize=(10, 10))
fig2.canvas.manager.set_window_title('Experiment 8 - Graph G2')
draw_graph(axs2[0,0], G2, pos2, title="G2: Original Graph")
draw_graph(axs2[0,1], G2, pos2, highlight_edges=path_to_edges(g2_walk), color='#d6113c', title="G2: Closed Walk")
draw_graph(axs2[1,0], G2, pos2, highlight_edges=path_to_edges(g2_trail), color='#00c853', title="G2: Closed Trail")
draw_graph(axs2[1,1], G2, pos2, highlight_edges=path_to_edges(g2_path), color='#0066ff', title="G2: Closed Path")
plt.tight_layout()
plt.show()