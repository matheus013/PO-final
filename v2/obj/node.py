import copy

import json
from random import randrange

from data.generator import MatrixLoad
from v2.util.map import MapIndex
from v2.util.solver import all_goals


class Node:
    def __init__(self, car, goals):
        self.routes = []
        self.cars = car
        self.goals = goals

    def f(self):
        cost = 0
        for i in self.cars:
            cost += i.total_cost
        return cost

    def print_test(self, solution=False):
        total_cost = 0
        total_hop = 0
        si = 0
        print('-----------------------------------------')
        for index, value in enumerate(self.cars):
            if len(value.task_list) != 0 and len(value.route) != 0:
                total_cost += value.calculate_cost()
                total_hop += len(value.route)
                if solution:
                    print('s' + str(si) + ' -> route: ' + str(value.route) + ' | cost: ' + str(
                        value.calculate_cost()) + ' to tasks: ' + str(value.task_list))
                    si += 1
        print('total_hop: %d, total_cost: %.2f' % (total_hop, total_cost))
        print('-----------------------------------------')

    def clone(self):
        return copy.deepcopy(self)

    def task_of(self, index):
        return self.cars[index].task_list

    def routes_of(self, index):
        return self.cars[index].route

    def possible(self):
        for index, value in enumerate(self.cars):
            if not value.possible():
                return False
        return True


class Car:
    def __init__(self, capacity, cost, name):
        self.name = name
        self.origin = 0
        self.cost = cost
        self.total_cost = -1
        self.capacity = capacity
        self.demand = 0
        self.task_list = []
        self.allocation = 0
        self.route = []
        self.cost_route = 0

    def alloc_task(self, task):
        self.task_list.append(task)
        self.allocation += 1

    def available(self):
        return self.allocation < self.capacity

    def __str__(self):
        result = str(self.capacity) + ' | ' + str(self.cost) + ' | ' + str(self.name)
        return result

    def calculate_cost(self, force=False):
        if not force and self.total_cost != -1:
            return round(self.total_cost, 2)
        self.total_cost = self.cost_route / self.cost
        return round(self.total_cost, 2)

    def possible(self):
        # TODO Otimizar
        return self.allocation <= self.capacity and all_goals(self.route, self.task_list)


class Problem:
    def __init__(self, df, ref):
        cars = df[ref]['cars']
        cap = df[ref]['cap']
        self.cities = json.loads(df[ref]['cities'])
        self.cars = [Car(cap[i], cars[i], i) for i in range(len(cars))]
        self.demand = json.loads(df[ref]['demand'])
        self.map = MapIndex()
        self.node = Node(self.cars, self.demand)
        self.priority = []

        MatrixLoad.cities = self.cities
        dist = MatrixLoad.get_matrix(only_read=True, uf=False)

        self.map.mapping(dist, MatrixLoad.cities)

    def dist_from_name(self, source, destination):
        return self.map.from_name(source, destination)

    def dist_from_index(self, source, destination):
        return self.map.mt[source][destination]

    def count_cities(self):
        return len(self.cities)

    def random_start(self):
        allocated = 0
        check = [0 for i in range(len(self.demand))]
        while allocated < len(self.demand):
            g = randrange(len(self.demand))

            if check[g] == 1:
                continue

            c = randrange(len(self.cars))
            if self.cars[c].available():
                self.cars[c].alloc_task(g)
                check[g] = 1
                allocated += 1
        return Node(self.cars, self.demand)
