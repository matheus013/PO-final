import os

from v2.obj.node import Problem
from v2.read.reader import Reader
from v2.util.search import create_solution, local_search, finale, disturbance
from v2.util.solver import routing

filename = "../instances/instance0.json"
data = Reader(filename).read()

p = Problem(data, os.path.basename(filename))

s0 = create_solution(p)
s0.print_test()

s = local_search(s0)

k = 2
K_MAX = 4
round = 0

while not finale(round, s):
    s_disturbed = disturbance(k, s)
    s_current = local_search(s_disturbed)
    if s_current.f() < s.f():
        s = s_current.clone()
        k = 2
    else:
        k = k + 1 if k < K_MAX else 2
    round += 1

print(s)
