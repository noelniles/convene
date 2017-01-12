"""Tools for geocoding addresses

Public functions:
    geocode   -- Geocode an address.
    createKML -- Create a KML file.
"""
import urllib, json, xml.dom.minidom
from convene import key
from config import MAPURL

def geocode(addr, sensor=False):
    """Geocode an address using Google Maps API.

    Keyword arguments:
    addr   -- An address
    sensor -- This is actually ignored in the new API
    """
    mapkey = key()
    mapurl = MAPURL

    url = ''.join([mapurl, urllib.quote(addr),
                   '&sensor=', str(sensor).lower(),
                   '&key=', mapkey])

    
def createKML(addr, fn):
    """Create a kml file for viewing in a browser or Google Earth.

    Keyword arguments:
    addr -- An address
    fn   -- A filename to write the KML.
    """
    root = xml.dom.minidom.Document()
    ns = root.createElementNS('http://earth.google.com/kml/2.2', 'kml')
    ns = root.appendChild(ns)

    doc = root.createElement('Document')
    doc = ns.appendChild(doc)

    placemark = root.createElement('Placemark')

    desc = root.createElement('description')
    desctxt = root.createTextNode(addr)
    desc.appendChild(desctxt)
    placemark.appendChild(desc)
    point = root.createElement('Point')
    placemark.appendChild(point)

    doc.appendChild(placemark)

    with open(fn, 'w') as f:
        f.write(root.toprettyxml(' '))


if __name__ == '__main__':
    createKML('627 E 21 St., Erie, PA, 16503', 'home.kml')

