from random import randrange

priority = []
mtz = []


def finale(path, goals):
    return all(elem in path for elem in goals)


def cut(shortlist, alpha):
    sorted(shortlist, key=lambda x: x[1])
    total = int(len(shortlist) * alpha)
    return shortlist[:total]


def expand(current, problem, alpha=0.4):
    shortlist = []
    current_index = current[0]

    if current_index >= len(mtz):
        return current_index, float('inf')

    for i in range(problem.count_cities()):
        if mtz[current_index][i] > 0:
            shortlist.append((i, mtz[current_index][i] + current[1]))

    shortlist = cut(shortlist, alpha)
    priority.append(shortlist[randrange(len(shortlist))])


def star(origin, problem, task_list):
    partial_path = []
    priority.append((origin, 0.0))

    while priority.__len__() > 0:
        next_node = priority.pop(0)
        partial_path.append(next_node[0])
        if finale(partial_path, task_list):
            return partial_path
        expand(next_node, problem)


def build_path(car, problem):
    global priority
    path = star(car.origin, problem, car.task_list)
    priority = []

    car.route = path
    return car


def solver(car, problem):
    return build_path(car, problem)


def routing(problem, solution):
    global mtz
    mtz = problem.map.mt
    for index, value in enumerate(solution.cars):
        if len(solution.cars) > 0:
            solution.cars[index] = solver(value, problem)
    return solution
