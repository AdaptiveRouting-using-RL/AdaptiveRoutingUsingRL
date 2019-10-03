import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def paper_network():
    # Create nodes. To keep track of nodes, first one is the
    s = Node('s', [[]], ['t', 'v1'])
    v1 = Node('v1', [[]], ['s', 'v2', 't'])
    v2 = Node('v2', [[]], ['t'])
    t = Node('t', [(None,0)], [])

    # Create edges between the nodes
    ## Node s
    s.create_edge(v1, 4, 10)
    s.create_edge(t, 15, 25)
    ## Node v1
    v1.create_edge(t, 12, 15)
    v1.create_edge(v2, 4, 10)
    ## Node v2
    v2.create_edge(t, 4, 10)
    return s

def prsnt():
    G = nx.DiGraph()

    G.add_node(0, name='i', index='0')
    G.add_node(1, name='x', index='1')
    G.add_node(2, name='y', index='2')
    G.add_node(3, name='z', index='3')
    G.add_node(4, name='t', index='4')

    edges = [(0,1),(0,4),(1,2),(1,3),(1,4),(2,4),(3,4)]

    G.add_edge(0,1,tx=4,wc=10)
    G.add_edge(0,4,tx=12,wc=25)
    G.add_edge(1,2,tx=3,wc=10)
    G.add_edge(1,3,tx=1,wc=15)
    G.add_edge(1,4,tx=10,wc=10)
    G.add_edge(2,4,tx=3,wc=10)
    G.add_edge(3,4,tx=1,wc=15)

    for node in G.nodes():
        for edge in G[node]:
            G[node][edge]["wct"] = G[node][edge]["wc"] + nx.dijkstra_path_length(G,edge,G.number_of_nodes()-1,weight='wc')
    return G

def random_dag(nodes, edges):
    """Generate a random Directed Acyclic Graph (DAG) with a given number of nodes and edges."""
    typ_tx_min = 4
    typ_tx_max = 10

    wc_min = 10
    wc_max = 30

    num_nodes = nodes
    num_edges = edges

    G = nx.DiGraph()

    G.add_node(0, name = 'i', index = '0') ## Create the inital node
    G.add_edge(0,1,tx=4,wc=10) # create edge from init to first node
    G.add_edge(nodes-2,nodes-1,tx=4,wc=10)# create edge from penultimate node to the final node
    G.add_node(nodes-1, name = 't', index = str(nodes-1)) ## Create the destination node

    for i in range(nodes - 1):
        G.add_node(i, index=str(i))

    while edges > 0:
        a = np.random.randint(1,nodes-1)
        b=a
        while b==a:
            b = np.random.randint(1,nodes-1)

        typ_tx = int(np.random.uniform(typ_tx_min, typ_tx_max, 1))
        wc_tx = int(np.random.uniform(wc_min, wc_max, 1))
        G.add_edge(a, b, tx=typ_tx, wc=wc_tx)

        if b > a:
            edges -= 1
        else:
            # we closed a loop!
            G.remove_edge(a,b)

    for i in range(nodes - 2,1,-1): ## check that there exists a path to dest
        if(nx.has_path(G,i,nodes-1) == False):
            typ_tx = int(np.random.uniform(typ_tx_min, typ_tx_max, 1))
            wc_tx = int(np.random.uniform(wc_min, wc_max, 1))
            G.add_edge(i, nodes-1, tx=typ_tx, wc=wc_tx)#Create an edge

    while nx.has_path(G,0,nodes-1) != True: #make sure theres a path from source to destination
        G = random_dag(num_nodes,num_edges)

    for node in G.nodes():
        for edge in G[node]:
            try:
                G[node][edge]["wct"] = G[node][edge]["wc"] + nx.dijkstra_path_length(G,edge,G.number_of_nodes()-1,weight='wc')
            except nx.NetworkXNoPath:
                print("not found")
    return G
