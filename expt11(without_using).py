import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx

def greedy_coloring(edges, nodes):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        
    color_map = {}
    for node in nodes:
        used_colors = {color_map[neighbor] for neighbor in adj[node] if neighbor in color_map}
        
        color = 0
        while color in used_colors:
            color += 1
            
        color_map[node] = color
        
    return color_map

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
    
    numeric_colors = greedy_coloring(edges, nodes)
    
    color_palette = ['red', 'lightgreen', 'lightblue', 'yellow', 'orange', 'purple']
    final_color_map = {node: color_palette[color_idx] for node, color_idx in numeric_colors.items()}
    
    print("Chromatic Number is:", len(set(final_color_map.values())))
    print("Color Map:")
    for node, color in final_color_map.items():
        print(f"  {node}: {color}")

    colored_nodes = [final_color_map[node] for node in G.nodes()]
    
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 2, 1)
    nx.draw(G, pos, with_labels=True, 
            node_color="pink", 
            node_size=1500, 
            edge_color="gray", 
            font_size=12, 
            font_weight="bold",
            edgecolors="black") 
    plt.title("Original Graph", fontsize=14, fontweight="bold")
    
    plt.subplot(1, 2, 2)
    nx.draw(G, pos, with_labels=True, 
            node_color=colored_nodes, 
            node_size=1500, 
            edge_color="gray", 
            font_size=12, 
            font_weight="bold",
            edgecolors="black")
    plt.title("Colored Graph", fontsize=14, fontweight="bold")
    
    plt.tight_layout()
    plt.show()

draw_graph_coloring()
