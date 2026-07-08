import matplotlib.pyplot as plt
import math
n = 9
edges = [
    (1, 2, 10, 'a'), (2, 3, 0, 'b'), (3, 4, 8, 'c'), 
    (4, 5, 12, 'd'), (5, 6, 7, 'e'), (6, 1, 4, 'f'),
     (1, 7, 1, 'g'), (2, 7, 3, 'h'), (3, 8, 1, 'i'), (4, 8, 9, 'j'),
     (5, 8, 6, 'k'), (6, 8, 2, 'l'), (6, 7, 2, 'm'), (7, 8, 8, 'n')
]
edges.sort(key=lambda x: x[2])
edge_label_map = {}
for u, v, w, lbl in edges:
    edge_label_map[(u, v)] = lbl
    edge_label_map[(v, u)] = lbl
mst_edges = []
steps = []
cost = 0
steps.append(([], 0))
adj = {i: [] for i in range(n)}
def has_path(u, v, visited):
    if u == v:
        return True
    visited.add(u)
    for nei in adj[u]:
        if nei not in visited:
            if has_path(nei, v, visited):
                return True
    return False
for u, v, w, lbl in edges:
    if not has_path(u, v, set()):
        mst_edges.append((u, v, w))
        cost += w
        adj[u].append(v)
        adj[v].append(u)
        steps.append((mst_edges.copy(), cost))
        if len(mst_edges) == n - 1:
            break
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
cols = 3
rows = math.ceil(len(steps) / cols)
plt.figure(figsize=(15, 6 * rows))
for i, (edges_list, c) in enumerate(steps):
    ax = plt.subplot(rows, cols, i + 1)
    for u, v, w, lbl in edges:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        plt.plot([x1, x2], [y1, y2], color='lightgray', linestyle='dashed', zorder=1)
        # draw edge label near the midpoint for reference
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        plt.text(mx, my + 0.2, lbl, color='blue', zorder=4, fontsize=10)
    for node in pos:
        x, y = pos[node]
        plt.scatter(x, y, color='lightgray', edgecolors='black', s=700, zorder=3)
        plt.text(x, y, str(node), ha='center', va='center', fontweight='bold', zorder=4)
    for u, v, w in edges_list:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        plt.plot([x1, x2], [y1, y2], color='black', linewidth=2.5, zorder=2)
        lbl = edge_label_map.get((u, v), '')
        plt.text((x1+x2)/2, (y1+y2)/2, f"{lbl}: {w}", color='red', fontweight='bold', zorder=5)
    plt.title(f"Step {i}\nCost = {c}", fontsize=14, fontweight="bold", pad=15)
    plt.axis("off")
plt.tight_layout(pad=3.0)
plt.show()
print("\nMST Edges:")
for u, v, w in mst_edges:
    lbl = edge_label_map.get((u, v), '')
    print(f"{lbl} ({u} - {v}) : {w}")
print("Total Cost:", cost)