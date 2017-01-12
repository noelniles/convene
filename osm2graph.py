import argparse, time
from imposm.parser import OSMParser as parser
from street_graph import StreetNet
from math import sqrt, sin, cos, radians, asin


class OSMGrapher():
    LAT = 0
    LON = 1

    def __init__(self, osmfile):
        self.street_net = StreetNet()
        self.coords = dict()

        self.bounds = dict()
        self.bounds['minlat'] = 9999
        self.bounds['maxlat'] = -9999
        self.bounds['minlon'] = 9999
        self.bounds['maxlon'] = -9999

        self.all_osm_relations = dict()
        self.all_osm_ways = dict()
        self.all_osm_nodes = dict()

        self.residential_nodes = set()
        self.industrial_nodes = set()
        self.commercial_nodes = set()

        self.connected_residential_nodes = set()
        self.connected_industrial_nodes = set()
        self.connected_commercial_nodes = set()

        self.max_speed_map = dict()
        self.max_speed_map['motorway'] = 140
        self.max_speed_map['trunk'] = 120
        self.max_speed_map['primary'] = 100
        self.max_speed_map['secondary'] = 80
        self.max_speed_map['tertiary'] = 70
        self.max_speed_map['road'] = 50
        self.max_speed_map['minor'] = 50
        self.max_speed_map['unclassified'] = 50
        self.max_speed_map['residential'] = 30
        self.max_speed_map['track'] = 30
        self.max_speed_map['service'] = 20
        self.max_speed_map['path'] = 10
        self.max_speed_map['cycleway'] = 1
        self.max_speed_map['bridleway'] = 1
        self.max_speed_map['pedestrian'] = 1
        self.max_speed_map['footway'] = 1

        p = parser(concurrency=4,
                   coords_callback = self.coords_callback,
                   nodes_callback = self.nodes_callback,
                   ways_callback = self.ways_callback,
                   relations_callback = self.relations_callback)
        p.parse(osmfile)


    def build_street_net(self):
        """Build a graph from an OSM file."""
        if 9999 not in self.bounds.values() and -9999 not in self.bounds.values():
            self.street_net.set_bounds(self.bounds['minlat'], self.bounds['maxlat'],
                                       self.bounds['minlon'], self.bounds['maxlon'])

        for osmid, tags, refs in self.all_osm_ways.values():
            if "highway" in tags:
                if not self.street_net.has_node(refs[0]):
                    coord = self.coords[refs[0]]
                    self.street_net.add_node(refs[0], coord[self.LON],
                                             coord[self.LAT])
                for i in range(0, len(refs)-1):
                    if not self.street_net.has_node(refs[i+1]):
                        coord = self.coords[refs[i+1]]
                        self.street_net.add_node(refs[i+1], coord[self.LON],
                                                 coord[self.LAT])
                        street = (refs[i], refs[i+1])

                        street_len = self.haversine(refs[i], refs[i+1])

                        max_speed = 50
                        if tags['highway'] in self.max_speed_map.keys():
                            max_speed = self.max_speed_map[tags['highway']]
                        if 'maxspeed' in tags:
                            max_speed_tag = tags['maxspeed']
                            if max_speed_tag.isdigit():
                                max_spped = int(max_speed_tag)
                            elif max_speed_tag.endswith('mph'):
                                max_speed = int(max_speed_tag.replace('mph','').
                                        strip(' '))
                            elif max_speed_tag == 'none':
                                max_speed = 140

                        if not self.street_net.has_street(street):
                            self.street_net.add_street(street, street_len,
                                                           max_speed)
        return self.street_net

    def coords_callback(self, coords):
        for osmid, lon, lat in coords:
            self.coords[osmid] = dict([(self.LAT, lat),(self.LON, lon)])
            self.bounds['minlat'] = min(self.bounds['minlat'], lat)
            self.bounds['maxlat'] = max(self.bounds['maxlat'], lat)
            self.bounds['minlon'] = min(self.bounds['minlon'], lon)
            self.bounds['maxlon'] = min(self.bounds['maxlon'], lon)

    def nodes_callback(self, nodes):
        for node in nodes:
             self.all_osm_nodes[node[0]] = node

    def relations_callback(self, relations):
        for relation in relations:
            self.all_osm_relations[relation[0]] = relation
    
    def ways_callback(self, ways):
        for way in ways:
            self.all_osm_ways[way[0]] = way

    def nodes(self, node):
        for n in node:
            print('NODE: ', n, end='\n\n\n')

    def haversine(self, id1, id2):
        """Returns the Haversine distance in meters."""
        lat1 = self.coords[id1][self.LAT]
        lon1 = self.coords[id1][self.LON]
        lat2 = self.coords[id2][self.LAT]
        lon2 = self.coords[id2][self.LON]
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        return 6367000 * c


if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument('--pbf', metavar='<osm file>', help='input pbf file',
            type=str)
    aparser.add_argument('all_coordinates', help='print every lat/log',
            action='store_true')
    args = aparser.parse_args()

    osmfile = args.pbf

    grapher = OSMGrapher(osmfile)
    street_net = grapher.build_street_net()

    print('Number of Edges: {}\nNumber of Nodes: {}\n'.format(
        street_net.num_edges(), street_net.num_nodes()))

    if args.all_coordinates:
        for node in street_net.nodes_iter():
            print(street_net.node_coordinates(node))

