import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def find_euler_circuit(edges, start_node):
    adj = defaultdict(list)
    for u, v, label in edges:
        adj[u].append((v, label))
        adj[v].append((u, label))
    used_edges = set()
    stack = [start_node]
    path = []
    while stack:
        v = stack[-1]
        found_edge = False
        while adj[v]:
            u, label = adj[v].pop()
            edge_id = tuple(sorted([u, v]))
            if edge_id not in used_edges:
                used_edges.add(edge_id)
                stack.append(u)
                found_edge = True
                break
        if not found_edge:
            path.append(stack.pop())
    return path[::-1]

def check_and_print_eulerian(nodes, edges, start_node):
    deg = defaultdict(int)
    for u, v, _ in edges:
        deg[u] += 1
        deg[v] += 1
    for n in nodes:
        if deg[n] % 2 != 0:
            print("Graph is NOT Eulerian")
            return None
    print("Graph is Eulerian")
    path_nodes = find_euler_circuit(edges, start_node)
    print(f"Eulerian Circuit: {path_nodes}")
    edge_lookup = {}
    for u, v, w in edges:
        edge_lookup[tuple(sorted([u, v]))] = w
    circuit_str = []
    for i in range(len(path_nodes) - 1):
        u, v = path_nodes[i], path_nodes[i+1]
        e_label = edge_lookup[tuple(sorted([u, v]))]
        circuit_str.append(f"{u} {e_label} ")
    circuit_str.append(path_nodes[-1])
    print("Eulerian Circuit (with edges):")
    print("".join(circuit_str))
    return path_nodes

def draw_euler_steps(G, pos, path):
    if not path:
        return
    num_steps = len(path)
    cols = 3
    rows = (num_steps + cols - 1) // cols
    
    fig = plt.figure(figsize=(15, 5 * rows))
    
    for i in range(num_steps):
        ax = plt.subplot(rows, cols, i + 1)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightgray', node_size=600)
        nx.draw_networkx_labels(G, pos, ax=ax, font_weight='bold')
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='lightgray', width=1.5)
        
        walk_edges = [(path[j], path[j+1]) for j in range(i)]
        if walk_edges:
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=walk_edges, edge_color='red', width=3.5)
            
        if i == 0:
            title = f"Start at {path[0]}"
        else:
            title = f"Step {i}: {path[i-1]} -> {path[i]}"
            
        ax.set_title(title, fontweight='bold', pad=10)
        ax.axis('off')
        
        ax.margins(0.30)
        
    plt.subplots_adjust(hspace=0.6, wspace=0.2, top=0.95, bottom=0.05)
    plt.show()

nodes = ['1', '2', '3', '4', '5', '6', '7']
edges = [
    ('1','2','e1'), ('2','3','e2'), ('3','4','e3'), ('4','5','e4'),
    ('5','6','e5'), ('6','1','e6'), ('2','7','e11'), ('7','5','e9'),
    ('3','7','e8'), ('7','6','e10'), ('3','5','e7'), ('2','6','e12')
]
G = nx.Graph()
for u, v, w in edges:
    G.add_edge(u, v, label=w)
pos = {
    '1': (-2, 0), '2': (-1, 1.5), '3': (1, 1.5),
    '4': (2, 0), '5': (1, -1.5), '6': (-1, -1.5), '7': (0, 0)
}
calculated_path = check_and_print_eulerian(nodes, edges, '1')
if calculated_path:
    draw_euler_steps(G, pos, calculated_path)
