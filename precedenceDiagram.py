import networkx as nx
import matplotlib.pyplot as plt

tasks = {
    0: [],
    1: [0],
    2: [0],
    3: [0],
    4: [0],
    5: [1, 2, 3, 4],
    6: [5],
    7: [5],
    8: [6, 7],
    9: [8],
    10: [9],
    11: [10],
    12: [11],
    13: [12],
    14: [0],
    15: [14],
    16: [15],
    17: [16],
    18: [17],
    19: [0],
    20: [18, 19],
    21: [20],
    22: [21],
    23: [21],
    24: [22, 23],
    25: [0],
    26: [24, 25],
    27: [26],
    28: [27],
    29: [28],
    30: [29],
    31: [24],
    32: [31],
    33: [32],
    34: [32],
    35: [33, 34],
    36: [35],
    37: [30, 36],
    38: [37],
    39: [38],
    40: [39],
    41: [40],
    42: [13, 41],
    43: [42],
    44: [42],
    45: [43, 44],
    46: [45],
    47: [46],
    48: [47],
    49: [48],
    50: [49],
    51: [50],
    52: [51],
    53: [50],
    54: [50],
    55: [53, 54],
    56: [55],
    57: [56],
    58: [56],
    59: [56],
    60: [56],
    61: [0],
    62: [57, 58, 59, 60],
    63: [0],
    64: [56, 61, 63],
    65: [52, 64],
    66: [65],
    67: [62],
    68: [67, 69],
    69: [66],
    70: [68],
    71: [70],
    72: [68],
    73: [68],
    74: [68],
    75: [68],
    76: [68],
    77: [68],
    78: [71, 72, 73, 74, 75, 76, 77],
    79: [78],
}

# Create a directed graph
graph = nx.DiGraph()

# Add nodes for each task
for task in tasks:
    graph.add_node(task)

# Add edges for task dependency
for task, dependencies in tasks.items():
    for dependency in dependencies:
        graph.add_edge(dependency, task)

# ----------Untuk melihat visualisasinya----------
# # Set positions for visual layout
# pos = nx.spring_layout(graph)

# # Draw the graph
# nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=10, font_weight='bold', width=1.5)

# # Draw edge labels
# labels = {edge: edge[0] for edge in graph.edges()}
# nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_size=8)

# # Show the graph
# plt.axis('off')
# plt.show()