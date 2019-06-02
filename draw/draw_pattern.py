from copy import deepcopy as copy

import config.common as common
import draw.tex as tex

x, y = 0, 0

def tikz_draw_peca_R(l, w, id, x, y):
  x1 = x+l*.10
  y1 = y+w*.10
  common.doc.write(
    ' \\filldraw[color=black!150, fill=green!35, thin]' \
    '('+str(x)+','+str(y)+') rectangle ('+str(x1)+','+str(y1)+') node [pos=.5] {'+str(id)+'};\n'
  )

def tikz_draw_peca_L(l1, w1, l2, w2, id, x, y):
  x1 = l1*.10
  x2 = l2*.10
  y1 = -w1*.10
  y2 = -w2*.10
  common.doc.write(
    ' \\filldraw[color=black!150, fill=green!35, thin]' \
    '('+str(x)+','+str(y)+') -- ' \
    '++('+str(x2)+',0) -- ' \
    '++(0,'+str(y1-y2)+') -- ' \
    '++('+str(x1-x2)+',0) -- ' \
    '++(0,'+str(y2)+') -- ' \
    '++('+str(-x1)+',0) -- ' \
    '++(0,'+str(-y1)+') node [right, pos=0.5] {'+str(id)+'};\n'
  )


def draw_plate():
  global x,y
  x1 = common.placa_L * .10
  y1 = common.placa_W * .10
  
  common.doc.write(
    '\\draw[color=black!150, fill=gray!35, thin]' \
    '('+str(x)+','+str(y)+') rectangle ('+str(x1)+','+str(y1)+');\n'
  )

  y = y1

def initial_pattern(piece_index, piece_type, lost_area):
  tex.open_tikz()
  draw_plate()
  rotate = False
  piece = None
  if piece_type == 'R':
    piece = copy(common.lista_pecas_R[piece_index])
  elif piece_type == 'R_rotated':
    piece = copy(common.lista_pecas_R[piece_index])
    rotate = True
  else:
    piece = copy(common.lista_pecas_L[piece_index])
  
  if rotate:
    aux = piece.w
    piece.w = piece.l
    piece.l = aux

  # local x, y
  x = 0
  y = 0

  if piece_type != 'L':
    n = common.placa_L // piece.l
    m = common.placa_W // piece.w
    for i in range(m):
      y = i*(piece.w*.10)
      for j in range(n):
        x = j*(piece.l*.10)
        tikz_draw_peca_R(piece.l,piece.w,piece_index,x,y)
  else:
    n = common.placa_L // piece.l1
    m = common.placa_W // piece.w1
    aux1 = piece.l1*.10
    aux2 = piece.w1*.10
    for i in range(m):
      y = (i+1) * aux2 
      for j in range(n):
        x = j * aux1
        tikz_draw_peca_L(piece.l1,piece.w1,piece.l2,piece.w2,piece_index,x,y)
    
  
  tex.close_tikz()
  
