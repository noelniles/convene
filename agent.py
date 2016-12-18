""" agent.py

This class represents an agent that has somewhere to convene with other
agents. Each agent shall have their own speed and their own view of the
world (map).
"""
class agent:
    def __init__(self, name):
        self.name = name
        self.speed = 0
        self.world = None       # Map of the world, not implemented yet
        self.start = None       # Start point
        self.end = None         # End point
        self.leave = None       # When this agent should leave
        self.mode = None        # Mode of transit
