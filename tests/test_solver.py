import unittest
import networkx as nx
from minimal_fvs_fpt.solver import find_minimal_fvs


class TestMinimalFVSProblem(unittest.TestCase):
    def test_solve(self):
        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3), (1, 3), (3, 4), (4, 1)])

        X = find_minimal_fvs(G)

        self.assertEqual(len(X), 1)
        self.assertTrue(
            nx.is_forest(G.subgraph([node for node in G.nodes if node not in X]))
        )
