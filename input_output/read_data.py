import config.general as general


def combine_L_pieces():
    # combine L pieces with their mirrored pieces
    for piece in general.pieces_L:
        # combine piece by 'horizontal'
        new_l = piece.dimensions.l1 + piece.dimensions.l2
        new_w = 2 * piece.dimensions.w2 if piece.dimensions.w1 - \
            piece.dimensions.w2 < piece.dimensions.w2 else (piece.dimensions.w1)
        b = piece.b * 2
        dimensions = general.Dimensions(new_l, new_w)
        combination = general.Combination(
            piece.id_, piece.id_, general.COMBINE_LL, general.HORIZONTAL)
        new_piece = general.Piece(
            general.COMBINED, dimensions, b, False, False, combination)

        new_piece = general.pieces.append(new_piece)
        general.pieces_C.append(general.pieces[-1])
        general.num_pieces_C += 1
        general.num_pieces += 1

        # combine piece by 'vertical'
        new_l = 2 * piece.dimensions.l2 if piece.dimensions.l1 - \
            piece.dimensions.l2 < piece.dimensions.l2 else piece.dimensions.l1
        new_w = piece.dimensions.w1 + piece.dimensions.w2
        b = piece.b * 2
        dimensions = general.Dimensions(new_l, new_w)
        combination = general.Combination(
            piece.id_, piece.id_, general.COMBINE_LL, general.VERTICAL)
        new_piece = general.Piece(
            general.COMBINED, dimensions, b, False, False, combination)

        new_piece = general.pieces.append(new_piece)
        general.pieces_C.append(general.pieces[-1])
        general.num_pieces_C += 1
        general.num_pieces += 1

# leitura do arquivo


def read_file(file_path=None):
    if file_path is None:
        return 0

    with open(file_path) as f:
        # tamanho da placa
        linha = f.readline().split()
        L, W = (int(x) for x in linha)
        general.plate = general.NT_Plate(L, W)

        # número de peças
        linha = f.readline()
        general.num_pieces = int(linha)

        pecas_R_rotated = []

        for _ in range(general.num_pieces):
            linha = [int(x) for x in (f.readline().split())]

            # verifica se a peça é regular ou do tipo-L
            if linha[0] == general.IRREGULAR:  # peça do tipo L
                trans = False

                # all L-pieces need to have L1 greater than W1,
                # if not, "rotate" the piece so that W1 becomes the new L1
                # finally, "reflect" the piece
                if linha[1] < linha[2]:
                    aux = linha[1]
                    linha[1] = linha[2]
                    linha[2] = aux

                    aux = linha[3]
                    linha[3] = linha[4]
                    linha[4] = aux
                    trans = True
                type_ = general.IRREGULAR
                dimensions = general.Dimensions_IRREGULAR(
                    linha[1], linha[2], linha[3], linha[4])
                b = linha[5]

                general.pieces.append(general.Piece(
                    type_, dimensions, b, False, trans))
                general.pieces_L.append(general.pieces[-1])
                general.num_pieces_L += 1
            else:  # peça regular
                type_ = general.REGULAR

                dimensions = general.Dimensions(linha[0], linha[1])
                b = linha[2]

                general.pieces.append(general.Piece(
                    type_, dimensions, b, False, False))
                general.pieces_R.append(general.pieces[-1])
                general.num_pieces_R += 1

                if general.ROTATE:
                    dimensions = general.Dimensions(linha[1], linha[0])

                    general.pieces.append(general.Piece(
                        type_, dimensions, b, True, False))
                    general.pieces_R.append(general.pieces[-1])
                    general.num_pieces_R += 1
                    general.num_pieces += 1

        combine_L_pieces()

        return 1
