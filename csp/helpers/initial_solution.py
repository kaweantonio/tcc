from csp.config import general
from csp.helpers import pattern, tex


def regular(plate_L, plate_W, plate_area, pieces):

    min_loss = plate_area
    piece_index = -1

    for piece in pieces:
        piece_l = piece.dimensions.l
        piece_w = piece.dimensions.w
        piece_area = piece.area

        # calculate how many pieces fit the length of the plate
        aux = plate_L // piece_l

        # calcutate how many pieces fit the width of the plate
        aux2 = plate_W // piece_w

        # the number of pieces is aux * aux2
        num_pieces = aux * aux2

        # total area of pieces on plate
        total_area = num_pieces * piece_area

        loss = plate_area - total_area

        if loss < min_loss:
            min_loss = loss
            piece_index = piece.id_

    return piece_index, min_loss


def irregular(plate_L, plate_W, plate_area, pieces):

    min_loss = plate_area
    piece_index = -1
    
    for piece in pieces:
        piece_l1 = piece.dimensions.l1
        piece_w1 = piece.dimensions.w1

        piece_area = piece.area
        # calculate how many pieces fit the length of the plate
        aux = plate_L // piece_l1

        # calcutate how many pieces fit the width of the plate
        aux2 = plate_W // piece_w1

        # the number of pieces is aux * aux2
        num_pieces = aux * aux2

        # total area of pieces on plate
        total_area = num_pieces * piece_area

        # # total loss area of pieces on plate
        # loss_piece_area = piece.loss
        # total_loss_area = num_pieces * loss_piece_area

        loss = plate_area - total_area
        if loss < min_loss:
            min_loss = loss
            piece_index = piece.id_
    print(min_loss)
    return piece_index, min_loss


def combined(plate_L, plate_W, plate_area, pieces):
    min_loss = plate_area
    piece_index = -1
    for piece in pieces:
        if piece.combination.type_ == general.COMBINE_LL:
            piece_l = piece.dimensions.l
            piece_w = piece.dimensions.w
            piece_area = piece.area

            # calculate how many pieces fit the length of the plate
            aux = plate_L // piece_l

            # calcutate how many pieces fit the width of the plate
            aux2 = plate_W // piece_w

            # the number of pieces is aux * aux2
            num_pieces = aux * aux2

            # total area of pieces on plate
            total_area = num_pieces * piece_area

            # # total loss area of pieces on plate
            # loss_piece_area = piece.loss
            # total_loss_area = num_pieces * loss_piece_area

            loss = plate_area - total_area

            if loss < min_loss:
                min_loss = loss
                piece_index = piece.id_

    return piece_index, min_loss


def composed():
    raise NotImplementedError


def solve():
    plate_L = general.plate.L
    plate_W = general.plate.W
    plate_area = plate_L * plate_W
    
    _regular = regular(plate_L, plate_W, plate_area, general.pieces_R)
    _irregular = irregular(plate_L, plate_W, plate_area, general.pieces_L)
    _combined = combined(plate_L, plate_W, plate_area, general.pieces_C)

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
    return _best
