import copy
from random import randrange, random

from pyUFbr.baseuf import ufbr
from tqdm import tqdm

from data.generator import MatrixLoad
from solver.neighborhood import Neighbor
from solver.solver import *

maker = MatrixLoad()
rounds = 10000

ul = 'AL'
# input
MatrixLoad.cities = ufbr.list_cidades(ul)

p = Problem()

p.origin = MatrixLoad.rand_city()

#TODO gerar instancia, e salvar um conjunto
p.mtz = MatrixLoad.get_matrix(True, ul)

n = randrange(3, len(MatrixLoad.cities) / 2)
p.goals = [MatrixLoad.rand_city() for i in range(n)]
p.cars = [randrange(3, 20) for i in range(n, n * 2)]
p.demand_by_goal = [1 for i in range(len(p.goals))]
p.capacity_by_car = [randrange(2, 10) for i in range(len(p.cars))]
p.routes = [[] for i in range(len(p.cars))]
p.allocated_capacity = [0 for i in range(len(p.cars))]
p.allocated_goal = [0 for i in range(len(p.goals))]
p.car_x_goal = [[0 for j in range((len(p.goals)))] for i in range((len(p.cars)))]
p.demand_from_car = [[] for i in range(len(p.cars))]
p.cost_route = [0 for i in range(len(p.cars))]

p.random_distribute_goals()
p.start_routes()

prob = [0.0, 0.5, 0.5, 0.5]

solutions = [(copy.deepcopy(p), p.total_cost())]
best_solution = copy.deepcopy(p)

nb = Neighbor()

n_car = len(p.cars)

alpha = 2 / 3

for i in tqdm(range(rounds), desc='running rounds'):
    if random() <= prob[0]:
        solutions.append((nb.combine(p, randrange(n_car), randrange(n_car)), p.total_cost(True)))
    if random() <= prob[1]:
        solutions.append((nb.perturb(p, randrange(n_car)), p.total_cost(True)))
    if random() <= prob[2]:
        solutions.append((nb.exchange(p, randrange(n_car), randrange(n_car)), p.total_cost(True)))
    if random() <= prob[3]:
        solutions.append((nb.move(p, randrange(n_car), randrange(n_car)), p.total_cost(True)))

    sorted(solutions, key=lambda x: x[1])
    salved = max(int(len(solutions) * alpha), 1)
    solutions = solutions[:salved]
    p = copy.deepcopy(solutions[randrange(len(solutions))][0])

    if p is None:
        p = copy.deepcopy(best_solution)

    if p.total_cost() < best_solution.total_cost() and p.possible():
        best_solution = copy.deepcopy(p)
print(best_solution.total_cost(), best_solution.routes)
