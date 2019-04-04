# imports necessários
from dataclasses import dataclass

# estrutura para armazernar as peças
@dataclass
class PecaRegular:
  l: int
  w: int
  b: int

@dataclass
class PecaL:
  l1: int
  w1: int
  l2: int
  w2: int
  b: int

# VARIÁVEIS GLOBAIS
# dimensões L, W da placa
placa_L, placa_W = 0, 0
# número de peças
N_pecas = 0

# leitura do arquivo
with open('teste inicial.BiL') as f:
  # tamanho da placa
  linha = f.readline().split()
  placa_L, placa_W = (int(x) for x in linha)

  # número de peças
  linha = f.readline()
  N_pecas = int(linha)
  r, l = 0, 0
  for i in range(N_pecas):
    linha = [int(x) for x in (f.readline().split())]
  
    # verifica se a peça é regular ou do tipo-L
    if linha[0] == 0: # peça do tipo L
      l += 1
      pass
    else: # peça regular
      r += 1
      pass
