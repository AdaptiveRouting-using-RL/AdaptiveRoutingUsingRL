import sys
import os
import numpy as np
import csv
import time

from environ import RountingEnv # The routing environment
from collections import defaultdict # memory efficient storing of value functions

def mc_prediction(policy, env,G, Final_deadline, num_episodes, discount_factor=1, alpha=0.9, epsilon=0.1):
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
    returns_time = defaultdict(float) # Keeps track of time and count of returns for each state
    returns_count = defaultdict(float)
    Q = defaultdict(lambda: np.zeros(G.number_of_nodes())) # The final value function
    eps_time = np.empty(num_episodes+1)
    for i_episode in range(1, num_episodes + 1):
        start_time = time.time() # Time keeping
        if i_episode > 40: # this will increase the time traversed after episode 40
            time_offset = 0
        episode = []# An episode is an array of (state, action, reward) tuples
        total_time = 0
        state = env.reset(Final_deadline)
        for t in range(100):
            deadline = env.get_deadline()
            action, time_traversed = policy(Q, G, epsilon, state, deadline)
            total_time += time_traversed
            if ([action, time_traversed] == [None,0]):
                break

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
            if(next_node != G.nodes[0]['index']):
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
