import redis
import yaml
import argparse


parser = argparse.ArgumentParser(
    description='Utility for synchronizing pillar data in Redis')
parser.add_argument('-H', '--host', dest='host', default='localhost')
parser.add_argument('-p', '--port', dest='port', default=6379)
parser.add_argument('-d', '--db', dest='db', default=0)
parser.add_argument('-P', '--password', dest='password', default=None)
parser.add_argument('-f', '--file', dest='filename', default='pillar.yaml',
                    help='The file that will be used for synchronizing')
parser.add_argument('extra_params', nargs=argparse.REMAINDER,
                    help='Extra parameters to be passed in. key=value format')

args = parser.parse_args()
extra_args = {k: v for k, v in (arg.split('=') for arg in args.extra_params)}
client = redis.Redis(host=args.host, port=args.port, db=args.db,
                     password=args.password, **extra_args)

yaml_data = yaml.load(open(args.filename, 'r'))

try:
    for key, value in yaml_data.items():
        client.set(key, value)
except AttributeError:
    print("There is no YAML data in this file")

redis_data = {}
for key in client.keys():
    rkey = key.decode('utf8')
    rval = client.get(key)
    try:
        redis_data[rkey] = eval(rval)
    except (NameError, SyntaxError):
        redis_data[rkey] = rval.decode('utf8')

with open(args.filename, 'w') as pillar:
    yaml.dump(redis_data, pillar, default_flow_style=False)
