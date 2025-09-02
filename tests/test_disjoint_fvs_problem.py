import unittest
import networkx as nx
from minimal_fvs_fpt.disjoint_fvs_problem import DisjointFVSProblem


class TestDisjointFVSProblem(unittest.TestCase):
    def test_solve_finds_fvs(self):
        G = nx.Graph()
        G.add_edges_from([(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (2, 3)])
        W = [2, 3]
        k = 2

        problem = DisjointFVSProblem(graph=G, W=W, k=k)
        problem.solve()

        self.assertTrue(problem.admissible_instance)

        remaining_graph = G.copy()
        remaining_graph.remove_nodes_from(problem.X)
        self.assertTrue(
            len(remaining_graph.nodes) == 0 or nx.is_forest(remaining_graph)
        )

        self.assertLessEqual(len(problem.X), k)

    def test_solve_finds_smaller_fvs(self):
        G = nx.Graph()
        G.add_edges_from(
            [(0, 1), (1, 2), (2, 3), (1, 3), (2, 5), (3, 5), (3, 4), (4, 5)]
        )
        W = [2, 5]
        k = 1

        problem = DisjointFVSProblem(graph=G, W=W, k=k)
        problem.solve()

        self.assertTrue(problem.admissible_instance)

        remaining_graph = G.copy()
        remaining_graph.remove_nodes_from(problem.X)
        self.assertTrue(
            len(remaining_graph.nodes) == 0 or nx.is_forest(remaining_graph)
        )

        self.assertLessEqual(len(problem.X), k)
