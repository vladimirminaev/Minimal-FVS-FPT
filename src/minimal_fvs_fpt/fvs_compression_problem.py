import networkx as nx
from .utils import get_list_of_proper_subsets
from .disjoint_fvs_problem import DisjointFVSProblem


class FVSCompressionProblem:
    """Solves the FVS Compression problem, a key step in FPT algorithms for FVS.

    Given a graph G and a known feedback vertex set (FVS) `Z` of size `k+1`,
    this class attempts to "compress" it to find a smaller FVS of size `k`.
    This is a core component of the fixed-parameter tractable algorithm for the
    Minimum Feedback Vertex Set problem.

    The algorithm works by iterating through all proper subsets of `Z`. For each
    subset, it formulates a `DisjointFVSProblem` to determine if a valid FVS
    of the required smaller size can be constructed.

    Attributes:
        graph (nx.Graph): The input graph.
        Z (list): A known feedback vertex set of size `k+1`.
        k (int): The target size for the new, smaller FVS (which is `len(Z) - 1`).
        X (list): The found FVS of size `k`, if one exists.
        admissible_instance (bool): Becomes `True` if a solution (an FVS of size `k`)
            is successfully found.

    Example:
        >>> import networkx as nx
        >>> from minimal_fvs_fpt.disjoint_fvs_problem import FVSCompressionProblem
        >>> # A 4-cycle graph where any single node is a minimal FVS.
        >>> G = nx.cycle_graph(4)
        >>> # Z is a valid FVS of size 2. We want to see if we can find one of size 1.
        >>> Z = [0, 2]
        >>> problem = FVSCompressionProblem(graph=G, Z=Z)
        >>> problem.solve()
        >>> print(f"Solution found: {problem.admissible_instance}")
        Solution found: True
        >>> # The found FVS should have size 1.
        >>> print(f"Found FVS of size {len(problem.X)}: {problem.X}")
        Found FVS of size 1: [0]
    """

    def __init__(self, graph, Z):
        """Initializes an instance of the FVSCompressionProblem.

        Args:
            graph (nx.Graph): The input graph.
            Z (list): A known FVS of the graph, which the algorithm will
                attempt to compress. Its size is expected to be `k+1`.
        """
        self.graph = graph
        self.Z = Z
        self.k = len(Z) - 1
        self.admissible_instance = False
        self.X = []

    def solve(self):
        """Executes the FVS compression algorithm.

        This method attempts to find an FVS of size `k` by leveraging the known
        FVS `Z` of size `k+1`. It first validates two preconditions:
        1. `Z` must be a valid feedback vertex set for the graph.
        2. The size of `Z` must be exactly `k+1`.

        If these conditions are met, it iterates through all proper subsets of `Z`.
        For each subset `X_Z`, it defines and solves a `DisjointFVSProblem` on
        the remaining graph parts to see if a valid disjoint FVS can complete
        the solution.

        If a solution is found in any iteration, `self.X` is updated with the
        new FVS of size `k`, `self.admissible_instance` is set to `True`, and
        the method terminates.

        The results are stored in the instance attributes `self.X` and `self.admissible_instance`.
        """
        # Z must be a FVS
        if len(
            [v for v in list(self.graph.nodes) if v not in self.Z]
        ) and not nx.is_forest(
            self.graph.subgraph([v for v in list(self.graph.nodes) if v not in self.Z])
        ):
            self.admissible_instance = False

        # Z must have cardinality k + 1
        elif len(self.Z) != self.k + 1:
            self.admissible_instance = False

        else:
            for X_Z in get_list_of_proper_subsets(self.Z):

                W = [v for v in self.Z if v not in X_Z]

                subproblem = DisjointFVSProblem(
                    graph=self.graph.subgraph(
                        [v for v in list(self.graph.nodes) if v not in X_Z]
                    ),
                    W=W,
                    k=len(W) - 1,
                )
                subproblem.solve()

                if subproblem.admissible_instance:
                    self.X = X_Z + subproblem.X
                    self.admissible_instance = True
                    break
