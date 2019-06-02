import config.common as common

def initial_solution():
  plate_L = common.placa_L
  plate_W = common.placa_W
  plate_area = plate_L * plate_W

  min_lost = plate_area
  piece_index = -1
  for i, piece in enumerate(common.lista_pecas_R):
    piece_l = piece.l
    piece_w = piece.w
    piece_area = piece_l * piece_w

    # calculate how many pieces fit the length of the plate
    aux = plate_L // piece_l

    # calcutate how many pieces fit the width of the plate
    aux2 = plate_W // piece_w

    # the number of pieces is aux * aux2
    num_pieces = aux * aux2

    # total area of pieces on plate
    total_area = num_pieces * piece_area

    lost = plate_area - total_area

    if lost < min_lost:
      min_lost = lost
      piece_index = i

  return piece_index, min_lost
