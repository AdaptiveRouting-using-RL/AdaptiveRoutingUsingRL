## RTSS 2019 submission titled "Adaptive Routing with Guaranteed Delay Bounds using Safe Reinforcement Learning"


### Pre-requisities
- Python version 3.7.0

#### Required python packages
##### Gym
Gym is a toolkit for developing and comparing reinforcement learning algorithms. It supports teaching agents everything from walking to playing games like Pong or Pinball. Our project uses gym for optimal memory usage and and state space construction.

Install using the command
`pip3 install gym`

##### NetworkX
NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks. Our project uses NetworkX to generate and manipulate networks.

Install using the command
`pip3 install networkx`

### Instructions
- Make sure the prerequisite packages mentioned above are installed correctly.
- Run script **runall.sh** in the folder Code to run all the experiments described in the paper.

### Code folder structure
- **Src.** Contains all the python files
- **Scripts.** Bash scripts for running python files
- **Results.** Generated CSV results are stored here
- **Plots.** Latex files for generating Plots
- **pdfs.** Generated plots are stored here