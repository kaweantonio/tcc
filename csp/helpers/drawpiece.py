from loguru import logger

from csp.config import general
from csp.helpers import tex


x, y = 0, 0

def draw_piece_R(id_, dimensions):
    global x, y
    x1 = x + dimensions.l * general.factor
    y1 = y - dimensions.w * general.factor
    tex.write(
        '\\filldraw[color=black!150, fill=green!35, thin]'
        '(' + str(x) + ',' + str(y) + ') rectangle (' + str(x1) + ',' +
        str(y1) + ') node [right, pos=0.5] {' + str(id_) + '};\n'
    )

    y = y1 - 0.5


def draw_piece_L(id_, dimensions):
    global x, y
    x1 = dimensions.l1 * general.factor
    x2 = dimensions.l2 * general.factor
    y1 = -dimensions.w1 * general.factor
    y2 = -dimensions.w2 * general.factor
    tex.write(
        '\\filldraw[color=black!150, fill=green!35, thin]'
        '(' + str(x) + ',' + str(y) + ') -- '
        '++(' + str(x2) + ',0) -- '
        '++(0,' + str(y1 - y2) + ') -- '
        '++(' + str(x1 - x2) + ',0) -- '
        '++(0,' + str(y2) + ') -- '
        '++(' + str(-x1) + ',0) -- '
        '++(0,' + str(-y1) + ') node [right, pos=0.5] {' + str(id_) + '};\n'
    )

    y = y - dimensions.w1 * general.factor - 0.5


def draw_reflected_piece_L(id_, dimensions):
    global x, y
    x1 = dimensions.l1 * general.factor
    x2 = dimensions.l2 * general.factor
    y1 = -dimensions.w1 * general.factor
    y2 = -dimensions.w2 * general.factor
    tex.write(
        '\\filldraw[color=black!150, fill=green!35, thin]'
        '(' + str(x) + ',' + str(y) + ') -- '
        '++(' + str(x1) + ',0) -- '
        '++(0,' + str(y1) + ') -- '
        '++(' + str(-x2) + ',0) -- '
        '++(0,' + str(y2 - y1) + ') -- '
        '++(' + str(x2 - x1) + ',0) -- '
        '++(0,' + str(-y2) + ') node [right, pos=0.5] {' + str(id_) + '};\n'
    )

    y = y - dimensions.w1 * general.factor - 0.5


def draw_piece_C_LL(pieceC):
    global x, y
    piece1_id = pieceC.combination.piece1_id
    piece2_id = pieceC.combination.piece2_id

    piece1 = general.pieces[piece1_id]
    piece2 = general.pieces[piece2_id]

    location = pieceC.combination.location

    if location == general.HORIZONTAL:
        aux_x = x
        aux_y = y
        
        # x += pieceC.dimensions.l*general.factor

        if pieceC.dimensions.w > piece1.dimensions.w1:
            y -= general.factor * piece1.dimensions.w2

        l1 = piece1.dimensions.l1
        l2 = piece1.dimensions.l2
        w1 = piece1.dimensions.w1
        w2 = piece1.dimensions.w2

        x1 = l1 * general.factor
        x2 = l2 * general.factor
        y1 = -w1 * general.factor
        y2 = -w2 * general.factor
        tex.write(
            '\\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x2) + ',0) -- '
            '++(0,' + str(y1 - y2) + ') -- '
            '++(' + str(x1 - x2) + ',0) -- '
            '++(0,' + str(y2) + ') -- '
            '++(' + str(-x1) + ',0) -- '
            '++(0,' + str(-y1) +
            ') node [right, pos=0.5] {' + str(piece1_id) + '};\n'
        )

        l1 = piece2.dimensions.l1
        l2 = piece2.dimensions.l2
        w1 = piece2.dimensions.w1
        w2 = piece2.dimensions.w2

        x += l2 * general.factor

        if pieceC.dimensions.w > piece1.dimensions.w1:
            y += (2 * piece1.dimensions.w2 - piece1.dimensions.w1) * general.factor

        x1 = l1 * general.factor
        x2 = l2 * general.factor
        y1 = -w1 * general.factor
        y2 = -w2 * general.factor
        tex.write(
            '\\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x1) + ',0) -- '
            '++(0,' + str(y1) + ') -- '
            '++(' + str(-x2) + ',0) -- '
            '++(0,' + str(y2 - y1) + ') -- '
            '++(' + str(x2 - x1) + ',0) -- '
            '++(0,' + str(-y2) +
            ') node [right, pos=0.5] {' + str(piece2_id) + '};\n'
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

        x1 = l1 * general.factor
        x2 = l2 * general.factor
        y1 = -w1 * general.factor
        y2 = -w2 * general.factor
        tex.write(
            '\\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x2) + ',0) -- '
            '++(0,' + str(y1 - y2) + ') -- '
            '++(' + str(x1 - x2) + ',0) -- '
            '++(0,' + str(y2) + ') -- '
            '++(' + str(-x1) + ',0) -- '
            '++(0,' + str(-y1) +
            ') node [right, pos=0.5] {' + str(piece1_id) + '};\n'
        )

        l1 = piece2.dimensions.l1
        l2 = piece2.dimensions.l2
        w1 = piece2.dimensions.w1
        w2 = piece2.dimensions.w2

        y += w2 * general.factor

        if pieceC.dimensions.l > piece1.dimensions.l1:
            x += (2 * piece1.dimensions.l2 - piece1.dimensions.l1) * general.factor

        x1 = l1 * general.factor
        x2 = l2 * general.factor
        y1 = -w1 * general.factor
        y2 = -w2 * general.factor
        tex.write(
            '\\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x1) + ',0) -- '
            '++(0,' + str(y1) + ') -- '
            '++(' + str(-x2) + ',0) -- '
            '++(0,' + str(y2 - y1) + ') -- '
            '++(' + str(x2 - x1) + ',0) -- '
            '++(0,' + str(-y2) +
            ') node [right, pos=0.5] {' + str(piece2_id) + '};\n'
        )
        x = aux_x
        y = aux_y

    #  y = aux_y

    y = y - pieceC.dimensions.w * general.factor - 0.5

