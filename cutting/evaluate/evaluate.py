from config import general
from cutting.evaluate.solution import initial, optimal


def initial_solution():
    return initial.solve()


def optimal_solution():
    optimal.solve()
