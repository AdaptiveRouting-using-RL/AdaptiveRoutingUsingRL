import numpy as np
import random
import os

from environ import RountingEnv # The routing environment
from collections import defaultdict # memory efficient storing of value functions
from network_generator import prsnt
from mc_prediction import mc_prediction

import csv

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

    probs = np.ones(len(feasible_edges), dtype = float) * epsilon / len(feasible_edges) # probabilities assignment
    probs = np.zeros(G.number_of_nodes())

    unique_nodes = []
    new_probs = epsilon / len(feasible_edges) # Divide by number of edges

    for i in feasible_edges:
        probs[feasible_edges] = new_probs
    if(all(np.multiply(Q[current_node],probs) == 0.0)): ## If we have no data on the value function, use a feasible edge
        best_action = np.argmax(probs)
    else:
        best_action = np.argmax(np.multiply(Q[current_node],probs)) # Non feasible paths become 0

    probs[best_action] += (1.0 - epsilon) # Add (1-epsilon) to the best action prob
    next_edge = np.random.choice(np.arange(len(probs)), p=probs)
    variance = int(os.environ['var'])
    time_traversed = int(np.random.uniform(G[int(current_node)][int(next_edge)]["tx"] - variance, G[int(current_node)][int(next_edge)]["tx"] +variance,1))
    time_traversed = max(time_traversed, 0)
    time_traversed = min(time_traversed, G[int(current_node)][int(next_edge)]["wc"])
    next_node = next_edge

    return(next_node, time_traversed)


deadline = int(os.environ['deadline'])
num_episodes = int(os.environ['num_episodes'])
variance = int(os.environ['var'])

print("Network with Uniform distribution. deadline: ",deadline,", variance: ",variance,", epsiodes: ", num_episodes)

G = prsnt()
best_path = [G.node[0]['name']]
env = RountingEnv(G, deadline)
Q, policy = mc_prediction(make_epsilon_greedy_policy, env, G, deadline, num_episodes)
