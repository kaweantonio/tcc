from os import path
from typing import Tuple

from csp.config import general
from csp.knapsack.knapsack import BidimensionalKnapsack
from csp.helpers import readfile


class cuttingStockProblem():

    def __init__(self, file_path):
        self.file_path = file_path
        self.directory_path = path.dirname(self.file_path)
        self.file_name = path.splitext(self.file_path)[0]        
        self.solution = None
        self.solution_loss = None

        readfile.read(self.file_path)

        self._combine_L_pieces()

    def _combine_L_pieces(self):
        # combine L pieces with their mirrored pieces
        for piece in general.pieces_L:
            # combine piece by 'horizontal'
            new_l = piece.dimensions.l1 + piece.dimensions.l2
            new_w = 2 * piece.dimensions.w2 if piece.dimensions.w1 - piece.dimensions.w2 < piece.dimensions.w2 else (piece.dimensions.w1)
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
            new_l = 2 * piece.dimensions.l2 if piece.dimensions.l1 - piece.dimensions.l2 < piece.dimensions.l2 else piece.dimensions.l1
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

    def _solve(self):
        knapsack = BidimensionalKnapsack()
        knapsack.solve()

        self.solution = knapsack.solution
        self.solution_loss = knapsack.solution_loss

    def get_solution(self) -> Tuple[list, int]:
        if self.solution is None:
            self._solve()

        return self.solution, self.solution_loss
