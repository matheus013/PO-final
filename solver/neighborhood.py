from random import randrange


# TODO VND busca local

class Neighbor:
    def exchange(self, solution, a, b):
        # TODO todas combinações e pegar melhor
        if a == b:
            return solution
        demand_a = solution.demand_from_car[a]
        demand_b = solution.demand_from_car[b]
        if len(demand_a) == 0 and len(demand_b) == 0:
            return solution
        if len(demand_a) == 0:
            rand_b = randrange(len(demand_b))
            i = solution.demand_from_car[b].pop(rand_b)
            solution.demand_from_car[a].append(i)

            solution.build_car_routes(a)
            solution.build_car_routes(b)
            return solution
        if len(demand_b) == 0:
            rand_a = randrange(len(demand_a))
            i = solution.demand_from_car[a].pop(rand_a)
            solution.demand_from_car[b].append(i)

            solution.build_car_routes(b)
            solution.build_car_routes(a)
            return solution
        rand_a = randrange(len(demand_a))
        rand_b = randrange(len(demand_b))

        i = solution.demand_from_car[b].pop(rand_b)
        j = solution.demand_from_car[a].pop(rand_a)

        solution.demand_from_car[a].append(i)
        solution.demand_from_car[b].append(j)

        solution.build_car_routes(a)
        solution.build_car_routes(b)
        return solution

    def perturb(self, solution, index):
        demand = solution.demand_from_car[index]
        if len(demand) == 0 or len(solution.routes[index]) == 0:
            return solution
        goals = solution.goals
        # print()
        i = randrange(len(solution.routes[index]))
        while i in goals:
            i = randrange(len(solution.routes[index]))
        solution.routes[index].pop(i)
        solution.total_cost(True)
        pass

    def combine(self, solution, a, b):

        # combinar rotas
        return solution

    def move(self, solution, a, b):
        if a == b:
            return solution

        demand_a = solution.demand_from_car[a]

        if len(demand_a) == 0:
            return solution

        rand_a = randrange(len(demand_a))

        j = solution.demand_from_car[a].pop(rand_a)

        solution.demand_from_car[b].append(j)

        solution.build_car_routes(a)
        solution.build_car_routes(b)
        return solution
