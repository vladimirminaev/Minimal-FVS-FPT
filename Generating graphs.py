def generating_graphs(n_vertices, k):
    
    G = nx.erdos_renyi_graph(n = n_vertices, p = 0, directed = False)
    
    G1 = G.copy()
    FVS = []
    nodes = list(G.nodes())
    
    while len(FVS) < k: 
        
        random_edge = random.sample(nodes, 2)
        
        if is_subset(random_edge, list(G.edges)) == False:
            G.add_edge(random_edge[0], random_edge[1])
        else:
            continue
   
        if nx.is_forest(G.subgraph([v for v in list(G.nodes) if v not in FVS])) == False:  
            FVS.append(random_edge[0])
        
    return [G, FVS]