import networkx as nx
from .fvs_compression_problem import solve_fvs_compression


def find_minimal_fvs(graph):
    """Solves the Minimum Feedback Vertex Set (FVS) problem using an FPT algorithm.

    This function implements a fixed-parameter tractable (FPT) algorithm to find
    the minimum set of vertices whose removal makes the graph acyclic. The
    algorithm is parameterized by the size of the FVS.

    It works by iteratively processing the graph's nodes one by one. For each
    node, it considers the subgraph induced by the nodes processed so far and
    uses the `solve_fvs_compression` function to try to find a smaller FVS,
    effectively "compressing" the solution at each step.

    Args:
        graph (nx.Graph): The input graph for which to find the minimal FVS.

    Returns:
        list: A list of vertices representing the minimal feedback vertex set
              found for the graph.

    Example:
        >>> import networkx as nx
        >>> # Create a graph of two triangles joined at node 3.
        >>> # The minimal FVS for this graph is the single vertex {3}.
        >>> G = nx.Graph([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3)])
        >>> min_fvs = find_minimal_fvs(G)
        >>> print(f"The minimal FVS is: {sorted(min_fvs)}")
        The minimal FVS is: [3]
        >>> # Verify that removing the FVS leaves a forest.
        >>> remaining_nodes = [n for n in G.nodes if n not in min_fvs]
        >>> is_forest = nx.is_forest(G.subgraph(remaining_nodes))
        >>> print(f"Is the remaining graph a forest? {is_forest}")
        Is the remaining graph a forest? True

    Notes:
        - The algorithm processes nodes incrementally, building up a solution.
        - It uses `solve_fvs_compression` as its core subroutine for optimization.
        - The Feedback Vertex Set problem is NP-hard, but this FPT approach
          can be efficient for graphs where the FVS size is small.
    """

    nodes = list(graph.nodes)
    X = []

    for i in range(len(nodes)):
        new_G = graph.subgraph(nodes[0 : i + 1])
        X_compressed = solve_fvs_compression(new_G, X + [nodes[i]])

        if X_compressed is None:
            X = X + [nodes[i]]

        else:
            X = X_compressed

    return X
