from math import log10

from loguru import logger

from csp.config import general


def info():
    logger.info('Informações do problema')
    logger.info('Dimensões da placa: {}x{}'.format(general.plate.L, general.plate.W))

    logger.info('Número de peças: {0}, Número de peças R: {1}, Número de peças L: {2}, Número de peças C: {3}'.format(
        general.num_pieces, general.num_pieces_R, general.num_pieces_L, general.num_pieces_C))
    logger.info('Lista de peças R: ')
    for piece in general.pieces_R:
        logger.info('\tPeça R #{} (l: {}, w: {}, b: {}, area: {}, rotated: {}, trans: {})'.format(
            piece.id_, piece.dimensions.l, piece.dimensions.w, piece.b, piece.area, piece.rotated, piece.transformed))

    logger.info('Lista de peças L: ')
    for piece in general.pieces_L:
        logger.info('\tPeça L #{} (l1: {}, w1: {}, l2: {}, w2: {}, b: {} area: {}, loss: {}, rotated: {}, transformed: {})'.format(
            piece.id_,
            piece.dimensions.l1, 
            piece.dimensions.w1, 
            piece.dimensions.l2, 
            piece.dimensions.w2, 
            piece.b, piece.area, 
            piece.loss, 
            piece.rotated, 
            piece.transformed
            )
        )

    logger.info('Lista de peças C: ')
    for piece in general.pieces_C:
        logger.info('\tPeça C #{} (l: {}, w: {}, id1: {}, id2: {}, area: {}, loss: {}, b:{}, type_comb: {}, comb_location: {})'.format(
            piece.id_,
            piece.dimensions.l,
            piece.dimensions.w, 
            piece.combination.piece1_id, 
            piece.combination.piece2_id, 
            piece.area, piece.loss, 
            piece.b, 
            "LL" if piece.combination.type_ == 0 else "LR", 
            "VERTICAL" if piece.combination.location else "HORIZONTAL"
            )
        )


# leitura do arquivo
def read(file_path=None):
    with open(file_path) as f:
        # tamanho da placa
        linha = f.readline().split()
        L, W = (int(x) for x in linha)
        general.plate = general.NT_Plate(L, W)

        factor = max(L,W)

        num_digits = int(log10(factor))+1

        general.factor = pow(10,-(num_digits-2))

        logger.debug(f"FACTOR {general.factor}")
        
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
            
            logger.debug('Peça nova do tipo: {}'.format('REGULAR' if type_ == 1 else 'IRREGULAR'))

    general.num_pieces_without_combined_pieces = general.num_pieces - general.num_pieces_C
