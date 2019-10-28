from typing import Tuple

from csp.config import general
from csp.knapsack.helpers import base

from loguru import logger

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
        self.strips_solution_value = dict()
        self.solution = None
        self.solution_value = None
        self.solution_without_transform = None
        self.solution_strips = None
        self.solution_strips_pieces = None
        self.solution_strips_w = None

    def get_solution(self) -> Tuple[list, int]:
        return self.solution, self.solution_value
    
    def solve(self):
        logger.info("Gerando faixas")
        self._generate_strips()

        logger.info("Inicializando processo de solução de cada faixa como um problema da mochila")
        self._solve_strips()

        logger.info("Resolvendo o último problema da mochila")
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

        logger.debug("Tamanhos de faixa possíveis: {}".format(unique_w))

        for i in unique_w:
            logger.debug("Gerando faixa de tamanho {}".format(i))
            strips[i] = []

            for piece in pieces:
                if piece.type_ == general.IRREGULAR:
                    w = piece.dimensions.w1
                else:
                    w = piece.dimensions.w

                if w <= i:
                    strips[i].append(piece.id_)
            
            self.strips_area[i] = L * i

            logger.debug("Faixa gerada: {}".format(strips[i]))
            logger.debug("Área ocupada da faixa: {}".format(self.strips_area[i]))
        
        self.strips = strips
        self.len_strips = len(strips)

        if not general.DEBUG:
            logger.info("Faixas geradas")
            for i, strip in enumerate(strips): 
                logger.info(" Faixa {}: {}".format(i, strip))

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

            solution, solution_value = self.linear_model(len(pieces_id_on_strip),
                                                   dummy_variables,
                                                   A,
                                                   b,
                                                   c,
                                                   constraint_types, i, sense='maximize')
            i += 1

            logger.debug("Faixa: {}, solução: {}, perda: {}".format(self.strips[key], solution, self.strips_area[key]-solution_value))
            logger.debug("Dados do problema - Matrix A: {}, vetor b: {}, vetor de constantes: {}".format(A,b,c))
            self.strips_solution[key] = solution
            self.strips_solution_value[key] = solution_value
            
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
                c.append(self.strips_solution_value[key])

        A.append(aux)
        b.append(W)
        constraint_types.append(default_constraint_types['LESS_THAN_OR_EQUAL'])

        logger.debug("Dados do problema - Matrix A: {}, vetor b: {}, vetor de constantes: {}".format(A,b,c))
        solution, solution_value = self.linear_model(len(aux),
                                               dummy_variables,
                                               A,
                                               b,
                                               c,
                                               constraint_types, 'final', sense='maximize')

        logger.debug("Solução encontrada: z*={1}\n Solução antes da transformação: {0}".format(solution, solution_value))

        self.solution_without_transform = solution

        self._strips_solution(solution)

        logger.debug("Iniciando transformação da solução")
        solution = self._transform_solution(solution)

        logger.debug("Solução depois da transformação: {}".format(solution))
        
        self.solution = solution
        self.solution_value = solution_value

    def _strips_solution(self, solution):
        self.solution_strips, self.solution_strips_pieces, self.solution_strips_w = [], [], []
        
        key_strips = list(self.strips.keys())
        
        for i, result in enumerate(solution):
            if result == 0.0:
                continue
            
            for _ in range(int(result)):
                self.solution_strips.append(self.strips_solution[key_strips[i]])
                self.solution_strips_pieces.append(self.strips[key_strips[i]])
                self.solution_strips_w.append(key_strips[i])

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
                        # print("combine_LL", value, strip_solution[i], key_strips[index])
                    elif combination_type == general.COMBINE_LR:
                        real_solution[pieces[piece].combination.piece1_id] += value * strip_solution[i]
                        real_solution[pieces[piece].combination.piece2_id] += value * strip_solution[i]
                        # print("combine_LR", value, strip_solution[i], key_strips[index])

        return real_solution

