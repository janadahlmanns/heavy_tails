import networkx as nx
import json
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import csv

# Parameters
n_nodes = 60  # Total number of nodes
m_edges = 4   # Number of edges each new node attaches to (controls heavy-tailedness)

# Generate Barabási-Albert network
# This creates preferential attachment: nodes with higher degree attract more connections
graph = nx.barabasi_albert_graph(n_nodes, m_edges)

# Compute spring layout (Fruchterman-Reingold algorithm)
# This naturally spreads out nodes and looks nice
pos = nx.spring_layout(graph, k=1.0, iterations=50, seed=42)

# Normalize positions to Manim coordinate space
# Manim typically uses [-8, 8] for x and [-4.5, 4.5] for y in standard view
# Let's normalize to [-5, 5] for x and [-3, 3] for y to give some margin
pos_normalized = {}
x_coords = [p[0] for p in pos.values()]
y_coords = [p[1] for p in pos.values()]

x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)

x_scale = (5 - (-5)) / (x_max - x_min) if x_max != x_min else 1
y_scale = (3 - (-3)) / (y_max - y_min) if y_max != y_min else 1

for node, (x, y) in pos.items():
    x_norm = -5 + (x - x_min) * x_scale
    y_norm = -3 + (y - y_min) * y_scale
    pos_normalized[node] = [x_norm, y_norm]

# Collect node data
nodes_data = []
for node in graph.nodes():
    degree = graph.degree(node)
    nodes_data.append({
        'id': int(node),
        'x': float(pos_normalized[node][0]),
        'y': float(pos_normalized[node][1]),
        'degree': int(degree)
    })

# Calculate degree distribution
degrees = [node['degree'] for node in nodes_data]
degree_counts = Counter(degrees)
degree_distribution = [
    {'degree': k, 'count': v} 
    for k, v in sorted(degree_counts.items())
]

print(f"Network generated")
print(f"Nodes: {n_nodes}")
print(f"Edges: {len(list(graph.edges()))}")
print(f"Degree range: {min(degrees)} - {max(degrees)}")
print(f"Average degree: {np.mean(degrees):.2f}")
print(f"Degree distribution: {degree_distribution}")

# Quick visualization - 16:9 aspect ratio
# Network: 6 high x 6 wide, Histogram: 6 high x 5 wide
fig = plt.figure(figsize=(14.4, 7.2))  # 14.4:7.2 = 2:1 = 16:9
gs = fig.add_gridspec(1, 2, width_ratios=[6, 5], hspace=0.3, wspace=0.3)

# Left plot: Network graph (6x6 square)
ax_network = fig.add_subplot(gs[0, 0])
nx.draw_networkx_nodes(graph, pos, node_color='#E79E16', node_size=300, ax=ax_network)
nx.draw_networkx_edges(graph, pos, alpha=0.3, ax=ax_network)
nx.draw_networkx_labels(graph, pos, font_size=8, ax=ax_network)
ax_network.set_title('Barabási-Albert Network', fontsize=12, fontweight='bold')
ax_network.set_aspect('equal')
ax_network.set_xlabel('X', fontsize=10)
ax_network.set_ylabel('Y', fontsize=10)
ax_network.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax_network.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax_network.tick_params(labelsize=8, labelbottom=True, labelleft=True)
# Remove top and right spines, keep bottom and left for axes
ax_network.spines['top'].set_visible(False)
ax_network.spines['right'].set_visible(False)
ax_network.spines['bottom'].set_visible(True)
ax_network.spines['left'].set_visible(True)

# Right plot: Degree distribution histogram (6x5)
ax_hist = fig.add_subplot(gs[0, 1])
ax_hist.bar(
    [d['degree'] for d in degree_distribution],
    [d['count'] for d in degree_distribution],
    color='#E79E16',
    alpha=0.7,
    edgecolor='black'
)
ax_hist.set_xlabel('Degree', fontsize=11)
ax_hist.set_ylabel('Number of Nodes', fontsize=11)
ax_hist.set_title('Degree Distribution', fontsize=12, fontweight='bold')
ax_hist.grid(axis='y', alpha=0.3)
# Add border
for spine in ax_hist.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(2)
    spine.set_edgecolor('black')

plt.tight_layout()
plt.savefig('network_visualization.png', dpi=150, bbox_inches='tight')
print(f"\nVisualization saved to network_visualization.png")
plt.show()

# Rebuild network incrementally to capture degree evolution
degree_evolution = {}  # {node_id: [degrees at each step]}

# Start with initial nodes (nodes 0 to m_edges)
growing_graph = nx.Graph()
growing_graph.add_nodes_from(range(m_edges + 1))

# Initialize degree evolution for first nodes
for node in growing_graph.nodes():
    degree_evolution[node] = [0]

# Simulate BA network growth by adding nodes sequentially
for new_node in range(m_edges + 1, n_nodes):
    growing_graph.add_node(new_node)
    
    # Find which nodes this new node connects to (simulate BA attachment)
    # We'll use the edges from the final BA graph that involve new_node
    neighbors_of_new = [n for n in graph.neighbors(new_node)]
    
    # Add edges to growing graph
    for neighbor in neighbors_of_new:
        if neighbor < new_node:  # Only add if neighbor was added before
            growing_graph.add_edge(new_node, neighbor)
    
    # Record degrees for all nodes that exist at this step
    for node in range(new_node + 1):
        if node not in degree_evolution:
            degree_evolution[node] = []
        degree_evolution[node].append(growing_graph.degree(node))

# Write network data to CSV with degree evolution
csv_path = 'network_data.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Header: node_id, x, y, then degree_0, degree_1, ..., degree_n_nodes-1, then targets
    header = ['node_id', 'x', 'y']
    for i in range(n_nodes):
        header.append(f'degree_at_node_{i}')
    
    # Add placeholder headers for targets
    max_neighbors = max(graph.degree(node) for node in graph.nodes())
    for i in range(max_neighbors):
        header.append(f'target_{i}_x')
        header.append(f'target_{i}_y')
    writer.writerow(header)
    
    # Write each node's data
    for node in graph.nodes():
        x, y = pos_normalized[node]
        neighbors = list(graph.neighbors(node))
        
        # Filter neighbors: only include if neighbor_id > node_id
        neighbors_filtered = [n for n in neighbors if n > node]
        
        row = [node, x, y]
        
        # Add degree evolution
        if node in degree_evolution:
            row.extend(degree_evolution[node])
        
        # Add neighbor coordinates as pairs
        for neighbor in neighbors_filtered:
            neighbor_x, neighbor_y = pos_normalized[neighbor]
            row.append(neighbor_x)
            row.append(neighbor_y)
        
        writer.writerow(row)

print(f"Network data saved to {csv_path}")
