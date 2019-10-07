from csp.config import general


# leitura do arquivo
def read(file_path=None):
    with open(file_path) as f:
        # tamanho da placa
        linha = f.readline().split()
        L, W = (int(x) for x in linha)
        general.plate = general.NT_Plate(L, W)

        # número de peças
        linha = f.readline()
        general.num_pieces = int(linha)

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
                if general.RESTRICTED:
                    b = linha[5]
                else:
                    b = 1
                general.pieces.append(general.Piece(
                    type_, dimensions, b, False, trans))
                general.pieces_L.append(general.pieces[-1])
                general.num_pieces_L += 1
            else:  # peça regular
                type_ = general.REGULAR

                dimensions = general.Dimensions(linha[0], linha[1])

                if general.RESTRICTED:
                    b = linha[2]
                else:
                    b = 1
                    
                general.pieces.append(general.Piece(
                    type_, dimensions, b, False, False))
                general.pieces_R.append(general.pieces[-1])
                general.num_pieces_R += 1

                if general.ROTATE:
                    original_id = general.pieces[-1].id_

                    dimensions = general.Dimensions(linha[1], linha[0])

                    general.pieces.append(general.Piece(
                        type_, dimensions, b, True, False))
                    general.pieces_R.append(general.pieces[-1])
                    general.num_pieces_R += 1
                    general.num_pieces += 1

                    rotated_id = general.pieces[-1].id_

                    general.original_ids_to_rotated_ids[original_id] = rotated_id
                    general.rotated_ids_to_original_ids[rotated_id] = original_id

    general.num_pieces_without_combined_pieces = general.num_pieces - general.num_pieces_C
