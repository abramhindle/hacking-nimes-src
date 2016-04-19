import liblo
import argparse

parser = argparse.ArgumentParser(description='Chorus!')
parser.add_argument('data', metavar='N', nargs='*',
                   help='data')
parser.add_argument("--host",default="localhost",help="Hostname")
parser.add_argument("--path",default="/test",help="Hostname")
parser.add_argument("--port",default=6668,help="Port")
args = parser.parse_args()

port = 6668
host = "localhost"
port = int(args.port)
host = args.host
path = args.path
data = args.data

def float_int_or_str(x):
    try:
       return int(x)
    except ValueError:
       """not an int"""
    try:
       return float(x)
    except ValueError:
       return str(x)

data = map(float_int_or_str,data)

target = liblo.Address(host,port)
liblo.send(target, path, *data)
