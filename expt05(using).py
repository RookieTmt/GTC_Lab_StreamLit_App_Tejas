import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
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
edges = [
    (1, 2, 'a'), (2, 3, 'b'), (3, 4, 'c'), 
    (4, 5, 'd'), (5, 6, 'e'), (6, 1, 'f'),
     (1, 7, 'g'), (2, 7, 'h'), (3, 8, 'i'), (4, 8, 'j'),
     (5, 8, 'k'), (6, 8, 'l'), (6, 7, 'm'), (7, 8, 'n')
]
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
G.add_weighted_edges_from(edges)
L = nx.line_graph(G)
labels_L = {e: G[e[0]][e[1]]['weight'] for e in L.nodes()}
pos_L = nx.kamada_kawai_layout(L)
fig, ax = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'width_ratios': [1, 1.5]})
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, ax=ax[0])
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v):w for u,v,w in edges}, ax=ax[0])
ax[0].set_title("ORIGINAL GRAPH", pad=15, fontweight='bold')
nx.draw(L, pos_L, labels=labels_L, node_color='lightgreen', node_size=600, ax=ax[1])
ax[1].set_title("CONVERTED LINE GRAPH", pad=15, fontweight='bold')
plt.tight_layout()
plt.show()