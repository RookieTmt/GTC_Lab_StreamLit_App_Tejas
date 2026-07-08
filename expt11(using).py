import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_coloring():
    G = nx.Graph()
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    edges = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'),
        ('F', 'G'), ('G', 'H'), ('H', 'I'), ('I', 'J'), ('J', 'A'),
        ('B', 'D'), ('B', 'E'), ('E', 'G'), ('D', 'J'), ('E', 'I'),
        ('G', 'I')
    ]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    pos = {
        'A': (-4.0, -2.0),
        'B': (-4.0, 0.0),
        'C': (-3.0, 1.5),
        'D': (-2.0, 0.0),
        'J': (-2.0, -2.0),
        'E': (0.0, 0.0),
        'F': (1.0, 1.5),
        'G': (2.0, 0.0),
        'H': (2.0, -2.0),
        'I': (0.0, -2.0)
    }

    # Greedy coloring (NetworkX implementation)
    coloring = nx.coloring.greedy_color(G, strategy='largest_first')
    # Map color indices to a palette
    palette = ['#ff9999', '#99ff99', '#9999ff', '#ffcc99', '#c2c2f0', '#f0e68c']
    node_colors = [palette[coloring[n] % len(palette)] for n in G.nodes()]

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True,
            node_color=node_colors,
            node_size=1200,
            edge_color='gray',
            font_size=14,
            font_weight='bold',
            edgecolors='black')

    chromatic = max(coloring.values()) + 1 if coloring else 0
    plt.title(f'Experiment 11: Greedy Coloring (k={chromatic})', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

draw_graph_coloring()
