import numpy as np
import random
import os
import sys
import time

from environ import RountingEnv # The routing environment
from collections import defaultdict # memory efficient storing of value functions
from network_generator import prsnt

import csv
def mc_prediction(policy, env,G, Final_deadline, num_episodes, discount_factor=0.75, alpha=1, epsilon=0.1):
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
    start_time = time.time()# Keeps track of time and count of returns for each state
    returns_time = defaultdict(float)
    returns_count = defaultdict(float)
    Q = defaultdict(lambda: np.zeros(G.number_of_nodes()))# The final value function
    eps_time = np.empty(num_episodes+1)
    for i_episode in range(1, num_episodes + 1):
        start_time = time.time() # Time keeping
        time_offset = 0
        if i_episode > 40: # ADDS A DYNAMIC CHANGE AFTER 40 EPSIDOES
            time_offset = 6

        # Generate an episode.
        episode = []# An episode is an array of (state, action, reward) tuples
        total_time = 0
        state = env.reset(Final_deadline)
        for t in range(100):
            deadline = env.get_deadline()
            action, time_traversed = policy(Q, G, np.minimum(1,1 * np.exp(-(i_episode/(num_episodes/10)))), state, deadline)

            if(action == int(G.nodes[1]['index'])):
                time_traversed = time_traversed + time_offset

            if ([action, time_traversed] == [None,0]):
                break

            total_time += time_traversed
            next_state, reward, done, _ = env.step(action, time_traversed)
            best_next_action = np.argmax(Q[next_state])
            td_target = reward + discount_factor * Q[next_state][best_next_action]
            td_delta = td_target - Q[state][action]
            Q[state][action] += alpha * td_delta
            episode.append(action)
            if done:
                eps_time[i_episode] = time.time() - start_time
                break
            state = next_state

        row = []
        filename = os.environ['resultsfile'] ## Write a result file after each episode

        w = csv.writer(open(filename+"Q_values.csv", "a+"))
        for key, val in Q.items():
            row = [i_episode, key]
            for v in range(len(val)):
                row.append(val[v])
            w.writerow(row)

        row = []
        w = csv.writer(open(filename+"best_path.csv", "a+"))
        row = [i_episode, G.nodes[0]['name']]
        for state,action in Q.items():
            next_node = G.nodes[np.argmax(action)]['index']
            row.append(G.nodes[int(next_node)]['name'])
            if(next_node == G.nodes[G.number_of_nodes() - 1]['index'] ): # If it is the final node
                break
        w.writerow(row)

        row = []
        w = csv.writer(open(filename+"chosen_path.csv", "a+"))
        row = [i_episode, G.nodes[0]['name']]
        for node in episode:
            row.append(G.nodes[int(node)]['name'])
        w.writerow(row)

        row  = []
        row = [i_episode, total_time]
        w = csv.writer(open(filename+"tx_times.csv", "a+"))
        w.writerow(row)

        np.savetxt(filename+"comp_times.csv", eps_time, delimiter=",")
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
        print("The Schedule is not feasible")
        return(0,0)
    if(current_node == G.nodes[G.number_of_nodes() - 1]['index']): # Exit if its the last node
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
    time_traversed = G[int(current_node)][int(next_edge)]["tx"]
    next_node = next_edge

    if(next_edge not in feasible_edges):
        print("NEXT EDGE NOT IN FEASIBLE")

    return(next_node, time_traversed)


deadline = int(os.environ['deadline'])
num_episodes = int(os.environ['num_episodes'])

print("Dynamic Network with deadline ",deadline," with epsiodes", num_episodes)
G = prsnt()
best_path = [G.node[0]['name']]
env = RountingEnv(G, deadline)
Q, policy = mc_prediction(make_epsilon_greedy_policy, env, G, deadline, num_episodes)
