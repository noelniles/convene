#!/usr/bin/python3
""" convene.py

This is a driver used to simulate multiple agents that have a common 
destination to convene.
"""
import googlemaps
import agent


def namer():
    n = 0
    while True:
        yield n
        n += 1


if __name__ == '__main__':
    n = namer()
    a1 = agent.agent(next(n))
    a2 = agent.agent(next(n))
    print('A1: ', a1.name)
    print('A2: ', a2.name)
