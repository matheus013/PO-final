from random import randrange

# from data.generator import MatrixLoad
from tqdm import tqdm

from data.generator import MatrixLoad

priority = []


def finale(path, goals):
    return all(elem in path for elem in goals)


class Problem:
    origin = []
    goals = []
    cars = []
    mtz = []
    demand_by_goal = []
    routes = []
    allocated_capacity = []
    allocated_goal = []
    capacity_by_car = []
    car_x_goal = []
    cost_route = []
    demand_from_car = []
    cost_solution = -1

    def random_distribute_goals(self):
        for g in range(len(self.goals)):
            c = randrange(len(self.cars))
            if self.allocated_capacity[c] < self.capacity_by_car[c]:
                self.allocated_capacity[c] += 1
                self.car_x_goal[c][g] = 1
                self.allocated_goal[g] = 1
                self.demand_from_car[c].append(g)

    def start_routes(self):
        # TODO melhorar contrução
        for i in tqdm(range(len(self.cars)), desc='starting routes'):
            if len(self.demand_from_car[i]) > 0:
                self.build_car_routes(i)
        pass

    def build_car_routes(self, index):
        self.routes[index], self.cost_route[index] = self.build_path(self.origin, self.demand_from_car[index])

    def build_path(self, origin, goals):
        path = self.star(origin, goals)
        cost = 0
        if path is None:
            return [], 0
        for i in range(len(path) - 1):
            name_current = MatrixLoad.cities[path[i]]
            name_next = MatrixLoad.cities[path[i + 1]]
            cost += self.mtz[name_current][name_next]
        return path, cost

    def expand(self, current, alpha=0.4):
        shortlist = []
        current_index = current[0]

        if current_index >= len(self.mtz):
            return current_index, float('inf')

        for i in range(len(self.mtz)):
            name_current = MatrixLoad.cities[current_index]
            name_next = MatrixLoad.cities[i]
            if self.mtz[name_current][name_next] > 0:
                shortlist.append((i, self.mtz[name_current][name_next] + current[1]))

        # TODO lista restrita de candidato

        sorted(shortlist, key=lambda x: x[1])
        total = int(len(shortlist) * alpha)
        shortlist = shortlist[:total]
        priority.append(shortlist[randrange(len(shortlist))])

    def star(self, start, goals):
        partial_path = []
        priority.append((start, 0.0))
        while priority.__len__() > 0:
            next_node = priority.pop(0)
            partial_path.append(next_node[0])
            if finale(partial_path, goals):
                return partial_path
            self.expand(next_node)
        # return []

    def total_cost(self, force=False):
        if self.cost_solution != -1 and not force:
            return self.cost_solution

        total = 0
        for i in range(len(self.cars)):
            total += self.cost_route[i] / self.cars[i]
        self.cost_solution = total
        return total

    def possible(self):
        # TODO Otimizar
        for i in range(len(self.cars)):
            if self.allocated_capacity[i] > self.capacity_by_car[i]:
                return False
        return True
