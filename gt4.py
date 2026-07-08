import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

degree_sequence = [4, 3, 3, 2, 2]
n = len(degree_sequence)

# 1. Havel-Hakimi Graph 
G1 = nx.havel_hakimi_graph(degree_sequence)

# 2. Manual Graph Construction 
def manual_graph(degrees):
    adj_matrix = np.zeros((n, n), dtype=int)
    rem_degrees = [[d, i] for i, d in enumerate(degrees)]
    
    for i in range(n):
        rem_degrees.sort(key=lambda x: x[0], reverse=True)
        
        deg_i, node_i = rem_degrees[0]
        rem_degrees[0][0] = 0 
        
        for k in range(1, deg_i + 1):
            rem_degrees[k][0] -= 1
            node_j = rem_degrees[k][1]
            adj_matrix[node_i][node_j] = 1
            adj_matrix[node_j][node_i] = 1
            
    return nx.from_numpy_array(adj_matrix)

G2 = manual_graph(degree_sequence)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.title("Havel-Hakimi Graph")
nx.draw(G1, with_labels=True, node_color='lightblue')

plt.subplot(1, 2, 2)
plt.title("Manual Construction Graph")
nx.draw(G2, with_labels=True, node_color='lightcoral')

plt.show()