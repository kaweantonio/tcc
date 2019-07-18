import config.common as common

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
        common.lista_pecas_L.append(common.Peca_L(linha[1], linha[2], linha[3], linha[4], linha[5], trans))
        common.conju_pecas.append(common.ConjuntoPecas(0, common.lista_pecas_L[-1]))
        common.N_pecas_L += 1
      else: # peça regular
        common.lista_pecas_R.append(common.Peca_R(linha[0], linha[1], linha[2], False))
        common.conju_pecas.append(common.ConjuntoPecas(1, common.lista_pecas_R[-1]))
        common.N_pecas_R += 1

        pecas_R_rotated.append(common.Peca_R(linha[1], linha[0], linha[2], True))

    common.lista_pecas_R.extend(pecas_R_rotated)
    common.N_pecas_R += len(pecas_R_rotated)

    return 1
