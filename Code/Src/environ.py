import gym
from gym import spaces
import networkx as nx

#Final_deadline = 20

class RountingEnv():
    """
    Action space is the possible destinations from the node.
    Observation is the current node name, amount of time saved, deadline
    """
    def __init__(self, G, Final_deadline):
        self.action_space = spaces.Discrete(G.number_of_nodes()) # Action space is edges available while sticking to the deadline
        self.current_node = G.node[0]
        self.next_node = []
        self.total_time = 0
        self.Final_deadline = Final_deadline
        self.deadline = 0
        self.G = G
        self._reset(Final_deadline)

    def reset(self, Final_deadline):
        return self._reset(Final_deadline)

    def step(self, action, time_traversed):
        return self._step(action, time_traversed)

    def _step(self, action, time_traversed):
        """
        Main fucntion that does the step action.
        Returns: Action: This was the node that was decided to be taken during the sampling
               : Reward: The amount of time saved while traversing
               : done: This is true if the action/next_node is equal to the destination node. Remember that this is the last entry in the table of nodes
        """
        done = False
        if(action == int(self.G.nodes[self.G.number_of_nodes() - 1]['index'])):
            done = True
            next_node = self._get_obs() # Stay in the same node as it is the final node
            self.total_time += time_traversed
            reward = self.Final_deadline - self.total_time # Reward assignment as the episode is completed
        else: # the action taken becomes the next node
            next_node = action
            reward = 0
            self.deadline = self.deadline - time_traversed # new deadline is old deadline - time_traversed. This is the same as reward for now
            self.total_time += time_traversed
            self.current_node = action
        return action, reward, done, {}

    def get_deadline(self): # returns the current deadline
        return (self.deadline)

    def _get_obs(self):
        return(int(self.G.nodes[self.current_node]['index']))

    def _reset(self,Final_deadline):# Should reset the environment. Builds the table for all nodes.
        self.current_node = 0
        self.total_time = 0
        self.deadline = Final_deadline # set deadline to final deadline
        return self._get_obs()
