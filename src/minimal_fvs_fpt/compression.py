import networkx as nx
from .utils import get_list_of_proper_subsets
from .disjoint_fvs_problem import DisjointFVSProblem


def solve_fvs_compression(graph, Z):
    """Compresses a Feedback Vertex Set (FVS) to a smaller one if possible.

    This function implements the "compression" step of an FPT algorithm for the
    FVS problem. Given a graph and a known FVS `Z` of size `k+1`, it attempts
    to find a new FVS `X` of size `k`.

    The core idea is to guess which vertices from `Z` are also in the smaller
    solution `X`. It iterates through all proper subsets `X_Z` of `Z`. For each
    guess, it formulates a `DisjointFVSProblem` to find the remaining vertices
    of the FVS in the rest of the graph, disjointly from `Z`.

    If a solution is found for any subset, it constructs the new FVS of size `k`
    and returns it immediately. If, after trying all proper subsets, no smaller
    FVS can be found, the function returns `None`.

    Args:
        graph (nx.Graph): The input graph.
        Z (list): A known feedback vertex set for the graph, with size `k+1`.

    Returns:
        list or None: A list of vertices representing a smaller FVS of size `k`
                      if one is found; otherwise, `None`.
    """
    X = []
    k = len(Z) - 1

    # Z must be a FVS
    if len([v for v in list(graph.nodes) if v not in Z]) and not nx.is_forest(
        graph.subgraph([v for v in list(graph.nodes) if v not in Z])
    ):
        X = None

    else:
        for X_Z in get_list_of_proper_subsets(Z):

            W = [v for v in Z if v not in X_Z]

            subproblem = DisjointFVSProblem(
                graph=graph.subgraph([v for v in list(graph.nodes) if v not in X_Z]),
                W=W,
                k=len(W) - 1,
            )
            subproblem.solve()

            if subproblem.admissible_instance:
                X = X_Z + subproblem.X
                break
        else:
            X = None

    return X
