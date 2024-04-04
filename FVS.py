def fvs(G, k, plot_solution = False):
    nodes = list(G.nodes)
    
    X = nodes[0:k]
    
    for i in range(k + 1, len(nodes)):
        print()
        #print('i = ', i)
        #print('X = ', X)
        #print(X + [nodes[i]])
        new_G =  G.subgraph(nodes[0:i + 1])
        new_X = fvs_c(new_G, X + [nodes[i]], k, plot_solution)
        #print('new_X = ', new_X)
        #nx.draw_networkx(new_G, with_labels=True)
        #plt.show()
        
        if len(new_X) == 0 and nx.is_forest(new_G) == False:
            
            
            #print('There is no FVS of size ', k, 'in the given graph')
            
            
            #nx.draw_networkx(new_G, with_labels=True)
            #plt.show()
            return []
        elif len(new_X) != 0:
            #print('i = ', i)
            #print('X = ', X, '; X_new = ', new_X)
            
            if len(new_X) < k:
                X = new_X + [v for v in X if v not in new_X][0:k - len(new_X)]
            else:
                X = new_X
                
    #print(X, ' is a FVS of size ', k)
    
    return X