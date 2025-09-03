import unittest
import networkx as nx
from minimal_fvs_fpt.compression import solve_fvs_compression


class TestFVSCompressionProblem(unittest.TestCase):
    def test_compression(self):

        G = nx.Graph()
        G.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)])
        Z = [1, 4]
        k = len(Z) - 1

        X = solve_fvs_compression(G, Z)

        self.assertIsNotNone(X)

        remaining_graph = G.copy()
        remaining_graph.remove_nodes_from(X)
        self.assertTrue(
            len(remaining_graph.nodes) == 0 or nx.is_forest(remaining_graph)
        )

        self.assertLessEqual(len(X), k)
