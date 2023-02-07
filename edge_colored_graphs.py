import random
import networkx as nx
import matplotlib.pyplot as plt


# creates a randomly 2 coloured complete graph on n vertices
def generate_random_two_color_graph(n):
    # create a complete graph with n vertices
    G = nx.complete_graph(n)
    # assign a random color to each edge in the graph
    for u, v in G.edges():
        G[u][v]["color"] = random.choice(["red", "blue"])
        
    return G


# draws a coloured graph with colored edges
def draw_graph(G):
    plt.figure(figsize=(5,5), facecolor="#111111")

    pos = nx.circular_layout(G)
    color_map = [G[u][v]["color"] for u, v in G.edges()]
    labels = {i: i for i in range(n)}

    nx.draw_networkx_nodes(G, pos, node_size=200, node_color="#aaaaaa", edgecolors="#aaaaaa", label="1")
    nx.draw_networkx_edges(G, pos, edge_color=color_map, width=2)
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_color="white")

    plt.axis("off")
    plt.show()


def find_monochrome_complete_subgraph(G, color, size):
    for v in G.nodes():
        # find all neighbors of v that are connected by an edge of color "color"
        neighbors = [u for u in G.neighbors(v) if G[v][u]["color"] == color and u != v]
        if len(neighbors) >= size - 1:
            # check if the neighbors form a complete subgraph
            subgraph = set([v] + neighbors)
            if len(subgraph) == size and all(G.has_edge(u, w) for u in subgraph for w in subgraph if u != w):
                return True, subgraph
    return False, set()


def find_mono_subgraphs(G, s, t):
    # check if there is a red monochrome subgraph with s vertices
    if find_monochrome_complete_subgraph(G, "red", s)[0]:
        print(f"There is a red monochrome subgraph with {s} vertices")
        print(find_monochrome_complete_subgraph(G, "red", s)[1])
    else:
        print(f"There is no red monochrome subgraph with {s} vertices")

    # check if there is a blue monochrome subgraph with t vertices
    if find_monochrome_complete_subgraph(G, "blue", t):
        print(f"There is a blue monochrome subgraph with {t} vertices")
    else:
        print(f"There is no blue monochrome subgraph with {t} vertices")


if __name__ == "__main__":
    n = 10
    G = generate_random_two_color_graph(n)
    find_mono_subgraphs(G, 7, 3)
    draw_graph(G)