def draw_piece_C_LR(pieceC):
    global x, y
    piece1_id = pieceC.combination.piece1_id
    piece2_id = pieceC.combination.piece2_id

    piece1 = general.pieces[piece1_id]
    piece2 = general.pieces[piece2_id]

    location = pieceC.combination.location

    y -= piece2.dimensions.w * general.factor

    # draw base piece, which is always a L piece

    l1 = piece1.dimensions.l1
    l2 = piece1.dimensions.l2
    w1 = piece1.dimensions.w1
    w2 = piece1.dimensions.w2

    x1 = l1 * general.factor
    x2 = l2 * general.factor
    y1 = -w1 * general.factor
    y2 = -w2 * general.factor
    tex.write(
        '\\filldraw[color=black!150, fill=green!35, thin]'
        '(' + str(x) + ',' + str(y) + ') -- '
        '++(' + str(x2) + ',0) -- '
        '++(0,' + str(y1 - y2) + ') -- '
        '++(' + str(x1 - x2) + ',0) -- '
        '++(0,' + str(y2) + ') -- '
        '++(' + str(-x1) + ',0) -- '
        '++(0,' + str(-y1) +
        ') node [right, pos=0.5] {' + str(piece1_id) + '};\n'
    )

    l = piece2.dimensions.l
    w = piece2.dimensions.w

    if location == general.HORIZONTAL:
        aux_x = x
        aux_y = y
        
        x += x2
        
        y -= ((w1 - w2) - w) * general.factor

        x1 = x + l * general.factor
        y1 = y - w * general.factor
        tex.write(
            '\\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') rectangle (' + str(x1) + ',' +
            str(y1) + ') node [right, pos=0.5] {' + str(piece2_id) + '};\n'
        )

    else:
        aux_x = x
        aux_y = y
        
        x = 0
        y += w * general.factor

        x1 = x + l * general.factor
        y1 = y - w * general.factor
        tex.write(
            '\\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') rectangle (' + str(x1) + ',' +
            str(y1) + ') node [right, pos=0.5] {' + str(piece2_id) + '};\n'
        )

    x = aux_x
    y = y - pieceC.dimensions.w * general.factor - 0.5

@logger.catch
def draw_pieces():
    logger.info("Desenhando peças")
    global x, y
    new_page = False

    if general.num_pieces_R > 0:
        tex.open_tikz()
        
        for _ in range(0, general.num_pieces_R):
            if new_page:
                tex.open_tikz()
                new_page = False
            
            piece_R = general.pieces_R[_]
            draw_piece_R(piece_R.id_, piece_R.dimensions)
            if abs(y) > 30:
                y = 0
                tex.close_tikz()
                tex.new_page()
                new_page = True
        
        if not new_page:
            tex.close_tikz()
            tex.new_page()

    if general.num_pieces_L > 0:
        tex.open_tikz()
        for _ in range(0, general.num_pieces_L):
            if new_page:
                tex.open_tikz()
                new_page = False
            piece_L = general.pieces_L[_]
            draw_piece_L(piece_L.id_, piece_L.dimensions)
            if abs(y) > 30:
                y = 0
                tex.close_tikz()
                tex.new_page()
                new_page = True
    
        if not new_page:
            tex.close_tikz()
            tex.new_page()
    
    if general.num_pieces_C:
        tex.open_tikz()
        for _ in range(0, general.num_pieces_C):
            if new_page:
                tex.open_tikz()
                new_page = False
            piece_C = general.pieces_C[_]
            if piece_C.combination.type_ == general.COMBINE_LL:
                draw_piece_C_LL(piece_C)
        
            elif piece_C.combination.type_ == general.COMBINE_LR:
                draw_piece_C_LR(piece_C)
            
            if abs(y) > 30:
                y = 0
                tex.close_tikz()
                tex.new_page()
                new_page = True

        if not new_page:
            tex.close_tikz()
            tex.new_page()
