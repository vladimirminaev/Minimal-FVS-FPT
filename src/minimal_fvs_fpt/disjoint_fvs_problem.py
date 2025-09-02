import networkx as nx


class DisjointFVSProblem:
    """Solves the Disjoint Feedback Vertex Set problem.

    This class is designed to find a feedback vertex set (FVS) `X` of size at
    most `k` that is disjoint from a given known FVS `W`. The problem is solved
    using a fixed-parameter tractable (FPT) approach, which involves a series
    of reduction rules to simplify the graph instance, followed by a recursive
    branching strategy.

    An instance is considered admissible only if the initial set `W` is indeed
    a valid feedback vertex set for the graph.

    Attributes:
        graph (nx.Graph): The graph instance being processed. It is modified
            by the reduction rules.
        W (list): A known feedback vertex set of the graph. The goal is to find
            another FVS that is disjoint from this set and has a lesser cardinality.
        X (list): The set of vertices in the disjoint FVS being constructed.
        k (int): The remaining budget for the size of the FVS `X`.
        admissible_instance (bool): A flag that is True if the current
            subproblem might still lead to a valid solution, and False otherwise.

    Examples:
        >>> G = nx.Graph()
        >>> G.add_edges_from([(1, 2), (2, 3), (3, 1), (3, 4)])
        >>> W = [1, 2]
        >>> k = 1
        >>> problem = DisjointFVSProblem(G, W, k)
        >>> problem.solve()
        >>> problem.X
        [3]
    """

    def __init__(self, graph, W, k, X=[]):
        """Initializes the DisjointFVSProblem instance.

        Args:
            graph (nx.Graph): The input graph for the problem.
            W (list): A known feedback vertex set of the graph.
            k (int): The budget for the cardinality of the new FVS.
            X (list): The set of vertices that must be in the disjoint FVS.
        """

        self.graph = nx.MultiGraph(graph)
        self.W = W
        self.X = X
        self.k = k
        self.admissible_instance = True

    def copy(self):
        """Creates a deep copy of the DisjointFVSProblem instance.

        Returns:
            DisjointFVSProblem: A new instance of the problem with identical attributes.
        """
        new_problem = DisjointFVSProblem(
            graph=self.graph.copy(), W=self.W.copy(), k=self.k, X=self.X.copy()
        )
        new_problem.admissible_instance = self.admissible_instance

        return new_problem

    def reduction_1(self):
        """Reduction Rule 1: Removes all vertices of degree at most 1.

        Vertices with a degree of 0 or 1 cannot be part of any cycle.
        Therefore, they can be safely removed from the graph without affecting
        the feedback vertex set problem. The graph is modified in-place.
        """
        nodes_to_remove = [
            node for node in self.graph.nodes if self.graph.degree(node) <= 1
        ]
        self.graph.remove_nodes_from(nodes_to_remove)

    def reduction_2(self):
        """Reduction Rule 2: Identifies necessary vertices for the disjoint FVS.

        This rule iterates through vertices `v` that are not in the known FVS `W`.
        If adding `v` to the subgraph induced by `W` creates a cycle, it implies
        that `v` must be part of any FVS that is disjoint from `W`. Consequently,
        `v` is added to the solution set `X`, removed from the graph, and the
        budget `k` is decremented. The graph is modified in-place.
        """
        H = [v for v in list(self.graph.nodes) if v not in self.W]

        for v in H:
            if not nx.is_forest(self.graph.subgraph(self.W + [v])):
                self.X.append(v)
                self.graph.remove_node(v)
                self.k -= 1

    def reduction_3(self):
        """Reduction Rule 3: Bypasses vertices of degree 2.

        This rule simplifies the graph by handling vertices `v` (not in `W`) that
        have a degree of 2 and at least one neighbor also not in `W`. Such a vertex
        `v` acts as a simple bridge. The rule removes `v` and adds a direct edge
        between its neighbors, preserving the essential cycle structure while reducing
        the graph's size. The graph is modified in-place.
        """
        H = [v for v in list(self.graph.nodes) if v not in self.W]

        for v in H:
            if (
                self.graph.degree(v) == 2
                and len(list(self.graph.subgraph(H).neighbors(v))) != 0
            ):
                self.graph.add_edge(
                    list(self.graph.neighbors(v))[0], list(self.graph.neighbors(v))[1]
                )
                self.graph.remove_node(v)

    def apply_reductions(self):
        """Applies the reduction rules repeatedly until the graph is fully reduced.

        This method exhaustively applies `reduction_1`, `reduction_2`, and
        `reduction_3` in a loop. The process continues until an entire pass
        through the reduction rules results in no change to the graph's
        structure. This ensures the graph is simplified as much as possible
        before the algorithm proceeds to the branching step.
        """

        while True:
            initial_graph = self.graph.copy()

            self.reduction_1()
            self.reduction_2()
            self.reduction_3()

            if nx.is_isomorphic(self.graph, initial_graph):
                break

    def solve(self):
        """Solves the Disjoint Feedback Vertex Set problem recursively.

        The method first checks for the admissibility of the instance, ensuring that
        the provided set `W` is a valid FVS. It then applies the reduction rules
        to simplify the problem. If the instance is still admissible and not fully
        solved, it enters a branching phase. It selects a vertex and recursively
        explores two possibilities: one where the vertex is added to the solution
        set `X`, and another where it is added to the forbidden set `W`.

        The state of the current instance (`self.X`, `self.admissible_instance`)
        is updated based on the outcome of the recursive calls.
        """

        # List of vertices not in W
        H = [v for v in list(self.graph.nodes) if v not in self.W]

        # If W was not a FVS, the given instance is not admissible
        if len(H) > 0 and not nx.is_forest(self.graph.subgraph(H)):
            self.admissible_instance = False

        # If the subgraph induced by W is not a forest, the instance is not admissible,
        # as there is no FVS disjoint from W
        elif not nx.is_forest(self.graph.subgraph(self.W)):
            self.admissible_instance = False

        else:
            reduced_dfvs_problem_instance = self.copy()

            # Apply reductions exhaustively
            reduced_dfvs_problem_instance.apply_reductions()

            H = [
                v
                for v in list(reduced_dfvs_problem_instance.graph.nodes)
                if v not in reduced_dfvs_problem_instance.W
            ]

            # If after applying reductions there are already more vertices,
            # that must be in X, then the budget allows, then the given instance
            # is not admissible
            if reduced_dfvs_problem_instance.k < 0:
                self.admissible_instance = False

            # If the graph has been reduced to a trivial graph, return all the parameters of the instance
            elif (
                len(list(reduced_dfvs_problem_instance.graph.nodes)) == 0
                or len(list(reduced_dfvs_problem_instance.graph.edges)) == 0
            ):
                self.X = reduced_dfvs_problem_instance.X

            # Otherwise we iterate over the vertices not in W with degree at most 1 and branch on them
            else:
                nodes_to_branch_on = [
                    node
                    for node, degree in reduced_dfvs_problem_instance.graph.subgraph(
                        H
                    ).degree()
                    if degree <= 1
                ]

                for node in nodes_to_branch_on:

                    # We either not include the node into the FVS by putting it into W
                    new_W = reduced_dfvs_problem_instance.W.copy()
                    new_W.append(node)

                    # Or we include it into FVS
                    new_G = reduced_dfvs_problem_instance.graph.copy()
                    new_G.remove_node(node)
                    new_X = reduced_dfvs_problem_instance.X.copy()
                    new_X.append(node)

                    # Branch 1: the node is not chosen for FVS
                    subproblem = DisjointFVSProblem(
                        reduced_dfvs_problem_instance.graph,
                        new_W,
                        reduced_dfvs_problem_instance.k,
                        reduced_dfvs_problem_instance.X,
                    )
                    subproblem.solve()

                    if subproblem.admissible_instance:
                        self.X = subproblem.X

                    # Branch 2: the node is chosen for FVS
                    else:
                        subproblem = DisjointFVSProblem(
                            new_G,
                            reduced_dfvs_problem_instance.W,
                            reduced_dfvs_problem_instance.k - 1,
                            new_X,
                        )
                        subproblem.solve()

                        if not subproblem.admissible_instance:
                            self.admissible_instance = False
                        else:
                            self.X = subproblem.X
