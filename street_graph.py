import networkx as nx

class StreetNet(object):
    ST_ATTR_IND_IND = 0
    ST_ATTR_IND_LEN = 1
    ST_ATTR_IND_MAX = 2
    ND_ATTR_IND_LON = 0
    ND_ATTR_IND_LAT = 1

    def __init__(self):
        self._graph = nx.Graph()
        self.bounds= None
        self.street_index = 0
        self.streets_by_index = dict()

    def has_street(self, street):
        return self._graph.has_edge(street[0], street[1])

    def add_street(self, street, length, max_speed):
        print('''calling add_string with street:{}\
                 length:{} max_speed:{}'''.format(street, length, max_speed))
        street_attr = [self.street_index, length, max_speed]
        driving_time = length / max_speed
        self._graph.add_edge(street[0], street[1], weight=driving_time, 
                attrs=street_attr)
        self.streets_by_index[self.street_index] = street
        self.street_index += 1

    def set_driving_time(self, street, driving_time):
        self._graph[street[0]][street[1]]['weight'] = driving_time

    def get_driving_time(self, street):
        return self._graph[street[0]][street[1]]['weight']

    def get_street_index(self, street):
        attr = nx.get_edge_attributes(self._graph, 'attrs')

    def get_street_by_index(self, street_index):
        if street_index in self.streets_by_index:
            return self.streets_by_index[street_index]
        else:
            return None

    def change_maxspeed(self, street, max_speed_delta):
        street_attr = nx.get_edge_attributes(self._graph, 'attrs')
        current_max_speed = street_attr
        print('CHANGE MAXSPEED (NOT IMPPLEMENTED!!!): ', street_attr)

    def set_bounds(self, minlat, maxlat, minlon, maxlon):
        self.bounds = ((minlat, maxlat), (minlon, maxlon))

    def add_node(self, node, lon, lat):
        lonlat = {'lon':lon, 'lat':lat}
        self._graph.add_node(node, lonlat)

    def get_nodes(self):
        return self._graph.nodes()

    def has_node(self, node):
        return self._graph.has_node(node)

    def num_edges(self):
        return self._graph.number_of_edges()

    def num_nodes(self):
        return self._graph.number_of_nodes()

    def draw_streets(self):
        nx.draw(self._graph)

    def nodes_iter(self):
        it = nx.nodes_iter(self._graph)
        yield from it

    def neighbors(self, node):
        return nx.neighbors(self._graph, node)

    def node_coordinates(self, node):
        lat = nx.get_node_attributes(self._graph, 'lat').get(node)
        lon = nx.get_node_attributes(self._graph, 'lon').get(node)
        return (lat, lon)

    def shortest_path(self, u):
        try:
            return nx.shortest_path(self._graph, source=u, weight='weight')
        except nx.exception.NetworkXNoPath as e:
            print(e)

    def __iter__(self):
        for street in self._graph.edges():
            if street[0] > street[1]:
                continue
            u, v = street
            edge_data = self._graph.get_edge_data(u, v)['attrs']
            print('edge data: ', edge_data)
            yield (street, edge_data[StreetNet.ST_ATTR_IND_IND],
                    edge_data[StreetNet.ST_ATTR_IND_LEN],
                    edge_data[StreetNet.ST_ATTR_IND_MAX])
