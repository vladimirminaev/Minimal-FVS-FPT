def is_subset(list_a, list_b):
    return all(element in list_b for element in list_a)

def powerset(iterable):
    s = list(iterable)
    return [list(item) for item in chain.from_iterable(combinations(s, r) for r in range(len(s)+1))]

def fvs_c(G, Z, k, plot_solution = False):
    
    if len([v for v in list(G.nodes) if v not in Z]) and nx.is_forest(G.subgraph([v for v in list(G.nodes) if v not in Z])) == False:
        #print('Z is not a FVS')  
        return []
    elif len(Z) != k + 1:
        #print('The cardinality of Z is wrong')
        return[]
    else:
        for X_Z in powerset(Z):
            if len(X_Z) == len(Z):
                continue
            else:
                #print('X_Z = ', X_Z)
                W = [v for v in Z if v not in X_Z]
                #print('Applying DFVS to ', [G.subgraph([v for v in list(G.nodes) if v not in X_Z]).nodes, W, [], len(W) - 1])
                output = dfvs(G.subgraph([v for v in list(G.nodes) if v not in X_Z]), W, [], len(W) - 1, plot_solution)
                
                if len(output) == 0:
                    #print('There is no FVS of size ', k, 'containing only ', X_Z, ' from ', Z)
                    continue
                else:
                    #print('The compressed FVS is found')
                    return X_Z + output[2]
            
    #print('Compression is not possible')
    
    return []    