import networkx as nx
from utils import powerset
from disjoint_fvs_problem import DisjointFVSProblem

class FVSCompressionProblem:
    def __init__(self, graph, X, k):
        self.graph = graph
        self.Z = X
        self.k = k
        self.admissible_instance = True

    def solve(self):
        """
        Solve the Feedback Vertex Set Compression problem.

        Parameters:
        G (nx.Graph): A graph.
        Z (list): A subset of nodes of G1.
        k (int): Is the cardinality of FVS looked for.

        Returns:
        list: In case of yes-instance, a of vertices that are
        FVS of G of cardinality k. Otherwise, an empty list.
        """
        if len([v for v in list(self.graph.nodes) if v not in self.Z]) and  not nx.is_forest(self.graph.subgraph([v for v in list(self.graph.nodes) if v not in self.Z])):
            return []
        elif len(self.Z) != self.k + 1:
            return[]
        else:
            for X_Z in powerset(self.Z):
                if len(X_Z) == len(self.Z):
                    continue
                else:
                    W = [v for v in self.Z if v not in X_Z]
                    subproblem = DisjointFVSProblem(self.graph.subgraph([v for v in list(self.graph.nodes) if v not in X_Z]), W,[], len(W) - 1)
                    output = subproblem.solve()

                    if not output.admissible_instance:
                        continue
                    else:
                        return X_Z + output.X
        return []