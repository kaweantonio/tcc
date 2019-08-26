from config import general
import input_output.tex as tex

x, y = 0, 0

def draw_piece_R(id_, dimensions):
  global x,y
  x1 = x+dimensions.l*.10
  y1 = y-dimensions.w*.10
  tex.write(
    '\\filldraw[color=black!150, fill=green!35, thin]' \
    '('+str(x)+','+str(y)+') rectangle ('+str(x1)+','+str(y1)+') node [right, pos=0.5] {'+str(id_)+'};\n'
  )

  y = y1 - 0.5

def draw_piece_L(id_, dimensions):
  global x,y
  x1 = dimensions.l1*.10
  x2 = dimensions.l2*.10
  y1 = -dimensions.w1*.10
  y2 = -dimensions.w2*.10
  tex.write(
    '\\filldraw[color=black!150, fill=green!35, thin]' \
    '('+str(x)+','+str(y)+') -- ' \
    '++('+str(x2)+',0) -- ' \
    '++(0,'+str(y1-y2)+') -- ' \
    '++('+str(x1-x2)+',0) -- ' \
    '++(0,'+str(y2)+') -- ' \
    '++('+str(-x1)+',0) -- ' \
    '++(0,'+str(-y1)+') node [right, pos=0.5] {'+str(id_)+'};\n'
  )

  y = y - dimensions.w1*.10 - 0.5

def draw_reflected_piece_L(id_, dimensions):
  global x,y
  x1 = dimensions.l1*.10
  x2 = dimensions.l2*.10
  y1 = -dimensions.w1*.10
  y2 = -dimensions.w2*.10
  tex.write(
    '\\filldraw[color=black!150, fill=green!35, thin]' \
    '('+str(x)+','+str(y)+') -- ' \
    '++('+str(x1)+',0) -- ' \
    '++(0,'+str(y1)+') -- ' \
    '++('+str(-x2)+',0) -- ' \
    '++(0,'+str(y2-y1)+') -- ' \
    '++('+str(x2-x1)+',0) -- ' \
    '++(0,'+str(-y2)+') node [right, pos=0.5] {'+str(id_)+'};\n'
  )

  y = y - dimensions.w1*.10 - 0.5

def draw_piece_C(pieceC):
  global x,y
  piece1_id = pieceC.combination.piece1_id
  piece2_id = pieceC.combination.piece2_id
  
  piece1 = general.pieces[piece1_id]
  piece2 = general.pieces[piece2_id]

  location = pieceC.combination.location

  if location == general.HORIZONTAL:
    aux_x = x
    aux_y = y
    # x += pieceC.l*0.10

    if pieceC.dimensions.w > piece1.dimensions.w1:
      y -= 0.1 * piece1.dimensions.w2

    l1 = piece1.dimensions.l1
    l2 = piece1.dimensions.l2
    w1 = piece1.dimensions.w1
    w2 = piece1.dimensions.w2

    x1 = l1*.10
    x2 = l2*.10
    y1 = -w1*.10
    y2 = -w2*.10
    tex.write(
      '\\filldraw[color=black!150, fill=green!35, thin]' \
      '('+str(x)+','+str(y)+') -- ' \
      '++('+str(x2)+',0) -- ' \
      '++(0,'+str(y1-y2)+') -- ' \
      '++('+str(x1-x2)+',0) -- ' \
      '++(0,'+str(y2)+') -- ' \
      '++('+str(-x1)+',0) -- ' \
      '++(0,'+str(-y1)+') node [right, pos=0.5] {'+str(piece1_id)+'};\n'
    )

    l1 = piece2.dimensions.l1
    l2 = piece2.dimensions.l2
    w1 = piece2.dimensions.w1
    w2 = piece2.dimensions.w2

    x += l2 * 0.10

    if pieceC.dimensions.w > piece1.dimensions.w1:
      y += (2 * piece1.dimensions.w2 - piece1.dimensions.w1) * 0.10

    x1 = l1*.10
    x2 = l2*.10
    y1 = -w1*.10
    y2 = -w2*.10
    tex.write(
      '\\filldraw[color=black!150, fill=green!35, thin]' \
      '('+str(x)+','+str(y)+') -- ' \
      '++('+str(x1)+',0) -- ' \
      '++(0,'+str(y1)+') -- ' \
      '++('+str(-x2)+',0) -- ' \
      '++(0,'+str(y2-y1)+') -- ' \
      '++('+str(x2-x1)+',0) -- ' \
      '++(0,'+str(-y2)+') node [right, pos=0.5] {'+str(piece2_id)+'};\n'
    )
    x = aux_x
  else:
    aux_x = x
    aux_y = y
    
    y -= 0.5

    l1 = piece1.dimensions.l1
    l2 = piece1.dimensions.l2
    w1 = piece1.dimensions.w1
    w2 = piece1.dimensions.w2

    x1 = l1*.10
    x2 = l2*.10
    y1 = -w1*.10
    y2 = -w2*.10
    tex.write(
      '\\filldraw[color=black!150, fill=green!35, thin]' \
      '('+str(x)+','+str(y)+') -- ' \
      '++('+str(x2)+',0) -- ' \
      '++(0,'+str(y1-y2)+') -- ' \
      '++('+str(x1-x2)+',0) -- ' \
      '++(0,'+str(y2)+') -- ' \
      '++('+str(-x1)+',0) -- ' \
      '++(0,'+str(-y1)+') node [right, pos=0.5] {'+str(piece1_id)+'};\n'
    )

    l1 = piece2.dimensions.l1
    l2 = piece2.dimensions.l2
    w1 = piece2.dimensions.w1
    w2 = piece2.dimensions.w2

    y += w2 * 0.10

    if pieceC.dimensions.l > piece1.dimensions.l1:
      x += (2 * piece1.dimensions.l2 - piece1.dimensions.l1) * 0.10

    x1 = l1*.10
    x2 = l2*.10
    y1 = -w1*.10
    y2 = -w2*.10
    tex.write(
      '\\filldraw[color=black!150, fill=green!35, thin]' \
      '('+str(x)+','+str(y)+') -- ' \
      '++('+str(x1)+',0) -- ' \
      '++(0,'+str(y1)+') -- ' \
      '++('+str(-x2)+',0) -- ' \
      '++(0,'+str(y2-y1)+') -- ' \
      '++('+str(x2-x1)+',0) -- ' \
      '++(0,'+str(-y2)+') node [right, pos=0.5] {'+str(piece2_id)+'};\n'
    )
    x = aux_x
    y = aux_y

#  y = aux_y

  y = y - pieceC.dimensions.w *.10 - 0.5

def draw_pieces():
  tex.open_tikz()
  for _ in range(0, general.num_pieces_R):
    piece_R = general.pieces_R[_]
    draw_piece_R(piece_R.id_, piece_R.dimensions)
  tex.close_tikz()

  tex.new_page()
  tex.open_tikz()
  for _ in range(0, general.num_pieces_L):
    piece_L = general.pieces_L[_]
    draw_piece_L(piece_L.id_, piece_L.dimensions)
  tex.close_tikz()

  tex.new_page()
  tex.open_tikz()
  for _ in range(0, general.num_pieces_C):
    piece_C = general.pieces_C[_]
    draw_piece_C(piece_C)

  tex.close_tikz()

  tex.new_page()

