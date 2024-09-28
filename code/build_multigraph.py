import networkx as nx

# Read the graphs
G1 = nx.read_gexf("graph_dimension1_to_share.gexf")
G2 = nx.read_gexf("graph_dimension2_to_share.gexf")
G3 = nx.read_gexf("graph_dimension3_to_share.gexf")

# Print statistics for G3 (as nodes from G1 and G2 are not needed)
print("Dimension 3 Nodes and Edges")
print(G3.number_of_nodes(), G3.number_of_edges())
print("Creators:", sum(1 for _, d in G3.nodes(data=True) if d.get('node') == 'creator'))
print("Members:", sum(1 for _, d in G3.nodes(data=True) if d.get('node') == 'member'))
print("Feeds:", sum(1 for _, d in G3.nodes(data=True) if d.get('node') == 'feed'))

# Create a new multidigraph
G = nx.MultiDiGraph()

# Add nodes from G3 (since G3 is sufficient for node information)
G.add_nodes_from(G3.nodes(data=True))

# Add edges from G1, G2, and G3
for G_source, edge_attr in [(G1, ('sign', 'time')), (G2, ('sign', 'time')), (G3, ('edge', 'time'))]:
    for u, v, d in G_source.edges(data=True):
        edge_data = {attr: d[attr] for attr in edge_attr}
        G.add_edge(u, v, **edge_data)

# Add reverse edges from G3 with the same attributes
for u, v, d in G3.edges(data=True):
    edge_data = {attr: d[attr] for attr in ('edge', 'time')}
    G.add_edge(v, u, **edge_data)

# Output the final graph stats
print("Nodes and Edges")
print(G.number_of_nodes(), G.number_of_edges())
print(next(iter(G.edges(data=True))))

# Save the combined graph
nx.write_gexf(G, "multi_graph_to_share.gexf")
