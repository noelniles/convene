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
        self.start_geo = None       # Start point
        self.end_geo = None         # End point
        self.start_address = None
        self.end_address = None
        self.leave = None       # When this agent should leave
        self.mode = None        # Mode of transit
        self.delta = 0
