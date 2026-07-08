import math
import matplotlib.pyplot as plt

def create_graph():
    nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    
    edges = [
        ('a','b',4), ('b','c',8), ('c','d',7),
        ('d','e',9), ('e','f',10), ('f','g',2),
        ('g','h',1), ('h','b',11), ('h','i',7),
        ('i','c',2), ('i','g',6), ('c','f',4), ('d','f',14)
    ]
    
    adj = {n: [] for n in nodes}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
        
    return nodes, edges, adj

def dijkstra_steps(nodes, adj, source):
    dist = {n: float('inf') for n in nodes}
    dist[source] = 0
    visited = set()
    steps = []
    
    while len(visited) < len(nodes):
        u = None
        min_val = float('inf')
        for n in nodes:
            if n not in visited and dist[n] < min_val:
                min_val = dist[n]
                u = n
                
        if u is None: break
        
        visited.add(u)
        changed_edges = []
        
        for v, w in adj[u]:
            if v not in visited:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    changed_edges.append((u, v))
                    
        steps.append((visited.copy(), dist.copy(), u, changed_edges))
        
    return steps

def draw_graph(ax, nodes, edges, pos):
    for u, v, w in edges:
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        ax.plot(x, y, color="lightgray", zorder=1)
        
        mx = (pos[u][0] + pos[v][0]) / 2
        my = (pos[u][1] + pos[v][1]) / 2
        ax.text(mx, my, str(w), color="black", zorder=3, 
                bbox=dict(facecolor='white', edgecolor='none', pad=1, alpha=0.8))

def draw_nodes(ax, nodes, pos, visited, current):
    for n in nodes:
        x, y = pos[n]
        color = "pink"
        
        if n in visited:
            color = "orange"
        if n == current:
            color = "blue"
            
        ax.scatter(x, y, s=800, c=color, edgecolors="black", zorder=4)
        ax.text(x, y, str(n), ha='center', va='center', fontweight="bold", zorder=5)

def draw_step(ax, nodes, edges, pos, visited, dist, current, changed_edges, step):
    draw_graph(ax, nodes, edges, pos)
    
    for u, v in changed_edges:
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        ax.plot(x, y, color="red", linewidth=2.5, zorder=2)
        
    draw_nodes(ax, nodes, pos, visited, current)
    
    for n, (x, y) in pos.items():
        val = "∞" if dist[n] == float('inf') else str(dist[n])
        ax.text(x, y + 0.3, val, color="green", fontweight="bold", ha='center')
        
    ax.set_title("Step " + str(step) + " (Selected: " + str(current) + ")", pad=15)
    ax.axis("off")

def show_steps(nodes, edges, steps):
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
    rows = math.ceil(total / cols) if total > 0 else 1
    fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 4 * rows))
    
    if total == 1:
        axes = [axes]
    elif hasattr(axes, "flat"):
        axes = list(axes.flat)
        
    for i in range(total):
        visited, dist, current, changed_edges = steps[i]
        draw_step(axes[i], nodes, edges, pos, visited, dist, current, changed_edges, i + 1)
        
    for i in range(total, len(axes)):
        axes[i].remove()
        
    plt.tight_layout()
    fig.subplots_adjust(hspace=0.4) 
    plt.show()

nodes, edges, adj = create_graph()
source = 'a'
steps = dijkstra_steps(nodes, adj, source)
show_steps(nodes, edges, steps)
