import networkx as nx

class DisjointFVSProblem:
    def __init__(self, graph, W, X, k):
        # Create a mutable copy of the graph if it's frozen
        if nx.is_frozen(graph):
            self.graph = nx.Graph(graph)
        else:
            self.graph = graph
        self.W = W
        self.X = X
        self.k = k
        self.admissible_instance = True

    def reduction_1(self):
        """
        Delete all the vertices of degree at most 1
        """
        # Create a list of nodes to remove to avoid modification during iteration
        nodes_to_remove = [node for node in self.graph.nodes if self.graph.degree(node) <= 1]
        self.graph.remove_nodes_from(nodes_to_remove)

        return self

    def reduction_2(self):
        """
        Delete all the vertices from vertices of G1=(V,E) that
        are not in V\W, which form a cycle with W.
        """
        H = [v for v in list(self.graph.nodes) if v not in self.W]
        nodes_to_remove = []
        
        for v in H:
            if not nx.is_forest(self.graph.subgraph(self.W + [v])):
                self.X.append(v)
                nodes_to_remove.append(v)
                self.k -= 1
        
        self.graph.remove_nodes_from(nodes_to_remove)

        return self

    def reduction_3(self):
        """
        Delete all the vertices of G1=(V,E) that are in V\W,
        are of degree 2 and have at least one neighbor in V\W
        """
        H = [v for v in list(self.graph.nodes) if v not in self.W]
        nodes_to_remove = []
        edges_to_add = []

        for v in H:
            if self.graph.degree(v) == 2 and len(list(self.graph.subgraph(H).neighbors(v))) != 0:
                neighbors = list(self.graph.neighbors(v))
                edges_to_add.append((neighbors[0], neighbors[1]))
                nodes_to_remove.append(v)
        
        self.graph.add_edges_from(edges_to_add)
        self.graph.remove_nodes_from(nodes_to_remove)

        return self

    def reductions(self):
        """
        Apply all the reductions.
        """
        H = [v for v in list(self.graph.nodes) if v not in self.W]
        
        if (len(H) > 0 and not nx.is_forest(self.graph.subgraph(H))):
            self.admissible_instance = False
            return self

        elif not nx.is_forest(self.graph.subgraph(self.W)):
            self.admissible_instance = False
            return self
        
        while True:
            old_graph = self.graph.copy()
            self.reduction_1()
            self.reduction_2()
            self.reduction_3()
            
            if nx.is_isomorphic(self.graph, old_graph):
                break
                
        return self

    def solve(self):
        """
        Solve the Disjoint Feedback Vertex Set problem.

        Parameters:
        G1 (nx.Graph): A graph.
        W1 (list): A subset of nodes of G1.
        X1 (list): Is the potential FVS.
        k1 (int): Is the cardinality of FVS looked for.

        Returns:
        list: In case of yes-instance, a graph with vertices from vertices of G1=(V,E) that
        are not in V\W, which form a cycle with W, deleted; updated
        FVS X and updated parameter k. Otherwise, an empty list.
        """
        self.reductions()

        if not self.admissible_instance:
            return self

        else:
            H = [v for v in list(self.graph.nodes) if v not in self.W]

            if self.k < 0:
                self.admissible_instance = False

                return self
            elif len(list(self.graph.nodes)) == 0 or len(list(self.graph.edges)) == 0 :
                return self
            else:
                for node in H:
                    if self.graph.subgraph(H).degree(node) <= 1:
                        new_G = self.graph.copy()
                        new_G.remove_node(node)

                        new_W = self.W.copy()
                        new_W.append(node)

                        new_X = self.X.copy()
                        new_X.append(node)
                        subproblem = DisjointFVSProblem(self.graph, new_W, self.X, self.k)
                        subproblem.solve()

                        if subproblem.admissible_instance:
                            return subproblem
                        else:
                            subproblem = DisjointFVSProblem(new_G, self.W, new_X, self.k - 1)
                            subproblem.solve()

                            if not subproblem.admissible_instance:
                                self.admissible_instance = False

                            return subproblem

        return self