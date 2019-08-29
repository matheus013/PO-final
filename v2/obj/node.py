import copy

import json
from random import randrange

from data.generator import MatrixLoad
from v2.util.map import MapIndex


class Node:

    def __init__(self, car, goals):
        self.routes = []
        self.cars = car
        self.goals = goals
        self.car_x_goal = [[0 for j in range((len(self.goals)))] for i in range((len(self.cars)))]

    def f(self):
        cost = 0
        for i in self.cars:
            cost += i.cost
        return cost

    def print_test(self):
        for index, value in enumerate(self.cars):
            if len(value.task_list) != 0:
                print(value.route, value.task_list)

    def clone(self):
        return copy.deepcopy(self)


class Car:

    def __init__(self, capacity, cost, name):
        self.name = name
        self.origin = 0
        self.cost = cost
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


class Problem:

    def __init__(self, df, ref):
        cars = df[ref]['cars']
        self.cities = json.loads(df[ref]['cities'])
        self.cars = [Car(randrange(1, 5), cars[i], i) for i in range(len(cars))]
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
