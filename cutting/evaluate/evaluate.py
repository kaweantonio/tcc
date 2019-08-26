from config import general
from draw import pattern
from input_output import tex
from cutting.evaluate.solution import initial


def initial_solution():
    return initial.best_initial_solution()
