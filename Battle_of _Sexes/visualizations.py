# visualizations.py
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import ConnectionPatch

def draw_game_tree():
    """Draws the game tree for the Battle of the Sexes with a dashed curved line."""
    G = nx.DiGraph()
    G.add_edge("Man", "woman1", label="Ballet")
    G.add_edge("Man", "woman2", label="Fight")
    G.add_edge("woman1", "(1,2)", label="Ballet")
    G.add_edge("woman1", "(0,0)_1", label="Fight")
    G.add_edge("woman2", "(0,0)_2", label="Ballet")
    G.add_edge("woman2", "(2,1)", label="Fight")
    pos = {
        "Man": (0, 1),
        "woman1": (-1, 0),
        "woman2": (1, 0),
        "(1,2)": (-2, -1),
        "(0,0)_1": (-0.5, -1),
        "(0,0)_2": (0.5, -1),
        "(2,1)": (2, -1)
    }
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1500, 
            font_size=10, font_weight="bold", arrows=True)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    xyA = pos["woman1"]
    xyB = pos["woman2"]
    con = ConnectionPatch(
        xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
        connectionstyle="arc3,rad=0.3", linestyle="--", color="black", linewidth=1.5
    )
    plt.gca().add_artist(con)
    plt.savefig('tree_plot.png', bbox_inches='tight', dpi=1200)
    plt.close()

def draw_normal_form_game():
    """Draws the normal form payoff table for the Battle of the Sexes."""
    data = [["(1,2)", "(0,0)"], ["(0,0)", "(2,1)"]]
    row_labels = ["Ballet", "Fight"]
    col_labels = ["Ballet", "Fight"]
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    table = ax.table(cellText=data, rowLabels=row_labels, colLabels=col_labels,
                     loc='center', cellLoc='center', edges='closed')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    for (row, col), cell in table.get_celld().items():
        cell.set_text_props(weight='bold')
        if row == 0 or col == -1:
            cell.set_facecolor('#d3d3d3')
        else:
            cell.set_facecolor('#ffffff')
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)
    fig.text(0.5, 0.65, "Man", fontsize=14, fontweight='bold', ha='center')
    fig.text(-0.1, 0.5, "Woman", fontsize=14, fontweight='bold', ha='center')
    plt.tight_layout(pad=2.0)
    plt.savefig('payoff_table.png', bbox_inches='tight', dpi=1200)
    plt.close()