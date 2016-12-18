# convene
Help agents gather

## Set up
1. Clone the repo by running the command `git clone https://github.com/shakabra/convene.git`
2. Install the Google Maps Python bindings. On Linux ditributions you can do this
by running `pip3 install googlemaps`.
3. Get a google maps API key. The program tries to load a google maps API key
from a text file called *mapkey.txt* if that file isn't there it will tell you.
To obtain a Google Maps API key see [this page](https://github.com/googlemaps/google-maps-services-python)
4. OK...Once you have the repo cloned, the bindings installed, and an API key 
saved in *mapkey.txt* you should be ready to run the code.

## How to run
```
usage: convene [-h] -n #AGENTS [-l LOGFILE_NAME] [-d] [-v]

optional arguments:
  -h, --help       show this help message and exit
  -n #AGENTS       The number of agents in the simulation. Limit is 20.
  -l LOGFILE_NAME  What to call the logfile
  -d               Print extra debugging stuff
  -v               verbose output
```
First make sure that the file called `convene` is executable and then just run
it from the command line e.g. on Linux  
### Barebones example
`convene -n 3`  
![Demo image](/demo/convene_demo_barebones.png?raw=true)

### Verbose with debugging and specifying the logfile
`convene -v -d -n 3 -l test.log`  
![Verbose demo image](/demo/convene_verbose_debug.png?raw=true)

#### N.B.
The *-n* option is to specify the number of agents to create in the simulation.
Right now this is capped at 20 to reduce the risk of hitting the rate limits on
the Google Maps API.

## What's going on here.
This program generates a number of agents at random locations. All the agents
have a common destination. The first problem...  
1. Given the agents have a different speed calculate the time each one should 
leave in order to arrive at a common meeting point.
