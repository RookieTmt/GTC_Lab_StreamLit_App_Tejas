import io
import os
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="GT Graph Explorer", layout="wide")

BASE_DIR = Path(__file__).resolve().parent

# Experiment data structure (1 to 11) with Aim, Theory, and Conclusion
EXPERIMENTS = {
    1: {
        "title": "Basic Graph Structures",
        "aim": "To implement basic graphs such as complete graph, cycle graph, path graph and complete bipartite graph.",
        "theory": """
**Basic Graphs** form the structural foundations of graph theory:
*   **Null / Empty Graph**: A graph containing vertices but no edges. Useful as a starting point for graph construction.
*   **Complete Graph ($K_n$)**: A graph with $n$ vertices where every pair of distinct vertices is connected by a unique edge. The total number of edges is $\\frac{n(n-1)}{2}$.
*   **Cycle Graph ($C_n$)**: A graph consisting of a single closed loop containing all $n$ vertices, where every vertex has degree 2.
*   **Path Graph ($P_n$)**: A linear sequence of vertices connected by edges. The end vertices have degree 1, and all intermediate vertices have degree 2.
*   **Complete Bipartite Graph ($K_{m,n}$)**: A graph whose vertices are partitioned into two sets of size $m$ and $n$, and edges connect every vertex in the first set to every vertex in the second set.
*   **Wheel Graph ($W_n$)**: A graph of size $n$ formed by connecting a single central vertex to all vertices of a cycle graph of size $n-1$.
        """,
        "conclusion": "Null, complete, cycle, path, wheel, and complete bipartite graphs were successfully constructed and visualized using NetworkX and Matplotlib, verifying their structural properties and vertex/edge counts."
    },
    2: {
        "title": "Graph Isomorphism Verification",
        "aim": "To implement graph isomorphism verification in order to compare structural equivalence between two graphs.",
        "theory": """
**Graph Isomorphism** is a fundamental concept in graph theory that determines whether two graphs are structurally identical. 
Two graphs $G$ and $H$ are isomorphic if there exists a bijection (one-to-one correspondence) $f: V(G) \\rightarrow V(H)$ between their vertices such that 
two vertices $u$ and $v$ are adjacent in $G$ if and only if $f(u)$ and $f(v)$ are adjacent in $H$.

Graph isomorphism verification is used to identify equivalent graph structures, which has applications in:
*   **Chemistry**: Molecular structure comparison (checking if two chemical formulas represent the same structure).
*   **Network Analysis**: Finding equivalent sub-networks.
*   **Database Indexing**: Pattern matching and graph querying.

The problem is computationally challenging (in the NP-intermediate class), but several algorithms exist for checking invariants like degree sequences, node counts, and using refinement techniques.
        """,
        "conclusion": "Graph isomorphism verification was successfully implemented using both NetworkX and backtracking approaches, establishing structural equivalence between different graph drawings."
    },
    3: {
        "title": "Subgraph Generation",
        "aim": "To implement generation of various subgraphs such as induced subgraphs, spanning subgraphs and edge-deleted subgraphs.",
        "theory": """
**Subgraphs** are smaller graphs constructed from a subset of the original graph's vertices and edges:
*   **Induced Subgraph**: Created by selecting a subset of vertices $V' \\subseteq V$ and including *all* edges from the original graph that connect vertices in $V'$.
*   **Spanning Subgraph**: Contains *all* vertices of the original graph $V$ but only a subset of the edges $E' \\subseteq E$.
*   **Edge-Deleted Subgraph**: Formed by removing one or more edges from the original graph while preserving all original vertices.

Subgraphs are essential in analyzing graph properties, identifying connected components, finding cliques (fully connected subgraphs), and in optimization problems like finding the minimum spanning tree or solving the Steiner tree problem.
        """,
        "conclusion": "Induced subgraphs, spanning subgraphs, and edge-deleted subgraphs were successfully generated and visualized, illustrating how sub-structures inherit and modify characteristics of the parent graph."
    },
    4: {
        "title": "Degree Sequence (Havel-Hakimi)",
        "aim": "To implement construction of a graph for a given degree sequence in order to realize there is a graphical sequence using Havel-Hakimi algorithm.",
        "theory": """
**Degree Sequence** is a list of the degrees of all vertices in a graph, typically arranged in non-increasing order. A sequence of integers is **graphical** if there exists a simple graph whose degree sequence is exactly that sequence.

The **Havel-Hakimi Algorithm** is a recursive algorithm used to determine if a given degree sequence is graphical and, if so, construct a corresponding simple graph.

**Algorithm Steps**:
1.  Sort the degree sequence in non-increasing order.
2.  Remove the first element, let's call it $d$.
3.  Subtract 1 from the next $d$ largest elements in the sequence. If any element becomes negative, the sequence is *not graphical*.
4.  Repeat steps 1-3 until the sequence becomes all zeros (which is *graphical*) or an impossible state is reached (not graphical).
        """,
        "conclusion": "The Havel-Hakimi recursive algorithm was successfully implemented to verify if a degree sequence is graphical, constructing simple graphs from valid degree distributions."
    },
    5: {
        "title": "Graph to Line Graph Conversion",
        "aim": "To implement conversion of a given graph into a line graph where each vertex represents an edge of the original graph, and adjacency reflects shared endpoints.",
        "theory": """
**Line Graph** (also called the edge graph or derived graph) $L(G)$ of a graph $G$ is a transformation where:
*   Each vertex in $L(G)$ corresponds to an edge in the original graph $G$.
*   Two vertices in $L(G)$ are adjacent if and only if their corresponding edges in $G$ share a common endpoint (are incident).

For example, if $G$ has edge $(u, v)$ and edge $(v, w)$, the corresponding vertices in the line graph will be connected because they share vertex $v$.

Properties of line graphs:
*   The line graph of a complete graph $K_n$ is the line-symmetric structure.
*   Line graphs are useful in network design, circuit theory, and translating edge-coloring problems into vertex-coloring problems.
        """,
        "conclusion": "Graph-to-line-graph conversion was successfully achieved, representing edge adjacencies as vertices and validating line-graph structural properties."
    },
    6: {
        "title": "Minimum Spanning Tree (Kruskal's Algorithm)",
        "aim": "To implement finding the minimum spanning tree for a given graph using Kruskal's algorithm, ensuring all vertices are connected with the minimum possible total edge weight and without forming cycles.",
        "theory": """
**Minimum Spanning Tree (MST)** is a subset of edges in a weighted connected graph that connects all vertices together with the minimum total edge weight and without forming any cycles. For a graph with $V$ vertices, an MST has exactly $V-1$ edges.

**Kruskal's Algorithm** is a greedy algorithm:
1.  Sort all edges of the graph by weight in non-decreasing order.
2.  Iterate through the sorted edges, adding each edge if it does not create a cycle with the already selected edges.
3.  To detect cycles efficiently, a **Disjoint Set Union (DSU)** (or Union-Find) data structure is used.
4.  Stop when exactly $V-1$ edges have been added.

Time complexity is $O(E \\log E)$ or $O(E \\log V)$, which is highly efficient. MST has applications in network design (e.g., laying down cables), transportation, clustering, and routing.
        """,
        "conclusion": "Kruskal's algorithm with Disjoint Set Union (DSU) was successfully implemented to compute the Minimum Spanning Tree of a weighted graph, optimizing edge connectivity without cycles."
    },
    7: {
        "title": "Shortest Path Computation",
        "aim": "To implement shortest path algorithm in order to compute shortest path from the source vertex to all the vertices in a weighted graph.",
        "theory": """
**Shortest Path Problem** is finding a path between two vertices in a weighted graph such that the sum of the weights of the edges is minimized.

**Dijkstra's Algorithm** (for non-negative edge weights):
1.  Initialize distances to all vertices as infinity except the source vertex, which is 0.
2.  Maintain a set of unvisited vertices.
3.  Select the unvisited vertex with the minimum tentative distance.
4.  Update the tentative distances of all its unvisited neighbors.
5.  Mark the current vertex as visited.
6.  Repeat until all vertices are visited.

With a priority queue (binary heap), the time complexity is $O((V + E) \\log V)$. It is widely used in GPS navigation, routing protocols like OSPF, and game development pathfinding.
        """,
        "conclusion": "Dijkstra's single-source shortest path algorithm was successfully implemented, computing optimal path costs and trajectories to all vertices in a weighted graph."
    },
    8: {
        "title": "Closed Walks, Trails, and Paths",
        "aim": "To implement generation of closed walks, trails and paths in a connected graph.",
        "theory": """
In graph theory, we distinguish between three related concepts of traversals:
*   **Walk**: A sequence of vertices and edges where each consecutive pair is connected. Vertices and edges can be repeated.
*   **Trail**: A walk in which no edge is repeated. Vertices can be repeated.
*   **Path**: A trail in which no vertex is repeated (except possibly the first and last).

**Closed Traversals** start and end at the same vertex:
*   **Closed Walk**: Starts and ends at the same vertex, repetition allowed.
*   **Closed Trail (Circuit)**: A trail with the same start and end vertex where no edge is repeated.
*   **Closed Path (Cycle)**: A path where start and end vertices are the same.
        """,
        "conclusion": "Connected graph traversals including closed walks, trails, and paths were successfully generated, highlighting repetition restrictions for vertices and edges."
    },
    9: {
        "title": "Eulerian Circuit Identification and Construction",
        "aim": "To implement an algorithm that checks for the existence of an Eulerian circuit and construct a circuit that traverses every edge of the graph exactly once.",
        "theory": """
**Eulerian Circuit** is a closed trail that traverses every edge of a graph exactly once and returns to the starting vertex.

**Existence Conditions** (Euler's Theorem):
A connected graph has an Eulerian circuit if and only if every vertex has an *even degree*.
If a connected graph has exactly 2 vertices of odd degree, it has an **Eulerian Path** (but not a circuit).

**Hierholzer's Algorithm** (to construct an Eulerian circuit):
1.  Start at any vertex.
2.  Follow unvisited edges until stuck (returning to start). This forms a tour.
3.  If there are vertices with unvisited edges in the current tour, start a new tour from one such vertex and merge it into the main tour.
4.  Repeat until all edges are visited.
        """,
        "conclusion": "Eulerian circuit existence was verified based on vertex degrees, and Hierholzer's algorithm was successfully used to construct tours traversing every edge exactly once."
    },
    10: {
        "title": "Hamiltonian Circuit Verification",
        "aim": "To implement a method that determines whether a graph contains a Hamiltonian circuit i.e. a cycle that visits every vertex exactly once.",
        "theory": """
**Hamiltonian Circuit** is a cycle that visits every vertex of a graph exactly once and returns to the starting vertex.

Unlike Eulerian circuits (which depend on vertex degrees being even), finding a Hamiltonian circuit is an **NP-complete problem** with no known polynomial-time algorithm for general graphs.

**Existence Conditions (Sufficient, not necessary)**:
*   **Dirac's Theorem**: If every vertex in a graph of $n$ vertices has degree $\\ge n/2$, then the graph has a Hamiltonian circuit.
*   **Ore's Theorem**: If for every pair of non-adjacent vertices $u$ and $v$, $\\text{deg}(u) + \\text{deg}(v) \\ge n$, then the graph has a Hamiltonian circuit.

Typically implemented using backtracking or heuristic search for small graphs. It is the basis for the Traveling Salesperson Problem (TSP).
        """,
        "conclusion": "Backtracking was successfully applied to verify the existence of a Hamiltonian circuit, generating closed cycles visiting every vertex exactly once."
    },
    11: {
        "title": "Greedy Graph Coloring",
        "aim": "To implement the greedy graph coloring that assigns colors to the vertices such that no two adjacent vertices share the same color with minimal chromatic number.",
        "theory": """
**Graph Coloring** is the assignment of colors (labels) to the vertices of a graph such that no two adjacent vertices share the same color. The minimum number of colors needed is called the **Chromatic Number** $\\chi(G)$.

**Greedy Graph Coloring Algorithm**:
1.  Color the first vertex with the first color.
2.  For each subsequent vertex, check the colors of its neighbors.
3.  Assign the vertex the smallest color index that has not been assigned to any of its adjacent neighbors.
4.  If all colors are used, assign a new color.

Greedy coloring is efficient ($O(V + E)$) but doesn't guarantee the minimal chromatic number. It depends heavily on the ordering of the vertices. Strategies like ordering by largest degree first (Welch-Powell) help reduce the number of colors.
        """,
        "conclusion": "Greedy graph coloring was successfully implemented, assigning colors to vertices such that adjacent nodes have distinct colors, and demonstrating the impact of vertex ordering on the chromatic number."
    }
}

