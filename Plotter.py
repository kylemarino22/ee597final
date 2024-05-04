import networkx as nx
import matplotlib.pyplot as plt

def plot_snapshot(snapshot, idx, fig, axes, max_bar):
    # Calculate row and column for the subplot based on idx
    num_cols = min(7, len(axes.flatten()))  # Ensures no more than 6 columns
    row = idx // num_cols
    col = idx % num_cols

    # Select the appropriate axes for this snapshot
    ax = axes[row, col]

    # Sort router_labels to ensure alphabetical order
    sorted_labels = sorted(snapshot.keys())

    # Adjust max_length based on max_bar
    max_length = max_bar

    # Creating the bars with different shadings
    for index, router in enumerate(sorted_labels):
        queue = snapshot.get(router, [])  # Get the queue for each router, or an empty list if none
        for start, packet in enumerate(queue):
            color = 'black' if packet == 1 else 'gray'  # Black for '1', gray for '0'
            ax.broken_barh([(index, 1)], (start, 1), facecolors=color)

    # Labeling and styling
    ax.set_xlim(0, len(sorted_labels))
    ax.set_ylim(0, max_length)
    ax.set_xticks(range(len(sorted_labels)))
    ax.set_xticklabels([f'          {r}' for r in sorted_labels])  # Using sorted_labels for x-axis labels
    ax.set_ylabel('Packet Index')
    ax.set_title('Router Queues')
    ax.grid(True)

def plot_snapshots(all_snapshots, max_bar=10):
    num_snapshots = len(all_snapshots)
    num_cols = 7
    num_rows = (num_snapshots + num_cols - 1) // num_cols  # Ceiling division

    # Create a figure with appropriate size
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols * 3, num_rows * 3), squeeze=False)

    for idx, snapshot in enumerate(all_snapshots):
        plot_snapshot(snapshot, idx, fig, axes, max_bar)

    plt.tight_layout()
    plt.show()
    

def plot_network(network, show=True, display_weights=True, filename=None):
   # print router graph
    G = nx.Graph()

    node_colors = []

    for router in network.router_graph:
        G.add_node(router.name)
        
        # Assign a different color if this router is the sink
        if router.sink:
            node_colors.append('red')  # Sink nodes in red
        else:
            node_colors.append('skyblue')  # Other nodes in skyblue

    for router in network.router_graph:
        for dest in router.dests:
            etx_truncated = f"{dest[1]:.2f}"  # Truncate to 2 decimal places
            edge_label = f"ETX: {etx_truncated}, Ticks: {dest[2]}"
            G.add_edge(router.name, dest[0].name, label=edge_label)

    # Position nodes using a layout
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(12, 8))  # Specify the figure size here (width, height)


    # Draw the nodes and edges
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, edge_color='k', font_size=20, font_weight='bold')

    # Draw edge labels using the weights
    if display_weights:
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=18)

    if filename:
        plt.savefig(filename, dpi=300)
        
    if show:
        plt.show() 
   

def plot_network_subplot(ax, network, n, d):
   # print router graph
    G = nx.Graph()

    node_colors = []

    for router in network.router_graph:
        G.add_node(router.name)
        
        # Assign a different color if this router is the sink
        if router.sink:
            node_colors.append('red')  # Sink nodes in red
        else:
            node_colors.append('skyblue')  # Other nodes in skyblue

    for router in network.router_graph:
        for dest in router.dests:
            etx_truncated = f"{dest[1]:.2f}"  # Truncate to 2 decimal places
            edge_label = f"ETX: {etx_truncated}, Ticks: {dest[2]}"
            G.add_edge(router.name, dest[0].name, label=edge_label)

    # Position nodes using a layout
    pos = nx.spring_layout(G)
    
    # plt.figure(figsize=(12, 8))  # Specify the figure size here (width, height)


    # Draw the nodes and edges
    nx.draw(G, pos, ax=ax, with_labels=True, node_color=node_colors, node_size=1000, edge_color='k', font_size=16, font_weight='bold')

    ax.set_title(f"Nodes={n}, Density={d}", size=18)

    # # Draw edge labels using the weights
    # if display_weights:
    #     edge_labels = nx.get_edge_attributes(G, 'label')
    #     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=18)

    # if filename:
    #     plt.savefig(filename, dpi=300)
        
    # if show:
    #     plt.show() 
   

     