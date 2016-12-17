#!/usr/bin/python3
""" convene.py

This is a driver used to simulate multiple agents that have a common 
destination to convene.
"""
import argparse, random
import googlemaps
import agent


def namer():
    """Yield the next integer. Used to generate unique sequential names."""
    n = 0
    while True:
        yield n
        n += 1

def random_line(afile):
    """Return a random line from a text file."""
    with open(afile) as f:
        line = next(f)
        for num, aline in enumerate(f):
          if random.randrange(num + 2): continue
          line = aline
    return line

def random_location():
    """Generate a random location to be used by the agents.  """
    return random_line('addr.txt')

def plan():
    """For each agent in the set of agents, calculate the optimal departure time."""
    print("Plan is not yet implemented")

agents = set()      # The set of all agents in the simulation

if __name__ == '__main__':
    # Set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nagents', type=int)
    args = parser.parse_args()

    # Create new agents and add them to the set of agents
    n = namer()
    while args.nagents:
        agents.add(agent.agent(next(n)))
        args.nagents -= 1

    for agent in agents:
        print('Name: ', agent.name)

    print(random_location())
