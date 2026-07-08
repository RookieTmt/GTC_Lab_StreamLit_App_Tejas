import networkx as nx
import matplotlib.pyplot as plt

degree_sequence = [4, 3, 3, 2, 2]
n = len(degree_sequence)


def manual_havel_hakimi(degrees):
    adj_matrix = [[0] * n for _ in range(n)]
    rem_degrees = [[deg, idx] for idx, deg in enumerate(degrees)]

    for _ in range(n):
        rem_degrees.sort(key=lambda x: x[0], reverse=True)
        if rem_degrees[0][0] == 0:
            break

        deg_i, node_i = rem_degrees[0]
        rem_degrees[0][0] = 0

        if deg_i > len([r for r in rem_degrees[1:] if r[0] > 0]):
            raise ValueError("Degree sequence is not graphical")

        for k in range(1, deg_i + 1):
            rem_degrees[k][0] -= 1
            node_j = rem_degrees[k][1]
            adj_matrix[node_i][node_j] = 1
            adj_matrix[node_j][node_i] = 1

    return adj_matrix


def adj_matrix_to_networkx(adj_matrix):
    G = nx.Graph()
    G.add_nodes_from(range(len(adj_matrix)))
    for i in range(len(adj_matrix)):
        for j in range(i + 1, len(adj_matrix)):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)
    return G


manual_adj_matrix = manual_havel_hakimi(degree_sequence)
manual_degrees = [sum(row) for row in manual_adj_matrix]

print("Degree sequence:", degree_sequence)
print("Constructed adjacency matrix:")
for row in manual_adj_matrix:
    print(row)
print("Node degrees:", manual_degrees)

G_manual = adj_matrix_to_networkx(manual_adj_matrix)
pos = nx.spring_layout(G_manual)

plt.figure(figsize=(8, 6))
nx.draw(G_manual, pos, with_labels=True, node_color='lightcoral', edge_color='gray', node_size=700)
plt.title("Manual Havel-Hakimi Graph")
plt.show()