def get_experiment_files(exp_num: int):
    """Get all Python files for a given experiment number."""
    files = []
    
    if exp_num == 1:
        names = ["gt1.py"]
    elif exp_num == 2:
        names = ["gt2.py", "gt2_without_using.py"]
    elif exp_num == 3:
        names = ["gt3.py", "gt3_without_using.py"]
    elif exp_num == 4:
        names = ["gt4.py", "gt4_without_using.py"]
    else:
        # Experiments 5 to 11
        # Search dynamically on disk for exp{exp_num:02d} or expt{exp_num:02d}
        pattern1 = f"expt{exp_num:02d}*.py"
        pattern2 = f"exp{exp_num:02d}*.py"
        
        found = list(BASE_DIR.glob(pattern1)) + list(BASE_DIR.glob(pattern2))
        
        # Remove duplicates and self
        unique_found = []
        seen = set()
        for p in found:
            if p.is_file() and p.name != "streamlit_app.py" and p.name not in seen:
                seen.add(p.name)
                unique_found.append(p)
                
        # Sort key to ensure 'using' comes before 'without_using' and 'sudoku' behaves correctly
        def sort_key(p):
            n = p.name.lower()
            if "sudoku" in n:
                if "without" in n:
                    return 4
                return 3
            if "without" in n:
                return 2
            return 1
            
        unique_found = sorted(unique_found, key=sort_key)
        names = [p.name for p in unique_found]
        
    for name in names:
        path = BASE_DIR / name
        if path.exists():
            files.append((name, str(path)))
            
    return files

