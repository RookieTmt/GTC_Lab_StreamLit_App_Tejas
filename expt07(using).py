import math
import matplotlib.pyplot as plt
import networkx as nx
def create_graph():
    G = nx.Graph()
    # Nodes: a,b,c,d,e,f,g,h,i
    # Edges as provided: ab4, bc8, cd7, de9, ef10, fg2, gh1, hb11,
    # hi7, ic2, ig6, cf4, df14
    edges = [
        ('a','b',4), ('b','c',8), ('c','d',7),
        ('d','e',9), ('e','f',10), ('f','g',2),
        ('g','h',1), ('h','b',11), ('h','i',7),
        ('i','c',2), ('i','g',6), ('c','f',4), ('d','f',14)
    ]
    G.add_weighted_edges_from(edges)
    return G
def dijkstra_steps(G, source):
    dist = {node: float('inf') for node in G.nodes()}
    dist[source] = 0
    visited = set()
    steps = []
    while len(visited) < len(G.nodes()):
        u = None
        min_dist = float('inf')
        for node in G.nodes():
            if node not in visited and dist[node] < min_dist:
                min_dist = dist[node]
                u = node
        if u is None:
            break
        visited.add(u)
        changed_edges = []
        for v in G.neighbors(u):
            w = G[u][v]['weight']
            if v not in visited:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    changed_edges.append((u, v))
        steps.append((visited.copy(), dist.copy(), u, changed_edges))
    return steps, dist
def draw_step(ax, G, pos, visited, dist, current, changed_edges, step):
    nx.draw_networkx_edges(G, pos, edge_color="gray", ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=changed_edges, edge_color="red", width=2, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color="lightgray", node_size=900, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=list(visited), node_color="orange", node_size=900, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=[current], node_color="blue", node_size=900, ax=ax)
    # draw node labels slightly above nodes to avoid overlap with distance values
    label_pos = {node: (x, y + 0.5) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(G, label_pos, font_size=12, font_weight='bold', ax=ax)
    # draw edge labels with a subtle white bbox for readability
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=labels, font_size=9,
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.75),
        label_pos=0.5, rotate=False, ax=ax
    )
    # draw distance values below nodes to separate from node labels
    for node, (x, y) in pos.items():
        val = "∞" if dist[node] == float('inf') else str(dist[node])
        ax.text(x, y - 0.45, val, ha='center', color="green", fontweight='bold')
    ax.set_title("Step " + str(step) + " (" + str(current) + ")", fontsize=10)
    ax.axis("off")
def show_steps(G, steps, dist, source):
    pos = {
        'a': (0, 5),        # left poke-out
        'b': (2.5, 10),     # top-left
        'c': (5, 10),       # top-middle
        'd': (7.5, 10),     # top-right
        'e': (10, 5),       # right poke-out
        'f': (7.5, 0),      # bottom-right
        'g': (5, 0),        # bottom-middle
        'h': (2.5, 0),      # bottom-left
        'i': (4, 5)         # center
    }
    total = len(steps)
    cols = 2
    rows = math.ceil(total / cols)
    # make figure wider and scale by number of rows for readability
    fig = plt.figure(figsize=(18, max(6, 3 * rows)))
    for i in range(total):
        ax = plt.subplot2grid((rows, cols + 1), (i // cols, i % cols))
        visited, dist_step, current, changed_edges = steps[i]
        draw_step(ax, G, pos, visited, dist_step, current, changed_edges, i + 1)
    ax_table = plt.subplot2grid((rows, cols + 1), (0, cols), rowspan=rows)
    ax_table.axis('off')
    paths = nx.single_source_dijkstra_path(G, source)
    table_data = []
    for node in sorted(G.nodes()):
        path = " → ".join(map(str, paths[node]))
        cost = dist[node]
        table_data.append([f"{source} → {node}", path, cost])

    table = ax_table.table(
        cellText=table_data,
        colLabels=["From → To", "Path", "Cost"],
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)
    ax_table.set_xlim(0, 1)
    ax_table.set_title("Shortest Paths (Dijkstra)", fontsize=14, fontweight="bold")
    plt.subplots_adjust(wspace=0.3, hspace=0.4)
    plt.show()
G = create_graph()
source = 'a'
steps, final_dist = dijkstra_steps(G, source)
show_steps(G, steps, final_dist, source)
