from config import general
from cutting.evaluate import evaluate
from draw import pattern


def cutting():
    initial_solution = evaluate.initial_solution()
    pattern.initial(initial_solution[0], initial_solution[1])

    evaluate.optimal_solution()
