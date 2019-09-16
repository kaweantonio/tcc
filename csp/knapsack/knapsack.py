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
        self.strips_loss = dict()
        self.strips_area = dict()
        self.strips_solution = dict()
        self.strips_solution_loss = dict()
        self.solution = None
        self.solution_loss = None

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

        for key in self.strips.keys():
            A, b, c = [], [], []
            dummy_variables = []
            constraint_types = []

            pieces_id_on_strip = self.strips[key]

            aux = []

            # adds dummy variable in the objective function
            c.append(self.strips_area[key])
            # for each dummy variable is necessary to inform
            # unique id, default value and constraint type
            dummy_variables.append([0, 1, default_constraint_types['EQUAL']])

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

                c.append(-piece.area)
            
            A.append(aux)
            b.append(L)
            constraint_types.append(default_constraint_types['LESS_THAN_OR_EQUAL'])

            solution, solution_loss = self.linear_model(len(pieces_id_on_strip),
                                                   dummy_variables,
                                                   A,
                                                   b,
                                                   c,
                                                   constraint_types)
            solution.pop(0)
            self.strips_solution[key] = solution
            self.strips_solution_loss[key] = solution_loss
            
    def _solve_last_knapsack(self):
        L, W = general.plate.L, general.plate.W

        A, b, c = [], [], []
        dummy_variables = []
        constraint_types = []

        aux = []
        
        # adds plate area as dummy variable in the objective function
        c.append(L*W)
        dummy_variables.append([0, 1, default_constraint_types['EQUAL']])

        # add constraint for each strip: sum of all strips weigth (key value) in plate 
        # has to be less than or equal to plate weigth
        # also adds the area for each strip in the objective function
        for key in self.strips.keys():
            aux.append(key)
            c.append(-self.strips_area[key])

        A.append(aux)
        b.append(W)
        constraint_types.append(default_constraint_types['LESS_THAN_OR_EQUAL'])

        solution, solution_loss = self.linear_model(self.len_strips,
                                               dummy_variables,
                                               A,
                                               b,
                                               c,
                                               constraint_types)
        solution.pop(0)

        solution = self._transform_solution(solution)

        self.solution = solution
        self.solution_loss = solution_loss

    def _transform_solution(self, solution) -> list:
        pieces = general.pieces

        real_solution = [0] * (len(general.pieces_R) + len(general.pieces_L))
        
        key_strips = list(self.strips.keys())

        solution = [int(x) for x in solution]
        
        for index, value in enumerate(solution):
            if value == 0:
                continue

            strip = self.strips[key_strips[index]]
            strip_solution = self.strips_solution[key_strips[index]]

            for i, piece in enumerate(strip):
                if pieces[piece].type_ != general.COMBINED:
                    real_solution[piece] += value * strip_solution[i]
                else:
                    if pieces[piece].combination.type_ == general.COMBINE_LL:
                        real_solution[pieces[piece].combination.piece1_id] += 2 * value * strip_solution[i]
        
        return real_solution

