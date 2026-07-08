import networkx as nx
import matplotlib.pyplot as plt

def havel_hakimi_realize(degrees):
    """
    Verifies if a degree sequence is graphical using the Havel-Hakimi algorithm.
    If graphical, returns the adjacency list and the edges constructed at each step.
    
    Returns:
        is_graphical (bool): True if graphical, False otherwise.
        adj_list (dict): Adjacency list of the final graph.
        steps_info (list of dict): Logging information for each step.
        edges_at_step (list of lists): Edges in the graph at each step.
    """
    # Check 1: Must be all non-negative integers
    if any(d < 0 for d in degrees):
        return False, {}, [], []
        
    # Check 2: Sum of degrees must be even (Handshaking Lemma)
    if sum(degrees) % 2 != 0:
        return False, {}, [], []

    n = len(degrees)
    adj = {i: set() for i in range(n)}
    
    # Track the state: list of [remaining_degree, node_index]
    rem = [[d, i] for i, d in enumerate(degrees)]
    
    steps_info = []
    edges_at_step = []
    
    # Initial state (0 edges)
    edges_at_step.append([])
    steps_info.append({
        "desc": "Initial State (No connections)",
        "degrees": sorted([d for d in degrees], reverse=True),
        "edges_added": []
    })
    
    current_edges = set()
    
    while True:
        # Sort in descending order of remaining degrees
        rem.sort(key=lambda x: x[0], reverse=True)
        
        # If the largest remaining degree is 0, we're done
        if rem[0][0] == 0:
            if all(x[0] == 0 for x in rem):
                return True, adj, steps_info, edges_at_step
            else:
                return False, {}, [], []
        
        d, u = rem[0]
        rem[0][0] = 0  # Mark processed
        
        if d >= len(rem):
            return False, {}, [], []
            
        added_this_step = []
        
        # Connect u to the next d vertices
        for k in range(1, d + 1):
            rem[k][0] -= 1
            v = rem[k][1]
            
            # Record edge (sorted representation)
            edge = tuple(sorted((u, v)))
            current_edges.add(edge)
            added_this_step.append(edge)
            
            adj[u].add(v)
            adj[v].add(u)
            
            if rem[k][0] < 0:
                return False, {}, [], []
                
        # Record this step's information
        active_degrees = sorted([x[0] for x in rem if x[0] >= 0], reverse=True)
        steps_info.append({
            "desc": f"Processed Node {u} (degree {d})",
            "degrees": active_degrees,
            "edges_added": added_this_step
        })
        edges_at_step.append(list(current_edges))

def print_havel_hakimi_trace(degrees):
    print("=" * 60)
    print(f"Analyzing Degree Sequence: {degrees}")
    print("=" * 60)
    
    is_graphical, adj, steps_info, edges_at_step = havel_hakimi_realize(degrees)
    
    if not is_graphical:
        # Check if Handshaking Lemma failed or other check failed
        if any(d < 0 for d in degrees):
            print("Result: NOT GRAPHICAL (contains negative values).")
        elif sum(degrees) % 2 != 0:
            print("Result: NOT GRAPHICAL (sum of degrees is odd, violates Handshaking Lemma).")
        else:
            # Run the algorithm again to print where it failed
            print("Havel-Hakimi Reduction trace before failure:")
            temp_degrees = sorted(degrees, reverse=True)
            step_num = 0
            print(f"  Step {step_num}: {temp_degrees}")
            while temp_degrees and temp_degrees[0] > 0:
                d = temp_degrees[0]
                temp_degrees = temp_degrees[1:]
                if d > len(temp_degrees):
                    print(f"  Step {step_num + 1}: Cannot subtract 1 from the next {d} elements (only {len(temp_degrees)} left).")
                    break
                for k in range(d):
                    temp_degrees[k] -= 1
                if any(x < 0 for x in temp_degrees):
                    print(f"  Step {step_num + 1}: {temp_degrees} (contains negative values after subtraction).")
                    break
                temp_degrees = sorted(temp_degrees, reverse=True)
                step_num += 1
                print(f"  Step {step_num}: {temp_degrees}")
            print("\nResult: NOT GRAPHICAL.")
        print("=" * 60 + "\n")
        return False, {}, []
        
    print("Step-by-Step Construction Trace:")
    for idx, info in enumerate(steps_info):
        print(f"\n--- {info['desc']} ---")
        print(f"  Degree State: {info['degrees']}")
        if info['edges_added']:
            print(f"  Edges Added: {', '.join(str(e) for e in info['edges_added'])}")
            print(f"  Total Edges in Graph: {len(edges_at_step[idx])}")
            
    print("\nResult: The degree sequence is GRAPHICAL!")
    print("\nFinal Manually Constructed Adjacency List:")
    for node in sorted(adj.keys()):
        neighbors = sorted(list(adj[node]))
        print(f"  Node {node} (deg {len(neighbors)}): {neighbors}")
    print("=" * 60 + "\n")
    return True, adj, edges_at_step

def plot_construction_steps(edges_at_step, num_nodes):
    num_steps = len(edges_at_step)
    fig, axes = plt.subplots(1, num_steps, figsize=(4 * num_steps, 4.5))
    
    if num_steps == 1:
        axes = [axes]
        
    # Build final graph to compute layout positions
    G_final = nx.Graph()
    G_final.add_nodes_from(range(num_nodes))
    G_final.add_edges_from(edges_at_step[-1])
    
    # Consistent layout positions across all steps
    pos = nx.spring_layout(G_final, seed=42)
    
    for idx, step_edges in enumerate(edges_at_step):
        ax = axes[idx]
        G_step = nx.Graph()
        G_step.add_nodes_from(range(num_nodes))
        G_step.add_edges_from(step_edges)
        
        is_final = (idx == num_steps - 1)
        node_color = '#10B981' if is_final else '#6366F1' # Emerald for final, indigo for intermediate
        border_color = '#065F46' if is_final else '#312E81'
        
        # Draw nodes
        nx.draw_networkx_nodes(
            G_step, pos, 
            ax=ax,
            node_color=node_color,
            node_size=600,
            edgecolors=border_color,
            linewidths=2
        )
        
        # Draw edges
        nx.draw_networkx_edges(
            G_step, pos,
            ax=ax,
            edge_color='#94A3B8',
            width=2.5,
            alpha=0.8
        )
        
        # Draw labels
        nx.draw_networkx_labels(
            G_step, pos,
            ax=ax,
            font_color='white',
            font_family='sans-serif',
            font_weight='bold',
            font_size=11
        )
        
        title_text = "Initial State" if idx == 0 else f"Step {idx}\n(Added {len(step_edges) - len(edges_at_step[idx-1])} edges)"
        ax.set_title(title_text, fontsize=12, fontweight='bold', pad=10, color='#1E293B')
        ax.axis('off')
        
    plt.suptitle("Havel-Hakimi Step-by-Step Graph Realization", fontsize=15, fontweight='bold', y=1.02, color='#1E293B')
    plt.tight_layout()
    plt.show()

# --- Main Execution ---

# 1. Test graphical sequence from gt4.py: [4, 3, 3, 2, 2]
deg_seq_valid = [4, 3, 3, 2, 2]
is_graphical_valid, adj_valid, edges_steps_valid = print_havel_hakimi_trace(deg_seq_valid)

# 2. Test a non-graphical sequence (even sum, but not realizable):
deg_seq_invalid = [3, 3, 3, 1]
print_havel_hakimi_trace(deg_seq_invalid)

# 3. Plot the step-by-step construction of the valid graph
if is_graphical_valid:
    plot_construction_steps(edges_steps_valid, len(deg_seq_valid))
