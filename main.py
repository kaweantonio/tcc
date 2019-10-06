import os
import argparse

from csp.config import general
from csp.helpers import tex, piece, pattern
from csp.csp import cuttingStockProblem


def main(file_path):
    problem = cuttingStockProblem(file_path)

    print('Número de peças: {0}, Número de peças R: {1}, Número de peças L: {2}, Número de peças C: {3}'.format(
        general.num_pieces, general.num_pieces_R, general.num_pieces_L, general.num_pieces_C))
    print('Lista de peças R: ')
    for piece in general.pieces_R:
        print('Peça R #{} (l: {}, w: {}, b: {}, area: {}, rotated: {}, trans: {})'.format(
            piece.id_, piece.dimensions.l, piece.dimensions.w, piece.b, piece.area, piece.rotated, piece.transformed))

    print('\nLista de peças L: ')
    for piece in general.pieces_L:
        print('Peça L #{} (l1: {}, w1: {}, l2: {}, w2: {}, b: {} area: {}, loss: {} rotated: {} transformed: {})'.format(piece.id_,
                                                                                                                         piece.dimensions.l1, piece.dimensions.w1, piece.dimensions.l2, piece.dimensions.w2, piece.b, piece.area, piece.loss, piece.rotated, piece.transformed))
    print('\nLista de peças C: ')
    for piece in general.pieces_C:
        print('Peça C #{} (l: {}, w: {}, id1: {}, id2: {}, area: {}, loss{}, b:{}, type_comb: {}, comb_location: {})'.format(piece.id_, piece.dimensions.l,
                                                                                                        piece.dimensions.w, piece.combination.piece1_id, piece.combination.piece2_id, piece.area, piece.loss, piece.b, piece.combination.type_, piece.combination.location))

    print('\nDimensão da placa:', general.plate.L, 'x', general.plate.W)

    if general.DRAW:
        tex.preparation()
        piece.draw_pieces()

    problem.get_solution()
    problem.print_final_solution()

    print(problem.solution, problem.solution_value, problem.solution_value_percentage)

    if general.DRAW:
        tex.close_document()
        tex.generate_pdf()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rotate', action='store_true', default=False, help='rotate regular pieces')
    parser.add_argument('-m', '--mirror', action='store_true', default=False, help='reflect/rotate irregular pieces in 180 degrees')
    parser.add_argument('-d', '--draw', action='store_true', default=False, help='draw pieces and solution in PDF')
    parser.add_argument('-R', '--RESTRICTED', action='store_true', default=False, help='solve the problem as a restricted problem')
    parser.add_argument('input', help='input file, BiL format')
    parser.add_argument('output', help='output file, PDF format (default: output.pdf)', default="output.pdf", nargs='?')
    

    args = parser.parse_args()

    if args.rotate:
        general.ROTATE = True
    if args.mirror:
        general.REFLECT = True
    if args.draw:
        general.DRAW = True
    if args.RESTRICTED:
        general.RESTRICTED = True

    try:
        with open(args.input, 'r') as handle:
            pass
    except FileNotFoundError as msg:
        parser.error(msg)

    main(args.input)
