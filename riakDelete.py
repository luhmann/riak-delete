import argparse
import os
import requests
import json
from riak import RiakClient, RiakNode

parser = argparse.ArgumentParser(description='Takes a list of redis keys and deletes them')
parser.add_argument('--host', dest='dest_riak', default='10.228.39.181', help='The host we push the riak data')
args = parser.parse_args()

# map arguments
dest_riak_host = args.dest_riak
print 'Targeted Riak Host ' + dest_riak_host

base_dir = os.path.dirname(os.path.realpath(__file__))

# connect to live riak
riak_connection = RiakClient(protocol='http', host=dest_riak_host, http_port=8098)
print riak_connection.ping()

riak_bucket = riak_connection.bucket('ez')

# Parses the keys.txt file and writes url
def readRiakKeys():
    keyListFilename = os.path.join(base_dir, 'keys.txt')
    return  [line.strip() for line in open(keyListFilename, 'r')]

imgs = readRiakKeys()
print 'Deleting Riak Keys: \n' + '\n'.join(imgs)

# get and save all images
for img in imgs:
    print 'Now deleting key: ' + img
    obj = riak_bucket.get(img)
    print 'Image exists? ' + str(obj.exists)
    if obj.exists is True:
      obj.delete()
      obj = riak_bucket.get(img)
      print 'Image exists? ' + str(obj.exists)
