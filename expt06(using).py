import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
edges_data = [
    (1, 2, 10, 'a'), (2, 3, 0, 'b'), (3, 4, 8, 'c'), 
    (4, 5, 12, 'd'), (5, 6, 7, 'e'), (6, 1, 4, 'f'),
     (1, 7, 1, 'g'), (2, 7, 3, 'h'), (3, 8, 1, 'i'), (4, 8, 9, 'j'),
     (5, 8, 6, 'k'), (6, 8, 2, 'l'), (6, 7, 2, 'm'), (7, 8, 8, 'n')
]
for u, v, weight, label in edges_data:
    G.add_edge(u, v, weight=weight, label=label)
pos = {
    1: (0, 5),        
    2: (3.3, 10),    
    3: (6.7, 10),    
    4: (10, 5),         
    5: (6.7, 0),    
    6: (3.3, 0),  
    7: (3.3, 5),       
    8: (6.7, 5)     
}
edges_gen = nx.algorithms.tree.mst.kruskal_mst_edges(G, minimum=True, data=True)
mst_edges = []
cost = 0
for u, v, d in edges_gen:
    w = d['weight']
    mst_edges.append((u, v, w))
    cost += w

plt.figure(figsize=(10, 8)) 
nx.draw_networkx_nodes(G, pos, node_color="lightgray", edgecolors="black", node_size=700)
nx.draw_networkx_labels(G, pos, font_weight="bold")
nx.draw_networkx_edges(G, pos, edge_color="lightgray", style="dashed")

if mst_edges:
    edge_list = [(u, v) for u, v, w in mst_edges]
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color="black", width=2.5)
    edge_labels = {(u, v): f"{G[u][v]['label']}: {w}" for u, v, w in mst_edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red", font_weight="bold")

plt.title(f"Final Minimum Spanning Tree (Kruskal's Algorithm)\nTotal Cost = {cost}", fontsize=14, fontweight="bold", pad=15)
plt.axis("off")
plt.tight_layout() 
plt.show()

print("\nFinal MST Edges (Kruskal's Algorithm):")
print("-" * 40)
for u, v, w in mst_edges:
    label = G[u][v]['label']
    print(f"Edge: {label} ({u} - {v}) | Weight: {w}")
print("-" * 40)
print(f"Total Minimum Cost: {cost}")

