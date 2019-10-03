import numpy as np
import random
import os
import networkx as nx
import time
import sys
import statistics

from environ import RountingEnv # The routing environment
from collections import defaultdict # memory efficient storing of value functions
from network_generator import prsnt, random_dag

import csv

def mc_prediction(policy, env,G, Final_deadline, num_episodes, discount_factor=1, alpha=1, epsilon=0.1):
    """
    Monte Carlo prediction algorithm. Calculates the value function
    for a given policy using sampling.

    Args:
        policy: A function that maps an observation to action probabilities.
        env:Routing environment.
        num_episodes: Number of episodes to sample.
        discount_factor: Gamma discount factor.

    Returns:
        A dictionary that maps from state -> value.
        The state is a tuple and the value is a float.
    """
    # Keeps track of time and count of returns for each state
    returns_time = defaultdict(float)
    returns_count = defaultdict(float)
    Q = defaultdict(lambda: defaultdict(float))
    for node in G.nodes():
        for edge in G.successors(node):
            Q[node][edge] = 0.0    # The final value function

    eps_time = np.empty(num_episodes+1)
    total_time = np.empty(num_episodes+1)
    node_num = 5
    for i_episode in range(1, num_episodes + 1):
        start_time = time.time() # Time keeping
        time_offset = 0
        episode = [] # An episode is an array of (state, action, reward) tuples
        total_time[i_episode] = 0
        state = env.reset(Final_deadline)
        for t in range(100):
            deadline = env.get_deadline()
            action, time_traversed = policy(Q, G, epsilon, state, deadline)
            total_time[i_episode] += time_traversed
            if ([action, time_traversed] == [None,0]):
                break
            next_state, reward, done, _ = env.step(action, time_traversed)
            if(not(Q[next_state])):
                td_target = reward
            else:
                best_next_action = max(Q[next_state],key=Q[next_state].get)
                td_target = reward + discount_factor * Q[next_state][best_next_action]
            td_delta = td_target - Q[state][action]
            Q[state][action] += alpha * td_delta
            if done:
                eps_time[i_episode] = time.time() - start_time
                break
            state = next_state
        """
        row = []
        filename = os.environ['resultsfile'] ## Write a result file after each episode
        w = csv.writer(open(filename, "a+"))
        for key, val in Q.items():
            row = [i_episode, key]
            for v in range(len(val)):
                row.append(val[v])
            w.writerow(row)

        row = []
        bestpathfile = os.environ['bestpathfile'] ## Write the best path for each episode
        w = csv.writer(open(bestpathfile, "a+"))
        row = [i_episode, G.nodes[0]['name']]
        for state,action in Q.items():
            next_node = G.nodes[np.argmax(action)]['index']
            row.append(G.nodes[int(next_node)]['name'])
            if(next_node == G.nodes[G.number_of_nodes() - 1]['index'] ): # If it is the final node
                break
        w.writerow(row)
    """
    row  = []
    row = [statistics.mean(total_time), Final_deadline]
    tx_time_file = "multinode_tx_times.csv" ## Write the time traveresed for each episode
    w = csv.writer(open(tx_time_file, "a+"))
    w.writerow(row)

    return Q, policy

def make_epsilon_greedy_policy(Q, G, epsilon, observation, deadline):
    """
    Creates an epsilon-greedy policy based on a given Q-function and epsilon.
    Args:
        Q: A dictionary that maps from state -> action-values.
            Each value is a numpy array of length nA (see below)
        epsilon: The probability to select a random action . float between 0 and 1.
        nA: Number of actions in the environment.
    Returns:
        A function that takes the observation as an argument and returns
        the probabilities for each action in the form of a numpy array of length nA.
    """
    current_node = observation
    time_traversed = 0
    next_node = 0
    feasible_edges = []

    for i in G[int(current_node)]:
        if G[int(current_node)][i]['wct'] <= deadline:
            feasible_edges.append(i)

    if(feasible_edges == []): # Are there no feasible edges
        return(0,0)

    if(current_node == G.nodes[G.number_of_nodes() - 1]['index']): # Exit if its the last node already
        return(0,0)

    probs = [] # probabilities assignment

    unique_nodes = []
    new_probs = epsilon / len(feasible_edges) # Divide by number of edges
    empty_Q_feasible = False
    for edge in feasible_edges:
        if(Q[current_node][edge]): # If Q value exists
            if(Q[current_node][edge] == 0.0):
                empty_Q_feasible = True
    probs = np.full(len(feasible_edges), new_probs)

    if(empty_Q_feasible):
        best_action = np.argmax(probs)
    elif(Q[current_node] == {}): ## we have no values on Q function
        best_action = np.argmax(probs)
    else:
        best_action = np.argmax(Q[current_node]) # Non feasible paths become 0

    probs[best_action] += (1.0 - epsilon) # Add (1-epsilon) to the best action prob
    next_edge = feasible_edges[np.random.choice(np.arange(len(probs)), p=probs)]
    time_traversed = G[int(current_node)][int(next_edge)]["tx"]
    next_node = next_edge

    return(next_node, time_traversed)


#deadline = int(os.environ['deadline'])
num_episodes = int(os.environ['num_episodes'])

for num_nodes in range(5,500):
    nodes = num_nodes
    edges = 50 * nodes
    G = random_dag(nodes,edges)
    deadline =  2 * nx.dijkstra_path_length(G,0,G.number_of_nodes()-1,weight='wc')

    print(num_nodes," node network with deadline ",deadline," with epsiodes", num_episodes)
    start_time = time.time()
    best_path = [G.node[0]['index']]
    env = RountingEnv(G, deadline)
    Q, policy = mc_prediction(make_epsilon_greedy_policy, env, G, deadline, num_episodes)
    for state,action in Q.items():
        next_node = max(Q[state],key=Q[state].get)
        best_path.append(next_node)
        if(next_node == G.number_of_nodes() - 1): # If it is the final node
            break

    row = []
    comp_time = time.time() - start_time
    row = [nodes, comp_time, len(best_path)]
    file = "multinode.csv"
    w = csv.writer(open(file, "a+"))
    w.writerow(row)
