from config import general
from input_output.read_data import read_file
import input_output.tex as tex
from draw import piece
from cutting import cutting

general.ROTATE = True
general.REFLECT = True

file_path = './data/teste inicial.BiL'

if read_file(file_path=file_path):
    print('Número de peças: {0}, Número de peças R: {1}, Número de peças L: {2}, Número de peças C: {3}'.format(
        general.num_pieces, general.num_pieces_R, general.num_pieces_L, general.num_pieces_C))
    print('Lista de peças R: ')
    for i, peca in enumerate(general.pieces_R):
        print('Peça R #{} (l: {}, w: {})'.format(
            peca.id_, peca.dimensions.l, peca.dimensions.w))

    print('\nLista de peças L: ')
    for i, peca in enumerate(general.pieces_L):
        print('Peça L #{} - type:{} b: {} Dimensions(l1: {}, w1: {}, l2: {}, w2: {}) area: {} loss: {} rotated: {} transformed: {} '.format(peca.id_, peca.type_,
                                                                                                                                            peca.b, peca.dimensions.l1, peca.dimensions.w1, peca.dimensions.l2, peca.dimensions.w2, peca.area, peca.loss, peca.rotated, peca.transformed))
    print('\nLista de peças C: ')
    for i, peca in enumerate(general.pieces_C):
        print('Peça C #{} (l: {}, w: {}, id1: {}, id2: {}, z={}, type_comb: {}, comb_location: {})'.format(peca.id_, peca.dimensions.l,
                                                                                                           peca.dimensions.w, peca.combination.piece1_id, peca.combination.piece2_id, peca.loss, peca.combination.type_, peca.combination.location))

    print('\nDimensão da placa:', general.plate.L, 'x', general.plate.W)

    tex.preparation()
    piece.draw_pieces()
    cutting.cutting()
    tex.close_document()
    tex.generate_pdf()
