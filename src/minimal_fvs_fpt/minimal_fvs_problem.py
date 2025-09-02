import networkx as nx
from .fvs_compression_problem import FVSCompressionProblem


class MinimalFVSProblem:
    """
    A class that solves the Minimal Feedback Vertex Set (FVS) problem using an iterative approach.

    This class implements an algorithm to find the minimum set of vertices that need to be
    removed from a graph to make it acyclic (i.e., break all cycles in the graph). It uses
    an iterative approach by examining subgraphs of increasing size and utilizing the
    FVSCompressionProblem for optimization.

    Attributes
    ----------
    graph : nx.Graph
        The input graph for which to find the minimal feedback vertex set.

    Methods
    -------
    solve()
        Computes and returns the minimal feedback vertex set for the input graph.

    Examples
    --------
    >>> G = nx.cycle_graph(4)  # Create a cycle graph with 4 nodes
    >>> problem = MinimalFVSProblem(G)
    >>> problem.solve()
    >>> print(f"Found FVS of size {len(problem.X)}: {problem.X}")
        Found FVS of size 1: [3]

    Notes
    -----
    - The algorithm processes nodes incrementally, building subgraphs of increasing size
    - Uses FVSCompressionProblem as a subroutine for optimization
    - Time complexity depends on the graph structure and size
    - The Feedback Vertex Set problem is NP-hard for general graphs
    """

    def __init__(self, graph):
        self.graph = graph
        self.X = []

    def solve(self):
        """
        Solve the Minimal Feedback Vertex Set (FVS) problem.

        This method finds a minimum set of vertices whose removal makes the graph acyclic.

        Parameters
        ----------
        G : nx.Graph
            An undirected graph in NetworkX format.

        Returns
        -------
        tuple
            A tuple containing:
            - list: The minimal Feedback Vertex Set (vertices to be removed)
            - list: Running times for each iteration of the algorithm
        """
        nodes = list(self.graph.nodes)
        k = 0

        for i in range(len(nodes)):
            new_G = self.graph.subgraph(nodes[0 : i + 1])
            subproblem = FVSCompressionProblem(new_G, self.X + [nodes[i]])
            subproblem.solve()

            if len(subproblem.X) == 0 and not nx.is_forest(new_G):
                k += 1
                self.X = self.X + [nodes[i]]

            elif len(subproblem.X) != 0:
                self.X = subproblem.X