def execute_code(code_text: str, file_path: str, output_container):
    """Execute code and capture output."""
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    figures = []

    original_stdout = sys.stdout
    original_stderr = sys.stderr
    original_show = plt.show
    original_figure_show = matplotlib.figure.Figure.show

    def capture_show(*args, **kwargs):
        try:
            fig = plt.gcf()
            figures.append(fig)
        finally:
            plt.close("all")

    def capture_figure_show(self, *args, **kwargs):
        figures.append(self)
        plt.close(self)

    try:
        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer
        plt.show = capture_show
        matplotlib.figure.Figure.show = capture_figure_show

        exec_globals = {
            "__name__": "__main__",
            "__file__": file_path,
        }
        exec(code_text, exec_globals)
    except Exception as exc:
        with output_container:
            st.error(f"Execution error: {exc}")
            stderr_value = stderr_buffer.getvalue()
            if stderr_value:
                st.text(stderr_value)
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        plt.show = original_show
        matplotlib.figure.Figure.show = original_figure_show

    with output_container:
        stdout_value = stdout_buffer.getvalue()
        stderr_value = stderr_buffer.getvalue()

        if stdout_value:
            st.subheader("Console output")
            st.text(stdout_value)

        if stderr_value:
            st.subheader("Errors / warnings")
            st.text(stderr_value)

        if figures:
            st.subheader("Graph output")
            for fig in figures:
                st.pyplot(fig)
        else:
            if not stdout_value and not stderr_value:
                st.info("Code executed successfully. No console output or graph generated.")

