from os import sep
from os import path
from typing import Tuple
from datetime import datetime

from csp.config import general
from csp.knapsack.knapsack import BidimensionalKnapsack, RestrictedBidimensionalKnapsack
from csp.helpers import readfile


class cuttingStockProblem():

    def __init__(self, file_path):
        self.file_path = file_path
        self.directory_path = path.dirname(self.file_path)
        self.file_name = path.splitext(path.basename(self.file_path))[0]   
        self.solution = None
        self.solution_value = None
        self.solution_value_percentage = None

        readfile.read(self.file_path)

        self._combine_L_pieces()
        self._combine_L_R_pieces()

    def _combine_L_pieces(self):
        # combine L pieces with their mirrored pieces
        for piece in general.pieces_L:
            # combine piece by 'horizontal'
            new_l = piece.dimensions.l1 + piece.dimensions.l2
            new_w = 2 * piece.dimensions.w2 if piece.dimensions.w1 - piece.dimensions.w2 < piece.dimensions.w2 else (piece.dimensions.w1)
            b = piece.b
            dimensions = general.Dimensions(new_l, new_w)
            combination = general.Combination(
                piece.id_, piece.id_, general.COMBINE_LL, general.HORIZONTAL, piece.id_)
            new_piece = general.Piece(
                general.COMBINED, dimensions, b, False, False, combination)

            general.pieces.append(new_piece)
            general.pieces_C.append(general.pieces[-1])
            general.num_pieces_C += 1
            general.num_pieces += 1

            # combine piece by 'vertical'
            new_l = 2 * piece.dimensions.l2 if piece.dimensions.l1 - piece.dimensions.l2 < piece.dimensions.l2 else piece.dimensions.l1
            new_w = piece.dimensions.w1 + piece.dimensions.w2
            dimensions = general.Dimensions(new_l, new_w)
            combination = general.Combination(
                piece.id_, piece.id_, general.COMBINE_LL, general.VERTICAL, piece.id_)
            new_piece = general.Piece(
                general.COMBINED, dimensions, b, False, False, combination)

            general.pieces.append(new_piece)
            general.pieces_C.append(general.pieces[-1])
            general.num_pieces_C += 1
            general.num_pieces += 1

    def _combine_L_R_pieces(self, alfa=0.30):
        for piece_L in general.pieces_L:
            
            # determine region to combine pieces:
            # - 'vertical' if 'l2' > (l1-l2)
            # - otherwise, combine by 'horizontal'
            if piece_L.dimensions.l2 > (piece_L.dimensions.l1 - piece_L.dimensions.l2):
                for piece_R in general.pieces_R:
                    new_l = piece_L.dimensions.l1 if piece_R.dimensions.l <= piece_L.dimensions.l1 else piece_R.dimensions.l
                    new_w = piece_L.dimensions.w1 + piece_R.dimensions.w

                    if piece_L.b < piece_R.b:
                        b = piece_L.b
                        piece_id_demand = piece_L.id_
                    else:
                        b = piece_R.b
                        piece_id_demand = piece_R.id_

                    area = new_l * new_w
                    loss = area - (piece_L.area + piece_R.area)
                    if loss <= area * alfa:
                        dimensions = general.Dimensions(new_l, new_w)
                        combination = general.Combination(
                            piece_L.id_, piece_R.id_, general.COMBINE_LR, general.VERTICAL, piece_id_demand
                        )

                        new_piece = general.Piece(
                            general.COMBINED, dimensions, b, False, False, combination
                        )

                        general.pieces.append(new_piece)
                        general.pieces_C.append(general.pieces[-1])
                        general.num_pieces_C += 1
                        general.num_pieces += 1
            else:
                for piece_R in general.pieces_R:
                    new_l = piece_L.dimensions.l1 if piece_R.dimensions.l <= (piece_L.dimensions.l1-piece_L.dimensions.l2) else piece_L.dimensions.l2 + piece_R.dimensions.l
                    new_w = piece_L.dimensions.w1 if piece_R.dimensions.w <= (piece_L.dimensions.w1-piece_L.dimensions.w2) else piece_L.dimensions.w2 + piece_R.dimensions.w
                    
                    if piece_L.b < piece_R.b:
                        b = piece_L.b
                        piece_id_demand = piece_L.id_
                    else:
                        b = piece_R.b
                        piece_id_demand = piece_R.id_

                    area = new_l * new_w
                    print(area, new_l, new_w)
                    loss = area - (piece_L.area + piece_R.area)
                    if loss <= area * alfa:
                        dimensions = general.Dimensions(new_l, new_w)
                        combination = general.Combination(
                            piece_L.id_, piece_R.id_, general.COMBINE_LR, general.HORIZONTAL, piece_id_demand
                        )

                        new_piece = general.Piece(
                            general.COMBINED, dimensions, b, False, False, combination
                        )
                        general.pieces.append(new_piece)
                        general.pieces_C.append(general.pieces[-1])
                        general.num_pieces_C += 1
                        general.num_pieces += 1
    
    def _solve(self):
        if general.RESTRICTED:
            knapsack = RestrictedBidimensionalKnapsack()
        else:
            knapsack = BidimensionalKnapsack()
        knapsack.solve()

        self.solution = knapsack.solution
        self.solution_value = knapsack.solution_value
        self.solution_value_percentage = (general.plate.L * general.plate.W) - self.solution_value

    def _generate_dat_file(self):
        file_name = self.directory_path + sep + self.file_name + '.dat'

        datetime_str = datetime.now().strftime("%a, %c")
        
        with open(file_name, 'w') as handle:
            handle.write('Solution for problem {0} generated at {1}'.format(file_name, datetime_str))

    def get_solution(self) -> Tuple[list, int]:
        if self.solution is None:
            self._solve()
            # self._generate_dat_file()

        return self.solution, self.solution_value

    def print_final_solution(self):
        pass
