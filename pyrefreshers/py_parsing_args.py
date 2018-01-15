#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description="This is job about arguments")
parser.add_argument('-i', type=str, help="This is the mandatory parameter", required=True)
parser.add_argument('-o', type=str, help="This is the optional parameter", required=False)

# cmdargs ends up being a dictionary/hash
cmdargs = parser.parse_args()

# access the parameter based on the flag
ivar = cmdargs.i
print(ivar)

ovar = cmdargs.o
if ovar is not None:
  print(ovar)
