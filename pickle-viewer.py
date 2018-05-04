from os import sys
import pickle
from pprint import PrettyPrinter

fname = sys.argv[1]
pp = PrettyPrinter(width=120, compact=True)
with open(fname, "rb") as file:
    data = pickle.load(file)
    pp.pprint(data)
