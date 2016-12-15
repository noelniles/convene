#!/usr/bin/python3
""" convene.py

This is a driver used to simulate multiple agents that have a common 
destination to convene.
"""
import googlemaps
import agent


def namer():
    """Yield the next integer. Used to generate unique sequential names."""
    n = 0
    while True:
        yield n
        n += 1

def random_location():
    """Generate a random location to be used by the agents. 
    
    These locations should be relatively close. Also, to make things easier
    none of the random locations should be separated by an impassable barrier.
    For example a walker shouldn't need to walk across the Pacific Ocean to get
    to the meeting place. Later we can probably remove this restriction and
    just stop searching if we notice that there is an impass.
    """
    print("Random location is not implemented yet")

def plan():
    """For each agent in the set of agents, calculate the optimal departure
    time.
    """
    print("Plan is not yet implemented")

agents = set()      # The set of all agents in the simulation

if __name__ == '__main__':
    n = namer()
    a1 = agent.agent(next(n))
    a2 = agent.agent(next(n))
    print('A1: ', a1.name)
    print('A2: ', a2.name)
