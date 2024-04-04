def minimal_fvs(G):
    
    nodes = list(G.nodes)
    k = 0
    X = []
    running_times = []
    
    for i in range(len(nodes)):
        start = time.time()
        #print()
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
            
            
            k += 1
            X = X + [nodes[i]]
            
        elif len(new_X) != 0:
            #print('i = ', i)
            #print('X = ', X, '; X_new = ', new_X)
            
            #print("Compressed version found: ", new_X)
            X = new_X
        
        end = time.time()
        
        running_times.append(start-end)
                
    #print(X, ' is a FVS of size ', k)
    
    
    #return X
    
    return [X, running_times]