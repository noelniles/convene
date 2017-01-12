# What's going on here?
-----------------------
This is a research project to create a simulation of agents in the world who
would like to meet up. The goal is simulate a network of roads using data from
Google Maps and OpenStreetMaps (OSM) and then set the agents loose towards a destination.
Using the simulation we hope to be able to evaluate various route planning
algorithms.

Much of the simulation code has been taken from another project called
[Streets4MPI](https://github.com/jfietkau/Streets4MPI). That project has been
a valuable resource. I've modified a lot of that code and updated it to work
with Python3. Also I've decided to use [networkx](https://networkx.github.io/)
instead of [pygraph](https://pypi.python.org/pypi/pygraph/0.1.0), but in the
future I'd like to use [graph-tools](https://graph-tool.skewed.de/) because of it's
[performance](https://graph-tool.skewed.de/performance). As the name says
Streets4MPI uses MPI. I think there might be better solutions these days and
I'm not even sure that I need that yet. For large simulations of competetive
agents parallelism of some sort would be appropriate.

### [x] Phase 1
Given:  
*&nu;* -- number of agents with different speeds and locations  
*&mu;* -- a common meeting destination  
*&tau;* -- a time that all the agents should meet  

Find:  
*&lambda;* -- the time each agent should leave to arrive at *&mu;* by time *&tau;*

### [ ] Phase 2
1. Generate random agents who want to meet for some reason (food, drinks, sports...).
2. Find the best spot for them to meet.
3. Simulate each agent travelling to the meeting spot and evaluate the decisions
   made along the way.
4. Augment agents decisions using some clever algorithm.

# What does this code do?
-------------------------
The `convene` script completes phase 1. When `convene` is executed a number of
agents at random locations is generated along with a random meeting spot. Then
the script calculates when each agents should leave to be at the meeting spot
at the required time. Also a KML file is produced that can be viewed in Google
Maps.

The more interesting stuff is happening in `osm2graph.py` and the `simulation.py`.
I've laid the ground work for a road network simulation containing agents with
various vehicles. The simulation starts by ingesting an OSM file containing data
about some real place; so far I've been using Honolulu and Seattle. Using the
OSM data a graph data structure is created where the roads are edges and the
nodes are various locations. Next the agents are created at random locations;
it is possible to start the agents somewhere specific. Then agents are put onto
the graph. The cars have a length and a braking distance and the roads have a
length and a speed limit so we can tell when roads are jammed. We can also insert
congestion artificially in order to concentrate on a small number of agents.

# Set up
--------
1. Clone the repo by running the command `git clone https://github.com/shakabra/convene.git`
2. Install the Google Maps Python bindings. On Linux ditributions you can do this
by running `pip3 install googlemaps`.
3. Install imposm which is used to read OSM files.
4. Install networkx which is used to build the graph.
5. Get a google maps API key. The program tries to load a google maps API key
from a text file called *mapkey.txt* if that file isn't there it will tell you.
To obtain a Google Maps API key see [this page](https://github.com/googlemaps/google-maps-services-python)
6. OK...Once you have the repo cloned, the bindings installed, and an API key 
saved in *mapkey.txt* you should be ready to run the code.

# How to run
-------------
```
usage: convene [-h] -n #AGENTS [-l LOGFILE_NAME] [-d] [-v] [-p]

optional arguments:
  -h, --help       show this help message and exit
  -n #AGENTS       The number of agents in the simulation. Limit is 20.
  -l LOGFILE_NAME  What to call the logfile
  -d               Print extra debugging stuff
  -v               verbose output
  -p               profile
```
Make sure that the file called `convene` is executable and then run it from
the command line e.g. on Linux...   

### Barebones example
`convene -n 3`  
![Demo image](/demo/convene_demo_barebones.png?raw=true)

### Verbose with debugging and specifying the logfile
`convene -v -d -n 3 -l test.log`  
![Verbose demo image](/demo/convene_verbose_debug.png?raw=true)

### Profiling with cProfile
`convene -p -n 3`
![Profile demo](/demo/convene_profile_demo.png?raw=true)

#### N.B.
The *-n* option is to specify the number of agents to create in the simulation.
Right now this is capped at 20 to reduce the risk of hitting the rate limits on
the Google Maps API.

# Explanation of files
----------------------
**agent<span></span>.py** - This is used by convene to store the state of each agent.  
**assests**  - This holds things like text files or kml. They aren't source code,
           but the code is using it.  
**convene** - CLI app that generates a number of agents at random location. Then
              it generates a random meeting spot and computes when each agent
              should leave to meet at a certain time.  
**demo** - This holds the pictures from above.  
**DEPENDS** - Dependencies that need to be installed for this code to run.  
**LICENSE** - GPLV3  
**logs** - This is where logs should go.  
**mapview<span></span>.py** - Utilities to create a KML file for viewing in the browser.  
**osm2graph<span></span>.py** - Converts an OSM file into a graph data structure.  
**pbf_explorer.py** - This was an experiment in reading PBF files. It uses the
                      Osmium library which is trick to set up. I've since switched
                      to using imposm to read PBF files. This is just here for
                      historical reasons and it's kinda useful for poking into
                      PBF files.  
**README<span></span>.md** - You're lookin' at it.  
**setting<span></span>.py** - These are various settings for the simulation.  
**sim<span></span>.py** - A driver for the simulation.  
**simulation_driver.py** - This is going to be a parallel implementation of the
                           the simulation bu I can't decide if I should use MPI
                           or something else.  
**street_graph.py** - This is the interface to the graph data structure. Edges
                      are roads and nodes are locations.
