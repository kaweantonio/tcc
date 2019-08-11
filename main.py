import config.common as common
import input_output.read_data as read
import input_output.tex as tex
import draw.draw_pieces as draw_pieces
import draw.draw_pattern as draw_pattern
import cutting_algorithm.cutting as cutting

ROTATE = True
REFLECT = True

common.__init__(rotate=ROTATE, reflect=REFLECT)

file_path='./data/teste inicial.BiL'

if read.read_file(file_path=file_path):
  print('Número de peças: {0}, Número de peças R: {1}, Número de peças L: {2}, Número de peças C: {3}'.format(common.N_pecas, common.N_pecas_R, common.N_pecas_L, common.N_pecas_C))
  print('Lista de peças R: ')
  for i, peca in enumerate(common.lista_pecas_R):
    print('Peça R #{} (l: {}, w: {})'.format(i+1, peca.l, peca.w))

  print('\nLista de peças L: ')
  for i, peca in enumerate(common.lista_pecas_L):
    print('Peça L #{}-id:{} (l1: {}, w1: {}, l2: {}, w2: {})'.format(i+1, peca.id_, peca.l1, peca.w1, peca.l2, peca.w2))

  print('\nLista de peças C: ')
  for i, peca in enumerate(common.lista_pecas_C):
    print('Peça C #{} (l: {}, w: {}, id1: {}, id2: {}, z={}, type_comb: {}, comb_location: {})'.format(i+1, peca.l, peca.w, peca.piece1_id, peca.piece2_id, peca.z, peca.type_comb, peca.comb_location))
  
  print('\nDimensão da placa:', common.placa_L, 'x', common.placa_W)

  tex.preparation()
  draw_pieces.draw_pieces()
  cutting.cutting()
  tex.close_document()
  tex.generate_pdf()
