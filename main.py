import config.common as common
import read.read_data as read

ROTATE = False
REFLECT = False

common.__init__(rotate=ROTATE, reflect=REFLECT)

file_path='./data/teste inicial.BiL'

if read.read_file(file_path=file_path):
  print('Número de peças: {0}, Número de peças R: {1}, Número de peças L: {2}'.format(common.N_pecas, common.N_pecas_R, common.N_pecas_L))
  print('Lista de peças R: ')
  for i, peca in enumerate(common.lista_pecas_R):
    print('Peça R #{} (l: {}, w: {})'.format(i+1, peca.l, peca.w))

  print('\nLista de peças L: ')
  for i, peca in enumerate(common.lista_pecas_L):
    print('Peça L #{} (l1: {}, w1: {}, l2: {}, w2:{})'.format(i+1, peca.l1, peca.w1, peca.l2, peca.w2))
  
  print('\nDimensão da placa: ', common.placa_L, 'x', common.placa_W)

  draw.generate_pdf()
