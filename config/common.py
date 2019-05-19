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

def __init__():
  # VARIÁVEIS GLOBAIS
  # dimensões L, W da placa
  global placa_L
  global placa_W 
  placa_L, placa_W = 0, 0
  # número de peças
  global N_pecas
  global N_pecas_R
  global N_pecas_L 
  N_pecas, N_pecas_R, N_pecas_L = 0, 0, 0
  # vetores de peças regulares e irregulares
  global lista_pecas_R
  global lista_pecas_L
  lista_pecas_R, lista_pecas_L = [], []
  # conjunto de todas as peças
  global conju_pecas
  conju_pecas = []
