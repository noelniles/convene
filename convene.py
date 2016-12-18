#!/usr/bin/python3
""" convene.py

This is a driver used to simulate multiple agents that have a common 
destination to convene.
"""
import argparse, time, random
from datetime import datetime
import googlemaps
import agent


def namer():
    """Yield the next integer. Used to generate unique sequential names."""
    n = 0
    while True:
        yield n
        n += 1

def key():
    """Get the google maps api key from the text file."""
    with open('mapkey.txt') as f:
        line = f.readline()
    return line

def random_time():
    """Generate a random meeting time not guaranteed to be future."""
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    t = datetime(year, month, day, hour, minute)
    return t

def mode_of_transit(agent):
    """Choose a mode of transit based on agent's speed."""
    n = random.randint(0, 1)
    if 0 < agent.speed < 5:
        agent.mode = 'walking'
    elif 5 < agent.speed < 15:
        agent.mode = 'bicycling'

    # Speeds over fifteen could be driving or transit.
    elif 15 < agent.speed < 30:
        if n == 0: agent.mode = 'transit'
        if n == 1: agent.mode = 'driving'
    else:
        if n == 0: agent.mode = 'transit'
        if n == 1: agent.mode = 'driving'

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

def plan(agents, dest):
    """For each agent in the set of agents, calculate the optimal departure time.
   
    TODO:
    This is the one function that makes requests to the google maps API so it
    would be a good idea to cache these results for a little while so we don't
    hit the rate limit.
    """
    print('planning...')
    k = key().strip()
    gmaps = googlemaps.Client(k)
    res = gmaps.distance_matrix('21.326674, -157.873421', '21.305277, -157.655481')
    print(res)
    for a in agents:
        dist = gmaps.distance_matrix(a.start, dest)
        print(dist)

agents = set()      # The set of all agents in the simulation

if __name__ == '__main__':
    # Set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nagents', type=int)
    args = parser.parse_args()

    if args.nagents is None or args.nagents < 1 or args.nagents > 15:
        print('You have to supply a number of agents [1-15] as an argument')

    # Generate a random place to convene.
    dest = random_location()

    # Generate a random time to convene.
    meeting_time = random_time()

    # Create new agents and add them to the set of agents.
    n = namer()
    while args.nagents:
        # Generate an agent with a name.
        a = agent.agent(next(n))

        # Give the agent a random starting location.
        a.start = random_location()

        # Set the meeting point.
        a.end = dest

        # Give the agent a random speed.
        a.speed = random.randint(2, 80)

        # Add the newly created agent to the set of agents
        agents.add(a)

        # Set the mode of transportation
        mode_of_transit(a)

        # Movin on...
        args.nagents -= 1

    plan(agents, dest)
    #for agent in agents:
    #    print('--------------------------------------------------------------')
    #    print('Name: ', agent.name)
    #    print('Start: ', agent.start)
    #    print('End: ', agent.end)
    #    print('Speed: ', agent.speed)
    #    print('Mode: ', agent.mode)
    #    print('--------------------------------------------------------------')


    print(key())
    print(meeting_time)
