import unittest
import networkx as nx
from minimal_fvs_fpt.minimal_fvs_problem import MinimalFVSProblem


class TestMinimalFVSProblem(unittest.TestCase):
    def test_solve(self):
        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3), (1, 3), (3, 4), (4, 1)])

        minimal_fvs_problem = MinimalFVSProblem(G)
        minimal_fvs_problem.solve()

        self.assertEqual(len(minimal_fvs_problem.X), 1)
        self.assertTrue(
            nx.is_forest(
                G.subgraph(
                    [node for node in G.nodes if node not in minimal_fvs_problem.X]
                )
            )
        )
