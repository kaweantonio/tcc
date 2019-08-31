from config import general
from cutting.evaluate.solution.helper import combined, irregular, regular
from draw import pattern
from input_output import tex


def best_initial_solution():
    _regular = regular.initial_solution()
    _irregular = irregular.initial_solution()
    _combined = combined.initial_solution()

    if general.DEBUG:
        print("Initial solution results:")
        print("Regular: {}".format(_regular[1]))
        print("Irregular: {}".format(_irregular[1]))
        print("Combined: {}".format(_combined[1]))
        tex.new_page()
        pattern.initial(_regular[0], _regular[1])
        tex.new_page()
        pattern.initial(_irregular[0], _irregular[1])
        tex.new_page()
        pattern.initial(_combined[0], _combined[1])
        tex.new_page()

    _best = _regular if _regular[1] < _irregular[1] else _irregular
    _best = _combined if _combined[1] < _best[1] else _best
    print(_best[0])
    print(_best[1])
    return _best
