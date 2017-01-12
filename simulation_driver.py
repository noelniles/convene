from datetime import datetime
from random import random, seed
from array import array
from itertools import repeat

from mpi4py import MPI

from osm2graph import OSMGrapher
from sim import Sim
from settings import settings
from cereal import Cereal
from utils import *


class SimDriver():
    def __init_(self):
        comm = MPI.COMM_WORLD