class RestrictedBidimensionalKnapsack(base.Base):
    def __init__(self):
        self.solution = None
        self.solution_value = 0
        self.solution_strips = []
        self.solution_strips_with_transform = []
        self.solution_strips_w = []
        self.solution_strips_pieces = []
        self.pieces_demand = None
    
    def get_solution(self):
        return self.solution, self.solution_value

    def solve(self):
        logger.debug("Preparando variáveis para resolução do problema restrito")
        self._pre_solve()
        logger.debug("Iniciando resolução")
        self._solve()
    
    def _pre_solve(self):
        self.pieces_demand = dict()

        for piece in general.pieces:
            id_ = piece.id_
            demand = piece.b
            type_ = piece.type_
            rotated = piece.rotated

            if type_ != general.COMBINED and not rotated:
                self.pieces_demand[id_] = demand
            
        self.solution = [0] * len(self.pieces_demand)

        logger.debug("Demandas a serem atendidas: {}".format(self.pieces_demand))

    def _solve(self):
        L, W = general.plate.L, general.plate.W

        dimension = W

        logger.debug("Iniciando solução. Entrando no loop")
        while True:
            logger.debug('Dimensão restante a ser alocada: {}'.format(dimension))
            logger.debug('Demandas restantes a serem atendidas: {}'.format(self.pieces_demand))

            logger.debug("Gerando faixas conforme informações de Dimensão e Demandas")
            strips = self._generate_strips(dimension)

            if not strips:
                logger.debug("Nenhuma faixa nova criada. Saindo do loop")
                break

            logger.debug("Solucionando faixas encontradas")
            strips_solution, strips_solution_value = self._solve_strips(strips)

            logger.debug("Selecionando melhor faixa")
            best_strip_solution, best_strip_solution_value, best_strip_solution_key = self._select_best_strip(strips_solution, strips_solution_value)
            
            logger.debug("Alocando melhor faixa na solução final")
            self._set_solution(best_strip_solution_key, strips[best_strip_solution_key], best_strip_solution, best_strip_solution_value)

            dimension -= best_strip_solution_key
            
            # input()
        
        logger.debug("Solução: {}".format(self.solution))
        logger.debug("Solução das faixas: {}".format(self.solution_strips))
        logger.debug("Solução das faixas sem transformação: {}".format(self.solution_strips_with_transform))
        logger.debug("Tamanho das faixas na solução final {}".format(self.solution_strips_w))
        logger.debug("Peças em cada faixa da solução final: {}".format(self.solution_strips_pieces))
        logger.debug("Valor final da solução: {}".format(self.solution_value))

    def _generate_strips(self, dimension):
        pieces = general.pieces
        strips = dict()
        
        unique_w = []

        for piece in pieces:
            if piece.type_ == general.IRREGULAR:
                w = piece.dimensions.w1
            else:
                w = piece.dimensions.w
            
            if w > dimension:
                continue

            if w not in unique_w:
                unique_w.append(w)
        
        unique_w.sort()

        logger.debug("Tamanhos de faixa possíveis encontradas: {}".format(unique_w))

        for i in unique_w:
            aux = []

            for piece in pieces:
                if piece.type_ == general.IRREGULAR:
                    w = piece.dimensions.w1
                else:
                    w = piece.dimensions.w

                if w <= i:
                    aux.append(piece.id_)
            
            if len(aux) > 0:
                strips[i] = aux

        logger.debug("Faixas criadas:")
        for i, strip in enumerate(strips):
            logger.debug("Faixa {}: {}".format(i, strip))
                    
        return strips

    def _solve_strips(self, strips):
        # create linear problem for each strip
        L, W = general.plate.L, general.plate.W
        pieces = general.pieces
        strips_solution, strips_solution_value = dict(), dict()
        i = 1
        for key in strips.keys():
            A, b, c = [], [], []
            dummy_variables = []
            constraint_types = []

            pieces_id_on_strip = strips[key]

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

            ids_to_ignore = []
            for id in pieces_id_on_strip:
                piece = pieces[id]
                if piece.type_ == general.COMBINED:
                    piece1_id = piece.combination.piece1_id
                    piece2_id = piece.combination.piece2_id

                    if piece1_id not in ids_to_ignore:
                        ids_to_ignore.append(piece1_id)
                    if piece2_id not in ids_to_ignore:
                        ids_to_ignore.append(piece2_id)
                elif id in general.original_ids_to_rotated_ids.keys():
                    ids_to_ignore.append(general.original_ids_to_rotated_ids[id])
                
            logger.debug('ids_to_ignore: {}'.format(ids_to_ignore))
            len_pieces_id_on_strip = len(pieces_id_on_strip)
            
            skip_piece = False
            # adds demand constrains for all pieces
            for index, id in enumerate(pieces_id_on_strip):
                demand = 0
                if skip_piece:
                    skip_piece = False
                    continue

                has_contraint = False
                aux = [0] * general.num_pieces

                piece = pieces[id]

                if piece.type_ == general.COMBINED:
                    piece1_id = piece.combination.piece1_id
                    piece2_id = piece.combination.piece2_id
                    type_ = piece.combination.type_

                    if type_ == general.COMBINE_LL:
                        aux[piece1_id] = 1
                        aux[id] = 2
                        demand = self.pieces_demand[piece1_id]
                    elif type_ == general.COMBINE_LR:
                        aux[piece1_id] = 1
                        aux[piece2_id] = 1
                        aux[id] = 2

                        demand = self.pieces_demand[piece.combination.piece_id_demand]

                    if index+1 < len_pieces_id_on_strip:
                        next_piece = pieces[pieces_id_on_strip[(index+1)]]
                        np_type_ = next_piece.combination.type_

                        if next_piece.type_ == general.COMBINED:
                            np_piece1_id = next_piece.combination.piece1_id
                            np_piece2_id = next_piece.combination.piece2_id
                            if type_ == general.COMBINE_LL == np_type_:
                                if np_piece1_id == piece1_id:
                                    aux[next_piece.id_] = 2
                                    skip_piece = True
                            elif type_ == general.COMBINE_LR == np_type_:
                                if np_piece1_id == piece1_id:
                                    if np_piece2_id in general.original_ids_to_rotated_ids.keys():
                                        if general.original_ids_to_rotated_ids[np_piece2_id] in pieces_id_on_strip:
                                            aux[general.original_ids_to_rotated_ids[np_piece2_id]] = 1
                                    elif np_piece2_id in general.rotated_ids_to_original_ids.keys():
                                        aux[general.rotated_ids_to_original_ids[np_piece2_id]] = 1

                    has_contraint = True
                elif id not in ids_to_ignore:
                    aux[id] = 1

                    if index+1 < len_pieces_id_on_strip:
                        next_piece = pieces[pieces_id_on_strip[(index+1)]]
                        np_id_ = next_piece.id_
                        if id in general.original_ids_to_rotated_ids.keys() and general.original_ids_to_rotated_ids[id] == np_id_:
                            aux[np_id_] = 1
                    
                    if not pieces[id].rotated:
                        demand = self.pieces_demand[id]
                    else:
                        demand = self.pieces_demand[general.rotated_ids_to_original_ids[id]]
                    has_contraint = True

                aux_strips = []

                for id in pieces_id_on_strip:
                        aux_strips.append(aux[id])
                
                demand = demand if demand > 0 else 0
                if has_contraint and demand > 0:
                    A.append(aux_strips)
                    b.append(demand)
                    constraint_types.append(default_constraint_types['GREATER_THAN_OR_EQUAL'])

            solution, solution_value = self.linear_model(len(pieces_id_on_strip),
                                                   dummy_variables,
                                                   A,
                                                   b,
                                                   c,
                                                   constraint_types, i, sense='maximize')
            i += 1

            logger.debug("Dados do problema - Matrix A: {}, vetor b: {}, vetor de constantes: {}".format(A,b,c))
            if solution is None:
                logger.debug('Faixa: {}'.format(strips[key]))
                return strips_solution, strips_solution_value
            
            #print(A,b,c)
            logger.debug("Faixa: {}, solução: {}, z*: {}".format(strips[key], solution, solution_value))

            strips_solution[key], strips_solution_value[key] = solution, solution_value
        
        return strips_solution, strips_solution_value 

    def _select_best_strip(self, strips_solution, strips_solution_value):
        best_strip_solution_value = -1
        best_strip_solution = None
        best_strip_key = None

        for key in strips_solution_value.keys():
            strip = strips_solution[key]
            value = strips_solution_value[key]

            if value > best_strip_solution_value:
                best_strip_solution_value = value
                best_strip_solution = strip
                best_strip_key = key
            elif value == best_strip_solution_value:
                if sum(strip) > sum(best_strip_solution):
                    best_strip_solution = strip
                    best_strip_key = key
        
        return best_strip_solution, best_strip_solution_value, best_strip_key

    def _transform_solution(self, strip_pieces, solution) -> list:
        pieces = general.pieces

        real_solution = [0] * (general.num_pieces_without_combined_pieces)

        for i, piece in enumerate(strip_pieces):
            if pieces[piece].type_ != general.COMBINED:
                if pieces[piece].rotated:
                    real_solution[general.rotated_ids_to_original_ids[piece]] += solution[i]
                else:
                    real_solution[piece] += solution[i]
            else:
                combination_type = pieces[piece].combination.type_
                if combination_type == general.COMBINE_LL:
                    real_solution[pieces[piece].combination.piece1_id] += 2 * solution[i]
                    # print("combine_LL", solution[i])
                elif combination_type == general.COMBINE_LR:
                    real_solution[pieces[piece].combination.piece1_id] += solution[i]
                    real_solution[pieces[piece].combination.piece2_id] += solution[i]
                    # print("combine_LR", solution[i])

        

        return [real_solution[i] for i in self.pieces_demand.keys()]

    def _set_solution(self, strip_dimension, strip_pieces, strip_solution, strip_value):
        self.solution_strips_w.append(strip_dimension)
        self.solution_strips_with_transform.append(self._transform_solution(strip_pieces, strip_solution))
        self.solution_strips.append(strip_solution)
        self.solution_strips_pieces.append(strip_pieces)
        self.solution_value += strip_value
        
        # pieces = general.pieces
        # for index, id in enumerate(strip_pieces):
        #     piece = pieces[id]

        #     if piece.type_ == general.COMBINED:
        #         piece1_id = piece.combination.piece1_id
        #         piece2_id = piece.combination.piece2_id

        #         if piece.combination.type_ == general.COMBINE_LL:
        #             self.pieces_demand[piece1_id] -= 2 * strip_solution[index]

        #         elif piece.combination.type_ == general.COMBINE_LR:
        #             self.pieces_demand[piece1_id] -= strip_solution[index]
        #             self.pieces_demand[piece2_id] -= strip_solution[index]
        #     else:
        #         self.pieces_demand[id] -= strip_solution[index]

        strip_solution = self.solution_strips_with_transform[-1]
        # print(self.solution_strips[-1])
        # print(strip_solution)
        for index, key in enumerate(self.pieces_demand.keys()):
            self.pieces_demand[key] -= strip_solution[index]
            self.solution[index] += strip_solution[index]
