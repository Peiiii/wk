import wk
from wk.extra.node import *
a=wk.ObjectFile('../data/a.txt')
a.write(3)
print(a.read())