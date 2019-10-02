from typing import Tuple

from csp.config import general
from csp.knapsack.helpers import base

default_constraint_types = {
    'LESS_THAN_OR_EQUAL': 'L',
    'GREATER_THAN_OR_EQUAL': 'G',
    'EQUAL': 'E'
}

class BidimensionalKnapsack(base.Base):
    def __init__(self):
        
        self.len_strips = None
        self.strips = dict()
        self.strips_area = dict()
        self.strips_solution = dict()
        self.strips_solution_loss = dict()
        self.solution = None
        self.solution_loss = None
        self.solution_without_transform = None

    def get_solution(self) -> Tuple[list, int]:
        return self.solution, self.solution_loss
    
    def solve(self):
        
        self._generate_strips()

        self._solve_strips()
        self._solve_last_knapsack()

    def _generate_strips(self):
        L = general.plate.L
        pieces = general.pieces
        strips = dict()
        
        unique_w = []

        for piece in pieces:
            if piece.type_ == general.IRREGULAR:
                w = piece.dimensions.w1
            else:
                w = piece.dimensions.w
            
            if w not in unique_w:
                unique_w.append(w)
        
        unique_w.sort()

        for i in unique_w:
            strips[i] = []

            for piece in pieces:
                if piece.type_ == general.IRREGULAR:
                    w = piece.dimensions.w1
                else:
                    w = piece.dimensions.w

                if w <= i:
                    strips[i].append(piece.id_)
            
            self.strips_area[i] = L * i
        
        self.strips = strips
        self.len_strips = len(strips)

    def _solve_strips(self):
        # create linear problem for each strip
        L, W = general.plate.L, general.plate.W
        pieces = general.pieces

        i = 1
        for key in self.strips.keys():
            A, b, c = [], [], []
            dummy_variables = []
            constraint_types = []

            pieces_id_on_strip = self.strips[key]

            aux = []

            # adds first constraint: sum of all pieces length in strip
            # has to be less than or equal to plate length
            # also adds the area for each piece in the ojective function
            for id in pieces_id_on_strip:
                piece = pieces[id]

                if piece.type_ == general.IRREGULAR:
                    l = piece.dimensions.l1
                else:
                    l = piece.dimensions.l
                
                aux.append(l)

                c.append(piece.area)
            
            A.append(aux)
            b.append(L)
            constraint_types.append(default_constraint_types['LESS_THAN_OR_EQUAL'])

            solution, solution_loss = self.linear_model(len(pieces_id_on_strip),
                                                   dummy_variables,
                                                   A,
                                                   b,
                                                   c,
                                                   constraint_types, i, sense='maximize')
            i += 1

            print("Faixa: {}, solução: {}, perda: {}".format(self.strips[key], solution, self.strips_area[key]-solution_loss))
            print(A,b,c)
            self.strips_solution[key] = solution
            self.strips_solution_loss[key] = solution_loss
            
    def _solve_last_knapsack(self):
        L, W = general.plate.L, general.plate.W

        A, b, c = [], [], []
        dummy_variables = []
        constraint_types = []

        aux = []

        # add constraint for each strip: sum of all strips weigth (key value) in plate 
        # has to be less than or equal to plate weigth
        # also adds the area for each strip in the objective function
        for key in self.strips.keys():
            if self.strips_solution[key] is not None:
                aux.append(key)
                c.append(self.strips_solution_loss[key])

        A.append(aux)
        b.append(W)
        constraint_types.append(default_constraint_types['LESS_THAN_OR_EQUAL'])

        print(A, b, c)
        solution, solution_loss = self.linear_model(len(aux),
                                               dummy_variables,
                                               A,
                                               b,
                                               c,
                                               constraint_types, 0, sense='maximize')

        print(solution, solution_loss)

        self.solution_without_transform = solution

        solution = self._transform_solution(solution)   

        self.solution = solution
        self.solution_loss = solution_loss

    def _transform_solution(self, solution) -> list:
        pieces = general.pieces

        real_solution = [0] * (len(general.pieces_R) + len(general.pieces_L))
        
        key_strips = list(self.strips.keys())

        solution = [int(x) for x in solution]
        
        for index, value in enumerate(solution):
            if value == 0.0:
                continue

            strip = self.strips[key_strips[index]]
            strip_solution = self.strips_solution[key_strips[index]]

            for i, piece in enumerate(strip):
                if pieces[piece].type_ != general.COMBINED:
                    real_solution[piece] += value * strip_solution[i]
                else:
                    combination_type = pieces[piece].combination.type_
                    if combination_type == general.COMBINE_LL:
                        real_solution[pieces[piece].combination.piece1_id] += 2 * value * strip_solution[i]
                        print("combine_LL", value, strip_solution[i], key_strips[index])
                    elif combination_type == general.COMBINE_LR:
                        real_solution[pieces[piece].combination.piece1_id] += value * strip_solution[i]
                        real_solution[pieces[piece].combination.piece2_id] += value * strip_solution[i]
                        print("combine_LR", value, strip_solution[i], key_strips[index])

        return real_solution

