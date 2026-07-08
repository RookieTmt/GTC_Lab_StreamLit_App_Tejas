import networkx as nx
import matplotlib.pyplot as plt

#Creating a base graph (Wheel Graph)
G = nx.wheel_graph(6)
pos = nx.spring_layout(G) 

#Built In Functions
# 1. Spanning Subgraph (Kruskal's)
spanning_edges = list(nx.minimum_spanning_edges(G, algorithm='kruskal', data=False))
G_spanning = nx.Graph()
G_spanning.add_nodes_from(G.nodes())
G_spanning.add_edges_from(spanning_edges)

# 2. Vertex-Induced Subgraph
G_v_induced = G.subgraph([0, 1, 2, 3])

# 3. Edge-Induced Subgraph
selected_edges = [(0, 1), (0, 2), (1, 2)]
G_e_induced = G.edge_subgraph(selected_edges)

#User Defined Functions
def manual_spanning(G, edges_to_keep):
    S = nx.Graph()
    S.add_nodes_from(G.nodes())
    S.add_edges_from(edges_to_keep)
    return S

def manual_vertex_induced(G, nodes_to_keep):
    VI = nx.Graph()
    VI.add_nodes_from(nodes_to_keep)
    for u, v in G.edges():
        if u in nodes_to_keep and v in nodes_to_keep:
            VI.add_edge(u, v)
    return VI

def manual_edge_induced(G, edges_to_keep):
    EI = nx.Graph()
    for u, v in edges_to_keep:
        if G.has_edge(u, v):
            EI.add_edge(u, v)
    return EI

#User Defined Graphs
nodes_subset = [0, 2, 4]
edges_subset = [(0, 1), (0, 5), (0, 2)]
G_spanning_user = manual_spanning(G, edges_subset)
G_v_induced_user = manual_vertex_induced(G, nodes_subset)
G_e_induced_user = manual_edge_induced(G, edges_subset)

#Ploting
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten() 
titles = [
    "Built-in: Spanning", "Built-in: Vertex-Induced", "Built-in: Edge-Induced",
    "Manual: Spanning", "Manual: Vertex-Induced", "Manual: Edge-Induced"
]

graphs = [
    G_spanning, G_v_induced, G_e_induced,
    G_spanning_user, G_v_induced_user, G_e_induced_user
]

for ax, g, title in zip(axes, graphs, titles):
    nx.draw(g, pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
    ax.set_title(title)

plt.tight_layout()
plt.show()