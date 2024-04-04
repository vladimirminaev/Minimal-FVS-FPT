import networkx as nx
import matplotlib.pyplot as plt
from itertools import chain, combinations
import time
import pandas as pd
import random


def reduction_1(G1, plot_solution = False):
    G = G1.copy()
    for node in list(G.nodes):
        if G.degree(node) <= 1:
            G.remove_node(node)
            if plot_solution == True:
                print('Deleting ', node, ' in reduction 1')
                nx.draw_networkx(G, with_labels=True)
                plt.show()
    return G


def reduction_2(G1, W, X, k, plot_solution = False):
    G = G1.copy()
    H = [v for v in list(G.nodes) if v not in W]
    
    for v in H:
        W_check = W.copy()
        W_check.append(v)
        if nx.is_forest(G.subgraph(W_check)) == False:
            X.append(v)
            G.remove_node(v)
            k -= 1
            if plot_solution == True:
                print('Deleting ', v, ' in reduction 2')
                nx.draw_networkx(G, with_labels=True)
                plt.show()
    return [G, X, k]



def reduction_3(G1, W, X, k, plot_solution = False):
    G = G1.copy()
    H = [v for v in list(G.nodes) if v not in W]
    
    for v in H:
        if G.degree(v) == 2 and len(list(G.subgraph(H).neighbors(v))) != 0:
            G.add_edge(list(G.neighbors(v))[0], list(G.neighbors(v))[1])
            G.remove_node(v)
            if plot_solution == True:
                print('Deleting ', v, ' in reduction 3')
                nx.draw_networkx(G, with_labels=True)
                plt.show()
    return G





def reductions(G1, W, k, plot_solution = False):
    
    X = []
    G = nx.MultiGraph(G1)
    
    if len([v for v in list(G.nodes) if v not in W]) > 0 and nx.is_forest(G.subgraph([v for v in list(G.nodes) if v not in W])) == False:
        #print('W is not a FVS')  
        return []
    elif nx.is_forest(G.subgraph(W)) == False:
        #print("W contains cycles")  
        return []
    else:
        while len(list(G.nodes)) > 0:
            #print('Before red', G.edges)
            g = reduction_1(G, plot_solution)
            g, X, k = reduction_2(g, W, X, k, plot_solution)
            g = reduction_3(g, W, X, k, plot_solution)
            #print('After red', g.edges)
            if nx.is_isomorphic(G, g):
                break
            else: 
                G = g
        return [G, W, X, k]