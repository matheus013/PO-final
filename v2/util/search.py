from v2.obj.node import Node
from v2.util.solver import routing


def local_search(solution_0):
    return Node([], [])


def create_solution(problem):
    node =problem.random_start()
    node = routing(problem, node)
    return


def finale(round, solution):
    if round >= 10:
        return True
    return False


def disturbance(k, solution):
    return solution
