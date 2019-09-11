from config import general
from draw import pattern
from input_output import tex
from cutting.evaluate.solution.helper import knapsack


def bidimensionalKnapsack():
    print("\n\n--------------------------------------------------------")
    print("Mochila")
    L, W = general.plate.L, general.plate.W

    # pieces = [_ for _ in general.pieces if _.type_ != general.COMBINED]
    pieces = general.pieces

    strips = []

    for piece in pieces:
      if piece.type_ == general.REGULAR:
        w = piece.dimensions.w
      elif piece.type_ == general.IRREGULAR:
        w = piece.dimensions.w1
      
      if w not in strips:
        strips.append(w)
    
    strips.sort()
    num_strips = len(strips)

    strips_dict = dict()

    for i in strips:
      strips_dict[i] = []
      for piece in pieces:
        if piece.type_ == general.REGULAR or piece.type_ == general.COMBINED:
          w = piece.dimensions.w
        elif piece.type_ == general.IRREGULAR:
          w = piece.dimensions.w1
        
        if w <= i:
          strips_dict[i].append(piece.id_)

    strips = strips_dict

    print("Número de faixas: {}".format(num_strips))
    print("Faixas: {}".format(strips_dict))

    print("--------------------------------------------------------")
    print("Definindo Mochila para cada faixa")

    knapsack_problems = []

    for key in strips.keys():
      A, b, c, dummy = [], [], [], []
      constrains_types = []
      pieces_id = strips[key]

      aux = []
      c.append(L*key)
      dummy.append([0, 1, "E"])

      for id in pieces_id:
        piece = pieces[id]

        if piece.type_ == general.REGULAR or piece.type_ == general.COMBINED:
          aux.append(piece.dimensions.l)
        else:
          aux.append(piece.dimensions.l1)
        c.append(-piece.area)
        
      A.append(aux)
      b.append(L)
      constrains_types.append("L")

      knapsack_problems.append([
        dummy,
        len(pieces_id),
        len(b),
        A,
        b,
        c,
        constrains_types,
        "minimize"
      ])


    for model in knapsack_problems:
      print(model)

      print(knapsack.knapsack(model[0], model[1], model[2], model[3], model[4], model[5], model[6],model[7]))


def solve():
    bidimensionalKnapsack()
