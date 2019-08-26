from config import general


def initial_solution():
    plate_L = general.plate.L
    plate_W = general.plate.W
    plate_area = plate_L * plate_W

    min_loss = plate_area
    piece_index = -1
    for i, piece in enumerate(general.pieces_C):
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
