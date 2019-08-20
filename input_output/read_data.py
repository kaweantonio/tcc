import config.common as common

def calc_z(L, W, piece1, piece2):
  piece1_area = (piece1.l1 * piece1.w2) + ((piece1.w1 - piece1.w2) * piece1.l2)
  print(type(piece2))

  if type(piece2) == common.Peca_L:
    piece2_area = (piece2.l1 * piece2.w2) + ((piece2.w1 - piece2.w2) * piece2.l2)
  else:
    piece2_area = piece2.l * piece2.w
  
  z = (L * W) - (piece1_area + piece2_area)

  return z

def combine_L_pieces():
  # combine L pieces with their mirrored pieces
  for piece in common.lista_pecas_L:
    # combine piece by 'horizontal'
    new_l = piece.l1 + piece.l2
    new_w = 2 * piece.w2 if piece.w1 - piece.w2 < piece.w2 else (piece.w1)
    new_piece = common.Peca_C(-1, new_l, new_w, calc_z(new_l, new_w, piece, piece), piece.id_, piece.id_, 'L-L-mirrored', 'l1')
    common.lista_pecas_C.append(new_piece)
    common.conju_pecas.append(common.ConjuntoPecas(2, common.lista_pecas_C[-1]))
    common.N_pecas_C += 1

    # combine piece by 'vertical'
    new_l = 2 * piece.l2 if piece.l1 - piece.l2 < piece.l2 else piece.l1
    new_w = piece.w1 + piece.w2   
    new_piece = common.Peca_C(-1, new_l, new_w, calc_z(new_l, new_w, piece, piece), piece.id_, piece.id_, 'L-L-mirrored', 'l2')
    common.lista_pecas_C.append(new_piece)
    common.conju_pecas.append(common.ConjuntoPecas(2, common.lista_pecas_C[-1]))
    common.N_pecas_C += 1

# leitura do arquivo
def read_file(file_path=None):
  if file_path is None:
    return 0

  with open(file_path) as f:
    # tamanho da placa
    linha = f.readline().split()
    common.placa_L, common.placa_W = (int(x) for x in linha)

    # número de peças
    linha = f.readline()
    common.N_pecas = int(linha)

    pecas_R_rotated = []
    
    id_ = 0
    for _ in range(common.N_pecas):
      linha = [int(x) for x in (f.readline().split())]
    
      # verifica se a peça é regular ou do tipo-L
      if linha[0] == 0: # peça do tipo L
        trans = False

        # all L-pieces need to have L1 greater than W1,
        # if not, "rotate" the piece so that W1 becomes the new L1
        # finally, "reflect" the piece
        if linha[1] < linha[2]:
          aux = linha[1]
          linha[1] = linha[2]
          linha[2] = aux

          aux = linha[3]
          linha[3] = linha[4]
          linha[4] = aux
          trans = True
        common.lista_pecas_L.append(common.Peca_L(id_, linha[1], linha[2], linha[3], linha[4], linha[5], trans))
        common.conju_pecas.append(common.ConjuntoPecas(0, common.lista_pecas_L[-1]))
        common.N_pecas_L += 1
      else: # peça regular
        common.lista_pecas_R.append(common.Peca_R(id_, linha[0], linha[1], linha[2], False))
        common.conju_pecas.append(common.ConjuntoPecas(1, common.lista_pecas_R[-1]))
        common.N_pecas_R += 1

        if common.ROTATE:
          id_ += 1
          common.lista_pecas_R.append(common.Peca_R(id_, linha[1], linha[0], linha[2], True))
          common.conju_pecas.append(common.ConjuntoPecas(1, common.lista_pecas_R[-1]))
          common.N_pecas_R += 1
      id_ += 1
    
    combine_L_pieces()

    return 1
