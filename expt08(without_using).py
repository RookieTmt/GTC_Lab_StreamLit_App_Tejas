import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
def path_to_edges(path):
    return [(str(path[i]), str(path[i+1])) for i in range(len(path)-1)]

def print_terminal_sequence(name, G, nodes):
    sequence_str = []
    for i in range(len(nodes) - 1):
        u, v = str(nodes[i]), str(nodes[i+1])
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
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=G.edges(), width=1.5, edge_color='#cccccc')
    if highlight_edges:
        valid_edges = []
        for u, v in highlight_edges:
            if G.has_edge(u, v): valid_edges.append((u, v))
            elif G.has_edge(v, u): valid_edges.append((v, u))
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=valid_edges, width=6.0, edge_color=color)
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True) if d['label']}
    nx.draw_networkx_edge_labels(
        G, pos, ax=ax, edge_labels=edge_labels, font_size=10, font_color='black', font_weight='bold',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=1.5)
    )
G1 = nx.Graph()
edges1 = [
    ('1','2','e1'), ('2','3','e2'), ('3','4','e3'), ('4','5','e4'),
    ('5','6','e5'), ('6','1','e6'), ('2','7','e11'), ('7','5','e9'),
    ('3','7','e8'), ('7','6','e10'), ('3','5','e7'), ('2','6','e12')
]
for u, v, w in edges1:
    G1.add_edge(u, v, label=w)
pos1 = {
    '1': (-2, 0), '2': (-1, 1.5), '3': (1, 1.5),
    '4': (2, 0), '5': (1, -1.5), '6': (-1, -1.5), '7': (0, 0)
}
g1_walk = ['1', '2', '3', '4', '5', '7', '3', '2', '1']
g1_trail = ['1', '2', '7', '5', '4', '3', '2', '6', '1']
g1_path = ['1', '2', '3', '4', '5', '6', '1']
G2 = nx.Graph()
edges2 = [
    ('1','2','e1'), ('2','3','e2'), ('3','4','e3'), ('4','5','e4'), 
    ('5','6','e5'), ('6','1','e6'), ('2','7','e11'), ('7','5','e9'), 
    ('3','7','e8'), ('7','6','e10'), ('3','5','e7'), ('2','6','e12')
]
for u, v, w in edges2: 
    G2.add_edge(u, v, label=w)
pos2 = {
    '1': (-2, 0), '2': (-1, 1.5), '3': (1, 1.5),
    '4': (2, 0), '5': (1, -1.5), '6': (-1, -1.5), '7': (0, 0)
}
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
draw_graph(axs1[0,1], G1, pos1, highlight_edges=path_to_edges(g1_walk), color='#d6113c', title="G1: Closed Walk")
draw_graph(axs1[1,0], G1, pos1, highlight_edges=path_to_edges(g1_trail), color='#00c853', title="G1: Closed Trail")
draw_graph(axs1[1,1], G1, pos1, highlight_edges=path_to_edges(g1_path), color='#0066ff', title="G1: Closed Path")
plt.tight_layout()
fig2, axs2 = plt.subplots(2, 2, figsize=(10, 10))
fig2.canvas.manager.set_window_title('Experiment 8 - Graph G2')
draw_graph(axs2[0,0], G2, pos2, title="G2: Original Graph")
draw_graph(axs2[0,1], G2, pos2, highlight_edges=path_to_edges(g2_walk), color='#d6113c', title="G2: Closed Walk")
draw_graph(axs2[1,0], G2, pos2, highlight_edges=path_to_edges(g2_trail), color='#00c853', title="G2: Closed Trail")
draw_graph(axs2[1,1], G2, pos2, highlight_edges=path_to_edges(g2_path), color='#0066ff', title="G2: Closed Path")
plt.tight_layout()
plt.show()
