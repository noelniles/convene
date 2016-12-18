# convene
Help agents gather

## Set up
1. Clone the repo by running the command `git clone https://github.com/shakabra/convene.git`
2. Install the Google Maps Python bindings. On Linux ditributions you can do this
by running `pip3 install googlemaps`.
3. Get a google maps API key. The program tries to load a google maps API key
from a text file called *mapkey.txt* if that file isn't there it will tell you.
To obtain a Google Maps API key see [this page]('https://developers.google.com/maps/documentation/geocoding/get-api-key')
4. OK...Once you have the repo cloned, the bindings installed, and an API key 
saved in *mapkey.txt* you should be ready to run the code.

## How to run
First make sure that the file called `convene` is executable and then just run
it from the command line e.g. on Linux `convene -n 5`.  
![Demo image](/demo/convene_demo.png?raw=true)

The *-n* option is to 
specify the number of agents to create in the simulation. Right now this is 
capped at 20 to reduce the risk of hitting the rate limits on the Google Maps
API.

## What's going on here.
This program generates a number of agents at random locations. All the agents
have a common destination. The first problem...  
1. Given the agents have a different speed when should each one leave?
