import networkx as nx
import matplotlib.pyplot as plt

# 1. Null graph with 5 vertices
G1 = nx.empty_graph(5)

# 2. Complete graph with 6 vertices
G2 = nx.complete_graph(6)

# 3. Complete bipartite graph with partitions 3 and 4
G3 = nx.complete_bipartite_graph(3, 4)

# 4. 8-vertex cycle graph
G4 = nx.cycle_graph(8)

# 5. Wheel graph with 1 central vertex + 5 cycle vertices
G5 = nx.wheel_graph(6)

# 6. Linear path graph with 5 vertices
G6 = nx.path_graph(5)

# Graph titles
titles = [
    "5-Vertex Null Graph",
    "6-Vertex Complete Graph",
    "5-Vertex Linear Graph",
    "Complete Bipartite Graph (3,4)",
    "8-Vertex Cycle Graph",
    "6-Vertex Wheel Graph",
]

graphs = [G1, G2, G6, G3, G4, G5]

# Create a 3x2 subplot grid
fig, axes = plt.subplots(2, 3, figsize=(12, 12))
axes = axes.flatten()

for ax, G, title in zip(axes, graphs, titles):
    # Use layouts best suited for each graph
    if G is G3:  # Bipartite
        pos = nx.bipartite_layout(G, nodes=range(3))
    elif G is G5:  # Wheel with central vertex in pentagram
        import math
        pos = {}
        pos[0] = (0, 0)  # Central vertex

        # 5 surrounding vertices in pentagram positions
        radius = 1.0
        angles_deg = [90, 162, 234, 306, 18]  # pentagram points
        for i, angle in enumerate(angles_deg):
            rad = math.radians(angle)
            pos[i+1] = (radius * math.cos(rad), radius * math.sin(rad))

    elif G in [G1, G2, G4]:
        pos = nx.circular_layout(G)
    else:  # Path graph
        pos = nx.spring_layout(G)
    
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color='skyblue',
        node_size=700,
        font_size=12,
        edge_color='gray'
    )
    ax.set_title(title)

plt.tight_layout()
plt.show()
