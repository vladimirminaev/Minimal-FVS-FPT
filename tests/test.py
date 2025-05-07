import unittest
import networkx as nx
from minimal_fvs_problem import MinimalFVSProblem

class TestMinimalFVSProblem(unittest.TestCase):
    def test_solve(self):
        G = nx.Graph()
        G.add_edge(1, 2)
        G.add_edge(2, 3)
        G.add_edge(1, 3)
        G.add_edge(3, 4)
        G.add_edge(4, 1)

        minimimal_fvs = MinimalFVSProblem(G).solve()

        self.assertEqual(minimimal_fvs, [1])
