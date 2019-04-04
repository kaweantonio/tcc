# imports necessários
from dataclasses import dataclass
from typing import Any

# estrutura para armazernar as peças do tipo:
# peças regulares                   - Peças R
# peças irregulares do tipo L       - Peças L
# peças combinadas (R e L ou L e L) - Peças C
@dataclass
class Peca_R:
  l: int
  w: int
  b: int

@dataclass
class Peca_L:
  l1: int
  w1: int
  l2: int
  w2: int
  b: int

@dataclass
class Peca_C:
  pass

@dataclass
class ConjuntoPecas:
  tipo: int
  dados: Any

# VARIÁVEIS GLOBAIS
# dimensões L, W da placa
placa_L, placa_W = 0, 0
# número de peças
N_pecas = 0
# vetores de peças regulares e irregulares
lista_pecas_R, lista_pecas_L = [], []
# conjunto de todas as peças
conju_pecas = []

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
      lista_pecas_L.append(Peca_L(linha[1], linha[2], linha[3], linha[4], linha[5]))
      conju_pecas.append(ConjuntoPecas(0, lista_pecas_L[-1]))
    else: # peça regular
      lista_pecas_R.append(Peca_R(linha[0], linha[1], linha[2]))
      conju_pecas.append(ConjuntoPecas(1, lista_pecas_R[-1]))

print(conju_pecas)
