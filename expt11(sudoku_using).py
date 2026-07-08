import networkx as nx
import matplotlib.pyplot as plt
solved_board = [
    [3, 1, 4, 2],
    [2, 4, 1, 3],
    [1, 2, 3, 4],
    [4, 3, 2, 1]
]
G = nx.Graph()
def vertex(row, col):
    return row * 4 + col
row_edges_set = set()
for row in range(4):
    for col1 in range(4):
        for col2 in range(col1 + 1, 4):
            e = frozenset([vertex(row, col1), vertex(row, col2)])
            row_edges_set.add(e)
col_edges_set = set()
for col in range(4):
    for row1 in range(4):
        for row2 in range(row1 + 1, 4):
            e = frozenset([vertex(row1, col), vertex(row2, col)])
            col_edges_set.add(e)
sub_edges_set = set()
for box_row in range(2):
    for box_col in range(2):
        cells = []
        for r in range(box_row * 2, box_row * 2 + 2):
            for c in range(box_col * 2, box_col * 2 + 2):
                cells.append(vertex(r, c))
        for i in range(len(cells)):
            for j in range(i + 1, len(cells)):
                e = frozenset([cells[i], cells[j]])
                sub_edges_set.add(e)
col_only = col_edges_set - row_edges_set
sub_only = sub_edges_set - row_edges_set - col_edges_set
def to_tuples(edge_set):
    return [tuple(sorted(e)) for e in sorted(edge_set)]
row_edge_list = to_tuples(row_edges_set)
col_edge_list = to_tuples(col_only)
sub_edge_list = to_tuples(sub_only)
def assign_curvatures(edge_list, base_rad):
    result = []
    for i, e in enumerate(edge_list):
        sign = 1 if i % 2 == 0 else -1
        result.append((e, sign * base_rad))
    return result
row_curved = assign_curvatures(row_edge_list, 0.12)
col_curved = assign_curvatures(col_edge_list, 0.25)
sub_curved = assign_curvatures(sub_edge_list, 0.40)
pos = {}
for row in range(4):
    for col in range(4):
        v = vertex(row, col)
        pos[v] = (col * 3.0, (3 - row) * 3.0)
        G.add_node(v)
color_hex = {1: "#D94F4F", 2: "#4DB86B", 3: "#4A90D9", 4: "#E6C13D"}
node_colors = [color_hex[solved_board[n // 4][n % 4]] for n in sorted(G.nodes())]
value_labels = {v: str(solved_board[v // 4][v % 4]) for v in G.nodes()}
fig, ax = plt.subplots(figsize=(15, 7.5))
ax.set_facecolor("#F8F8F8")
fig.patch.set_facecolor("#F8F8F8")
ax.set_title("4X4 sudoku coloring", fontsize=18, fontweight="bold", color="#1A1A1A", pad=14)
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1600, edgecolors="#333333", linewidths=1.8, ax=ax)
for (u, v), rad in row_curved:
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color="#888888", width=1.2, arrows=True, arrowstyle="-", connectionstyle=f"arc3,rad={rad}", ax=ax)
for (u, v), rad in col_curved:
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color="#5599CC", width=1.2, arrows=True, arrowstyle="-", connectionstyle=f"arc3,rad={rad}", ax=ax)
for (u, v), rad in sub_curved:
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color="#CC7733", width=1.2, arrows=True, arrowstyle="-", connectionstyle=f"arc3,rad={rad}", ax=ax)
nx.draw_networkx_labels(G, pos, labels=value_labels, font_size=16, font_color="white", font_weight="bold", ax=ax)
ax.set_ylim(-1.5, 10.5)
ax.axis("off")
plt.tight_layout()
plt.show()