import config.common as common

def initial_solution():
  plate_L = common.placa_L
  plate_W = common.placa_W
  plate_area = plate_L * plate_W

  min_lost = plate_area
  piece_index = -1
  for i, piece in enumerate(common.lista_pecas_L):
    piece_l1 = piece.l1
    piece_w1 = piece.w1
    piece_l2 = piece.l2
    piece_w2 = piece.w2 
    # piece_max_l = max([piece_l1, piece_l2])
    piece_max_l = piece_l1
    # piece_max_w = max([piece_w1, piece_w2])
    piece_max_w = piece_w1

    piece_area = piece_max_l * piece_max_w
    # calculate how many pieces fit the length of the plate
    aux = plate_L // piece_max_l

    # calcutate how many pieces fit the width of the plate
    aux2 = plate_W // piece_max_w

    # the number of pieces is aux * aux2
    num_pieces = aux * aux2

    # total area of pieces on plate
    total_area = num_pieces * piece_area

    # total lost area of pieces on plate
    lost_piece_area = (piece_l1-piece_l2) * (piece_w1-piece_w2)
    
    total_lost_area = num_pieces * lost_piece_area

    lost = plate_area - (total_area - total_lost_area)
    print(lost)
    if lost < min_lost:
      min_lost = lost
      piece_index = i

  return piece_index, min_lost
