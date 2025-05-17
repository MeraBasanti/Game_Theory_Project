import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

class GameTree:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.pos = {}
        self.node_labels = {}
        self.edge_labels = {}
        self.current_y = 0
        self.level_height = 1
        self.node_width = 1
    
    def add_node(self, node_id, label="", level=0, position=None):
        self.graph.add_node(node_id)
        if position:
            x, y = position
        else:
            x = level * self.node_width
            y = self.current_y - level * self.level_height
        self.pos[node_id] = (x, y)
        self.node_labels[node_id] = label
    
    def add_edge(self, from_node, to_node, label=""):
        self.graph.add_edge(from_node, to_node)
        self.edge_labels[(from_node, to_node)] = label
    
    def draw(self, title="Extensive Form Game"):
        plt.figure(figsize=(10, 6))
        nx.draw_networkx_nodes(self.graph, self.pos, node_size=2000, node_color='lightblue')
        nx.draw_networkx_labels(self.graph, self.pos, labels=self.node_labels, font_size=10)
        
        # Draw curved edges with labels
        ax = plt.gca()
        for (u, v), label in self.edge_labels.items():
            arrow = FancyArrowPatch(
                posA=self.pos[u],
                posB=self.pos[v],
                arrowstyle='->',
                connectionstyle='arc3,rad=0.2',
                color='black'
            )
            ax.add_patch(arrow)
            ax.text(
                (self.pos[u][0] + self.pos[v][0]) / 2,
                (self.pos[u][1] + self.pos[v][1]) / 2,
                label,
                horizontalalignment='center',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
            )
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()