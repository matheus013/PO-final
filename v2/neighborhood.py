from random import randrange

from v2.util.solver import solver


def exchange(solution, problem):
    n = len(solution.cars)
    for index, value in enumerate(solution.cars):
        b = randrange(n)
        if index == b:
            continue
        goals_a = solution.task_of(index)
        goals_b = solution.task_of(b)
        if len(goals_a) == 0 or len(goals_b) == 0:
            continue
        job_a = randrange(len(goals_a))
        job_b = randrange(len(goals_b))

        i = solution.task_of(index).pop(job_a)
        j = solution.task_of(b).pop(job_b)

        solution.task_of(index).append(i)
        solution.task_of(b).append(j)

        solution.cars[index] = solver(solution.cars[index], problem)
        solution.cars[b] = solver(solution.cars[b], problem)
    return solution.clone()


def perturb(solution, problem=None):
    index = randrange(len(solution.cars))
    pre = solution.clone()
    demand = solution.task_of(index)

    if len(demand) == 0 or len(solution.task_of(index)) < 2:
        return solution
    goals = solution.task_of(index)

    i = randrange(len(solution.task_of(index)))
    while i in goals:
        length_route = len(solution.routes_of(index))
        if length_route != 0:
            i = randrange(length_route)
            solution.routes_of(index).pop(i)
            break
        i = randrange(len(solution.task_of(index)))
    return solution if solution.cars[index].possible() else pre


def combine(solution, problem):
    return solution


def move(solution, problem):
    n = len(solution.cars)

    a = randrange(n)
    b = randrange(n)

    if a == b:
        return solution

    demand_a = solution.task_of(a)

    if len(demand_a) == 0:
        return solution

    rand_a = randrange(len(demand_a))

    j = solution.task_of(a).pop(rand_a)

    solution.task_of(b).append(j)

    solution.cars[a] = solver(solution.cars[a], problem)
    solution.cars[b] = solver(solution.cars[b], problem)
    return solution.clone()
