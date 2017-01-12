"""
Search for pubs in an osm file and list their names.
"""
import osmium
import argparse, sys, pprint


class NamesHandler(osmium.SimpleHandler):
    def __init__(self, node=False, area=False, changeset=False, relation=False,
            way=False):
        super(NamesHandler, self).__init__()
        self.NODE, self.AREA, self.CHANGESET, self.RELATION, self.WAY = \
            node, area, changeset, relation, way

    def output_pubs(self, tags):
        if 'amenity' in tags: #and tags['amenity'] == 'restaurant':
            if 'name' in tags:
                print('name: {} amenity: {}'.format(tags['name'], tags['amenity']))

    def area(self, a):
        if self.AREA:
            print('**************** AREA *****************************************')
            print('orig id.....................', a.orig_id())
            print('from way?...................', a.from_way())
            print('is multipolygon?............', a.is_multipolygon())
            print('num rings...................', a.num_rings())
            for tag in a.tags:
                print('tag.........(k:{}, v:{})'.format(tag.k, tag.v))
    
    def changeset(self, c):
        print('bounds edited: ', c.bounds)

    def node(self, n):
        if self.NODE:
            print('lat:{} lon:{}'.format(n.location.lat, n.location.lon))
    
    def relation(self, r):
        if self.RELATION:
            print('*************** RELATION **************************************')
            for member in r.members:
                print('member ref:......................', member.ref)
                print('member role:.....................', member.role)
                print('member type:.....................', member.type)
            for tag in r.tags:
                print('tag.........(k:{}, v:{})'.format(tag.k, tag.v))

    def way(self, w):
        if self.WAY:
            try:
                print('Road length: ', osmium.geom.haversine_distance(w.nodes))
            except osmium._osmium.InvalidLocationError as e:
                print('ERROR: ', e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', metavar='pbf file', help='input pbf file',
            type=str, required=True)
    parser.add_argument('--node', help='print information about the nodes',
            action='store_true')
    parser.add_argument('--area', help='print information about the areas',
            action='store_true')
    parser.add_argument('--relation', help='print information about the relations',
            action='store_true')
    parser.add_argument('--changeset', help='print information about the changesets',
            action='store_true')
    parser.add_argument('--way', help='print information about the ways',
            action='store_true')
    args = parser.parse_args()

    h = NamesHandler(node=args.node, area=args.area, relation=args.relation,
            changeset=args.changeset, way=args.way)
    h.apply_file(args.i)