# Apply custom premium aesthetics CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Code block font sizing */
    .stCodeBlock, .stCodeBlock code, pre, code {
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 14px !important;
    }
    
    /* Custom button styling */
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 12px -1px rgba(59, 130, 246, 0.4) !important;
    }
    
    button[data-testid="baseButton-secondary"] {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    button[data-testid="baseButton-secondary"]:hover {
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
    }
    
    /* Radio options list styling in sidebar */
    [data-testid="stSidebar"] .stRadio > div {
        background-color: rgba(30, 41, 59, 0.3);
        padding: 10px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Console & output formatting */
    .stText, pre {
        background-color: #0B0F19 !important;
        color: #10B981 !important;
        border: 1px solid #1E293B !important;
        border-radius: 6px !important;
        padding: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Build list of all available files grouped by experiment
sidebar_options = []
for i in range(1, 12):
    exp_title = EXPERIMENTS[i]["title"]
    files = get_experiment_files(i)
    for f_name, f_path in files:
        version_label = ""
        if "without_using" in f_name or "without" in f_name:
            if "sudoku" in f_name:
                version_label = "Sudoku (Manual)"
            else:
                version_label = "Manual"
        elif "using" in f_name:
            if "sudoku" in f_name:
                version_label = "Sudoku (Library)"
            else:
                version_label = "Library"
        
        if version_label:
            label = f"🔬 Exp {i} ({version_label}): {exp_title}"
        else:
            label = f"🔬 Exp {i}: {exp_title}"
            
        sidebar_options.append({
            "exp_num": i,
            "file_name": f_name,
            "file_path": f_path,
            "label": label
        })

# Initialize index in session state
if "selected_file_index" not in st.session_state:
    st.session_state.selected_file_index = 0

# Ensure the index is within bounds
st.session_state.selected_file_index = max(0, min(st.session_state.selected_file_index, len(sidebar_options) - 1))

# Sidebar layout
st.sidebar.markdown(
    """
    <div style="padding: 10px; background: linear-gradient(135deg, #1E1B4B 0%, #311042 100%); border-radius: 8px; margin-bottom: 20px;">
        <h3 style="color: #F8FAFC; margin: 0; font-size: 1.2rem; font-weight: 700; text-align: center;">📊 Graph Theory Lab</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Render flat sidebar radio list
selected_option = st.sidebar.radio(
    "Experiments Navigation",
    options=sidebar_options,
    index=st.session_state.selected_file_index,
    format_func=lambda opt: opt["label"]
)

# Debugging the mismatch
# Only run this if we have options to select from
if sidebar_options and selected_option in sidebar_options:
    current_index = sidebar_options.index(selected_option)
    st.session_state.selected_file_index = current_index
else:
    # Set a safe default if the list is empty or the selection is invalid
    st.session_state.selected_file_index = 0

# Extract details for selected option
if selected_option is not None and isinstance(selected_option, dict):
    selected_exp_num = selected_option["exp_num"]
    selected_file_name = selected_option["file_name"]
    selected_file_path = selected_option["file_path"]
else:
    # Handle the case where there is no valid selection yet
    selected_exp_num = None
    selected_file_name = None
    selected_file_path = None

# Main pane header: Subject Title & GEC Logo
header_col1, header_col2 = st.columns([1, 6])
with header_col1:
    logo_path = BASE_DIR / "gec_logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=100)
with header_col2:
    st.markdown(
        """
        <h1 style="background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.8rem; font-weight: 700; margin: 0; padding: 0;">
            Graph Theory (GT)
        </h1>
        <p style="color: #94A3B8; font-size: 1.1rem; margin: 5px 0 0 0; font-weight: 500;">Goa Engineering College (GEC) | Lab Portfolio</p>
        """,
        unsafe_allow_html=True
    )

# Determine the title safely
if selected_exp_num is not None and selected_exp_num in EXPERIMENTS:
    exp_title = EXPERIMENTS[selected_exp_num]['title']
else:
    exp_title = "Select an Experiment"

# Render the HTML using the safe variable
st.markdown(
    f"""
    <div style="border-bottom: 2px solid #1E293B; padding-bottom: 10px; margin-top: 15px; margin-bottom: 20px;">
        <h2 style="color: #F8FAFC; font-size: 1.8rem; font-weight: 600; margin: 0;">
            Experiment {selected_exp_num if selected_exp_num is not None else '...'}: {exp_title}
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Synchronized custom tabs inside the main pane
exp_files = get_experiment_files(selected_exp_num)

if len(exp_files) > 1:
    st.markdown("<p style='font-size: 0.95rem; color: #94A3B8; font-weight: 600; margin-bottom: 8px;'>Choose Implementation Version:</p>", unsafe_allow_html=True)
    cols = st.columns(len(exp_files))
    for idx, (f_name, f_path) in enumerate(exp_files):
        # Determine tab label
        tab_label = f_name
        if "without_using" in f_name or "without" in f_name:
            if "sudoku" in f_name:
                tab_label = "Sudoku (Manual)"
            else:
                tab_label = "Manual Implementation"
        elif "using" in f_name:
            if "sudoku" in f_name:
                tab_label = "Sudoku (Library)"
            else:
                tab_label = "Library Implementation"
        
        is_active = (f_name == selected_file_name)
        with cols[idx]:
            if st.button(
                tab_label,
                key=f"tab_btn_{f_name}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                # Update selected index
                for opt_idx, opt in enumerate(sidebar_options):
                    if opt["file_name"] == f_name:
                        st.session_state.selected_file_index = opt_idx
                        st.rerun()

# ----------------- SECTION 1: EXPERIMENT DETAILS -----------------
st.markdown("### 📋 Experiment Details")

# Display Aim card
st.markdown(
    f"""
    <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(59, 130, 246, 0.2); border-left: 5px solid #3B82F6; border-radius: 8px; padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <span style="font-weight: 700; color: #3B82F6; font-size: 1.1rem; display: block; margin-bottom: 5px;">🎯 Aim</span>
        <span style="color: #E2E8F0; font-size: 1.05rem; line-height: 1.5;">{EXPERIMENTS[selected_exp_num]['aim']}</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Display Theory Card header
st.markdown(
    f"""
    <div style="background: rgba(245, 158, 11, 0.05); border-left: 5px solid #F59E0B; padding: 12px 18px; border-radius: 0 8px 8px 0; margin-bottom: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <span style="font-weight: 700; color: #F59E0B; font-size: 1.1rem; display: block; margin-bottom: 0px;">📚 Theory</span>
    </div>
    """,
    unsafe_allow_html=True
)
# Render Markdown Theory content
st.markdown(EXPERIMENTS[selected_exp_num]['theory'])

# Display Conclusion Card header
st.markdown(
    f"""
    <div style="background: rgba(16, 185, 129, 0.05); border-left: 5px solid #10B981; padding: 12px 18px; border-radius: 0 8px 8px 0; margin-top: 20px; margin-bottom: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <span style="font-weight: 700; color: #10B981; font-size: 1.1rem; display: block; margin-bottom: 0px;">🏁 Conclusion</span>
    </div>
    """,
    unsafe_allow_html=True
)
# Render Conclusion content
st.markdown(EXPERIMENTS[selected_exp_num]['conclusion'])

st.divider()

# ----------------- SECTION 2: SOURCE CODE & OUTPUT -----------------
st.markdown("### 💻 Source Code & Output")

# Load selected file code
try:
    code_text = Path(selected_file_path).read_text(encoding="utf-8")
except Exception as e:
    code_text = f"# Error loading file: {e}"

# Source Code Subheader and expander
st.markdown(f"**Viewing file:** `{selected_file_name}` | *Location:* `{selected_file_path}`")
with st.expander("📝 View Source Code", expanded=True):
    st.code(code_text, language="python")

# Output Subheader & Execution Panel
st.markdown("#### 📊 Execution & Output")

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown(f"Click the button on the right to compile and run `{selected_file_name}`.")
with col2:
    run_button = st.button("Run Code", key=f"run_{selected_file_name}", type="primary", use_container_width=True)

output_container = st.container()

if run_button:
    execute_code(code_text, selected_file_path, output_container)

# ----------------- FOOTER -----------------
st.markdown(
    """
    <div style="text-align: center; padding: 25px; border-top: 1px solid #1E293B; margin-top: 50px; color: #94A3B8; font-size: 0.95rem; font-family: 'Outfit', sans-serif;">
        <strong>Tejas M. Tripathi</strong> | 24B-CO-072 | Semester 4
    </div>
    """,
    unsafe_allow_html=True
)
