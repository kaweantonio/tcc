import os
import argparse

from csp.config import general
from csp.helpers import tex, piece
from csp.csp import cuttingStockProblem


def main(file_path):
    problem = cuttingStockProblem(file_path)

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

    problem.get_solution()

    print(problem.solution, problem.solution_loss)

    tex.close_document()
    tex.generate_pdf()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rotate', action='store_true', default=False, help='rotate regular pieces')
    parser.add_argument('-m', '--mirror', action='store_true', default=False, help='reflect/rotate irregular pieces in 180 degrees')
    
    parser.add_argument('input', help='input file, PDF format')
    parser.add_argument('output', help='output file, PDF format (default: output.pdf)', default="output.pdf", nargs='?')
    

    args = parser.parse_args()

    if args.rotate:
        general.ROTATE = True
    if args.mirror:
        general.REFLECT = True

    try:
        with open(args.input, 'r') as handle:
            pass
    except FileNotFoundError as msg:
        parser.error(msg)

    main(args.input)
