from pymongo import MongoClient
import yaml
import argparse


parser = argparse.ArgumentParser(
    description='Utility for synchronizing pillar data in Redis')
parser.add_argument('-H', '--host', dest='host', default='localhost')
parser.add_argument('-p', '--port', dest='port', default=27017)
parser.add_argument('-d', '--db', dest='db', default='salt')
parser.add_argument('-c', '--collection', dest='collection', default='pillar')
parser.add_argument('-P', '--password', dest='password', default=None)
parser.add_argument('-f', '--file', dest='filename', default='pillar.yaml',
                    help='The file that will be used for synchronizing')
parser.add_argument('extra_params', nargs=argparse.REMAINDER,
                    help='Extra parameters to be passed in. key=value format')

args = parser.parse_args()
extra_args = {k: v for k, v in (arg.split('=') for arg in args.extra_params)}
client = MongoClient(args.host, args.port)

yaml_data = yaml.load(open(args.filename, 'r'))

try:
    for key, value in yaml_data.items():
        client[args.db].insert(dict(key, value))
except AttributeError:
    print("There is no YAML data in this file")

mongo_data = {}
for doc in client.find():
    val.popitem('_id')
    try:
        mongo_data.update(eval(val))
    except (NameError, SyntaxError):
        mongo_data[key] = val.decode('utf8')

with open(args.filename, 'w') as pillar:
    yaml.dump(mongo_data, pillar, default_flow_style=False)
