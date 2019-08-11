# imports necessários
from dataclasses import dataclass
from typing import Any

# estrutura para armazernar as peças do tipo:
# peças regulares                   - Peças R
# peças irregulares do tipo L       - Peças L
# peças combinadas (R e L ou L e L) - Peças C
@dataclass
class Peca_R:
  id_: int
  l: int
  w: int
  b: int
  rotated: bool

@dataclass
class Peca_L:
  id_:int
  l1: int
  w1: int
  l2: int
  w2: int
  b: int
  trans: bool

@dataclass
class Peca_C:
  id_: int
  l: int
  w: int
  z: int
  piece1_id: Any
  piece2_id: Any
  type_comb: str
  comb_location: str

@dataclass
class ConjuntoPecas:
  tipo: int
  dados: Any

def __init__(rotate, reflect):
  # VARIÁVEIS GLOBAIS
  ## variáveis de controle
  global ROTATE
  ROTATE = rotate
  global REFLECT
  REFLECT = reflect

  ## variáveis de descrição das peças
  # dimensões L, W da placa
  global placa_L
  global placa_W 
  placa_L, placa_W = 0, 0
  # número de peças
  global N_pecas
  global N_pecas_R
  global N_pecas_L
  global N_pecas_C
  N_pecas, N_pecas_R, N_pecas_L, N_pecas_C = 0, 0, 0, 0
  # vetores de peças regulares e irregulares
  global lista_pecas_R
  global lista_pecas_L
  global lista_pecas_C
  lista_pecas_R, lista_pecas_L, lista_pecas_C = [], [], []
  # conjunto de todas as peças
  global conju_pecas
  conju_pecas = []

  ## variável para geração do pdf
  global doc
  doc = None
