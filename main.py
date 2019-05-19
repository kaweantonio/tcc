import config.common as common
import read.read_data as read
import draw.draw_pdf as draw

common.__init__()

file_path='./data/teste inicial.BiL'

if read.read_file(file_path=file_path):
  print('Número de peças: {0}, Número de peças R: {1}, Número de peças L: {2}'.format(common.N_pecas, common.N_pecas_R, common.N_pecas_L))
  print('Lista de peças R: ', common.lista_pecas_R)
  print('Lista de peças L: ', common.lista_pecas_L)
  print('Dimensão da placa: ', common.placa_L, 'x', common.placa_W)

  draw.generate_pdf()
