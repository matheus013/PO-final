from ils.neighborhood import exchange, move, combine, perturb
from ils.util.solver import routing

neigh = [exchange, perturb, combine, move]


def local_search(solution_0, problem, max_u=3):
    best = solution_0.clone()
    u = 0
    while u < max_u:
        s = neigh[u](solution_0, problem)
        if s.f() < best.f():
            u = 0
            best = s.clone()
        else:
            u += 1
    return best


def create_solution(problem):
    node = problem.random_start()
    node = routing(problem, node)
    return node


def finale(round, max_rounds):
    return round >= max_rounds


def disturbance(k, solution):
    pre = solution.clone()
    for i in range(k):
        solution = perturb(solution)
    return solution
