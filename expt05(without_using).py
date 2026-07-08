import matplotlib.pyplot as plt
import itertools
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
edge_nodes = edges
L_edges = []
for e1, e2 in itertools.combinations(edge_nodes, 2):
    if set(e1[:2]) & set(e2[:2]):
        L_edges.append((e1, e2))
pos_L = {}
for e in edge_nodes:
    u, v, w = e
    mid_x = (pos[u][0] + pos[v][0]) / 2
    mid_y = (pos[u][1] + pos[v][1]) / 2
    pos_L[e] = (mid_x, mid_y)
fig, ax = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'width_ratios':[1, 1]})
for (u,v,w) in edges:
    x = [pos[u][0], pos[v][0]]
    y = [pos[u][1], pos[v][1]]
    ax[0].plot(x, y, color='gray', zorder=1)
    ax[0].text((x[0]+x[1])/2 + 0.1, (y[0]+y[1])/2 + 0.1, w, fontweight='bold')
for n, (x,y) in pos.items():
    ax[0].scatter(x, y, color='lightblue', edgecolors='black', s=600, zorder=2)
    ax[0].text(x, y, n, ha='center', va='center', fontweight='bold', zorder=3)
ax[0].set_title("ORIGINAL GRAPH", pad=15, fontweight='bold')
ax[0].axis('off')
for (e1, e2) in L_edges:
    x = [pos_L[e1][0], pos_L[e2][0]]
    y = [pos_L[e1][1], pos_L[e2][1]]
    ax[1].plot(x, y, color='gray', linewidth=1, zorder=1)
for e, (x,y) in pos_L.items():
    ax[1].scatter(x, y, color='lightgreen', edgecolors='black', s=500, zorder=2)
    ax[1].text(x, y, e[2], ha='center', va='center', fontweight='bold', zorder=3)
ax[1].set_title("CONVERTED LINE GRAPH (Midpoint Layout)", pad=15, fontweight='bold')
ax[1].axis('off')
plt.tight_layout()
plt.show()