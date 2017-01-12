from time import time
from math import sqrt
from operator import itemgetter
from array import array
from itertools import repeat

import settings
from osm2graph import OSMGrapher
from street_graph import StreetNet


class Sim:
    def __init__(self, street_net, trips, jam_tolerance, log_callback):
        self.street_net = street_net
        self.trips = trips
        self.jam_tolerance = jam_tolerance
        self.log_callback = log_callback
        self.step_counter = 0
        self.traffic_load = array('I', repeat(0, self.street_net.street_index))
        print(self.traffic_load)
        self.cumulative_traffic_load = None

    def step(self):
        self.step_counter += 1
        self.log_callback('Preparing edges...')

        for street, street_index, length, max_speed in self.street_net:
            street_traffic_load = self.traffic_load[street_index]

            ideal_speed = calculate_driving_speed(length, max_speed, 0)

            actual_speed = calculate_driving_speed(length, max_speed,
                    street_traffic_load)

            perceived_speed = actual_speed + (ideal_speed - actual_speed) \
                    * self.jam_tolerance

            driving_time = length / perceived_speed

            self.street_net.set_driving_time(street, driving_time)

        self.traffic_load = array('I', repeat(0, self.street_net.street_index))

        origin_nr = 0

        for origin in self.trips.keys():
            origin_nr += 1
            self.log_callback('Origin nr'+str(origin_nr) + '...')
            paths = self.street_net.shortest_path(origin)

            for target, goal in paths.items():
                current = goal[0]
                while current != origin:
                    street = (min(current, paths[current]),
                              max(current, paths[current]))
                    current = paths[current]
                    usage = settings.TRIP_VOLUME
                    street_index = self.street_network.get_street_index(street)
                    self.traffic_load[street_index] += usage

def calculate_driving_speed(street_length, max_speed, number_of_trips):
    space_per_car = street_length / max(number_of_trips, 1)
    space_to_brake = max(space_per_car - settings.CAR_LEN,
            settings.MIN_BRAKE_DIST)
    potential_speed = sqrt(settings.BRAKE_DECEL*space_to_brake*2)
    actual_speed = min(max_speed, potential_speed*3.6)
    return actual_speed


if __name__ == '__main__':
    def out(*output):
        for o in output:
            print(o)
            print('')

    street_net = StreetNet()
    street_net.add_node(1, 0, 0)
    street_net.add_node(2, 0, 0)
    street_net.add_node(3, 0, 0)
    street_net.add_node(4, 0, 0)
    street_net.add_node(5, 0, 0)
    street_net.add_node(6, 0, 0)
    street_net.add_street((1, 2), 10, 50)
    street_net.add_street((2, 3), 100, 50)
    street_net.add_street((2, 4), 25, 30)
    street_net.add_street((3, 4), 120, 60)

    trips = dict()
    trips[1] = [3]
    trips[2] = [4]
    trips[3] = [4]
    trips[4] = [3]
    trips[1] = [3]
    trips[2] = [3]
    trips[2] = [3]
    trips[5] = [1]
    trips[6] = [1]
    trips[6] = [2]
    trips[5] = [2]
    sim = Sim(street_net, trips, 0.7, out)

    for step in range(10):
        print('Running simulation trip {} of 10'.format(step+1))
        sim.step()

