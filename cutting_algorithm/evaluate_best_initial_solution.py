import config.common as common
import draw.draw_pattern as draw_pattern
import input_output.tex as tex

from cutting_algorithm.initial_solution import initial_solution_peca_R as init_solu_peca_R
from cutting_algorithm.initial_solution import initial_solution_peca_R_rotated as init_solu_peca_R_rotated
from cutting_algorithm.initial_solution import initial_solution_peca_L as init_solu_peca_L

def main():
  piece_R, lost_R = init_solu_peca_R.initial_solution()
  piece_R_rotated, lost_R_rotated = init_solu_peca_R_rotated.initial_solution()
  piece_L, lost_L = init_solu_peca_L.initial_solution()
  
  print(piece_R, lost_R)
  print(piece_R_rotated, lost_R_rotated)
  print(piece_L, lost_L)

  draw_pattern.initial_pattern(piece_L, 'L', lost_L)
