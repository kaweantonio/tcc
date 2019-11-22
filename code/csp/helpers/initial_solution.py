from copy import deepcopy as copy
from operator import itemgetter

from loguru import logger

from csp.config import general
from csp.helpers import pattern, tex

def regular(plate_L, plate_W, plate_area, pieces):

    area = 0
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


        if total_area > area:
            area = total_area
            piece_index = piece.id_

    loss = 1 - (area / general.plate.area)        
    
    return piece_index, loss


def irregular(plate_L, plate_W, plate_area, pieces):

    area = 0
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

        if total_area > area:
            area = total_area
            piece_index = piece.id_

    loss = 1 - (area / general.plate.area)        
    
    return piece_index, loss


def combined(plate_L, plate_W, plate_area, pieces):
    area = 0
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

            if total_area > area:
                area = total_area
                piece_index = piece.id_
    
    loss = 1 - (area / general.plate.area)        
    
    return piece_index, loss


def composed():
    logger.info("Buscando solução inicial homogênea composta")
    L, W = general.plate.L, general.plate.W
    value = 0
    strips = []
    strips_pieces = []
    strips_w = []
    pieces = copy(general.pieces[:general.num_pieces_without_combined_pieces])

    pieces_ordered = sorted(pieces, key= lambda x: itemgetter(1)(x.dimensions), reverse=True)

    for i, piece in enumerate(pieces_ordered):
        strip_L = L
        demand = piece.b

        if demand == 0: 
            continue

        l, w = itemgetter(0)(piece.dimensions), itemgetter(1)(piece.dimensions)
        if w <= W:        
            strips.append([])
            strips_pieces.append([])
            strips_w.append(w)
            W -= w
        else:
            break

        num_pieces = L // l

        num_pieces = min(demand, num_pieces)

        for _ in range(num_pieces):
            strips_pieces[-1].append(piece.id_)
            strips[-1].append(num_pieces)

        demand -= num_pieces
        strip_L -= num_pieces * l
        value += num_pieces * piece.area

        while demand > 0:
            strips.append([])
            strips_pieces.append([])
            strip_L = L
            strips_w.append(w)

            num_pieces = L // l

            num_pieces = min(num_pieces, demand)

            for _ in range(num_pieces):
                strips_pieces[-1].append(piece.id_)
                strips[-1].append(num_pieces)
            
            demand -= num_pieces
            strip_L -= num_pieces * l
            value += num_pieces * piece.area
        
        for j, piece2 in enumerate(pieces_ordered[i+1:], start=i+1):
            l, w = itemgetter(0)(piece2.dimensions), itemgetter(1)(piece2.dimensions)
            if l <= strip_L and piece2.b > 0:
                demand = piece2.b
                num_pieces = strip_L // l 

                num_pieces = min(demand, num_pieces)

                for _ in range(num_pieces):
                    strips_pieces[-1].append(piece2.id_)
                    strips[-1].append(num_pieces)

                pieces_ordered[j].b -= num_pieces
                strip_L -= num_pieces * l
                value += num_pieces * piece2.area
    
    value = 1 - (value / general.plate.area)

    logger.info("Solução encontrada")
    logger.info(' z*={}%'.format(round(value*100,3)))
    logger.info(' Faixas:')
    for i, strip in enumerate(strips_pieces):
        logger.info('  Faixa {}: {}'.format(i, strip))
    
    return strips, value, strips_pieces, strips_w

def solve():
    plate_L = general.plate.L
    plate_W = general.plate.W
    plate_area = plate_L * plate_W
    
    logger.info("Buscando solução inicial homogênea simples")
    _regular = regular(plate_L, plate_W, plate_area, general.pieces_R)
    _irregular = irregular(plate_L, plate_W, plate_area, general.pieces_L)
    _combined = combined(plate_L, plate_W, plate_area, general.pieces_C)

    if general.DEBUG:
        logger.debug("Soluções iniciais encontradas")
        logger.debug(" Regular: z*={}%".format(round(_regular[1]*100, 3)))
        logger.debug(" Irregular: z*={}%".format(round(_irregular[1]*100,3)))
        logger.debug(" Combined: z*={}%".format(round(_combined[1]*100,3)))

        if general.DRAW:
            logger.debug("Desenhando soluções iniciais encontradas")
            if _regular[0] >= 0:
                pattern.initial(_regular[0], _regular[1])
            if _irregular[0] >= 0:
                pattern.initial(_irregular[0], _irregular[1])
            if _combined[0] >= 0:
                pattern.initial(_combined[0], _combined[1])

    _best = _regular if _regular[1] < _irregular[1] else _irregular
    _best = _combined if _combined[1] < _best[1] else _best

    logger.info("Melhor solução inicial: z*={}% com peça {}".format(round(_best[1]*100, 3), _best[0]))
    return _best
