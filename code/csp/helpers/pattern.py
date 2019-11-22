from copy import deepcopy as copy

from csp.config import general
from csp.helpers import tex


def draw_piece_R(piece, x, y):
    x1 = x + piece.dimensions.l * general.factor
    y1 = y + piece.dimensions.w * general.factor
    tex.write(
        ' \\filldraw[color=black!150, fill=green!35, thin]'
        '(' + str(x) + ',' + str(y) + ') rectangle (' + str(x1) +
        ',' + str(y1) + ');\n'
    )

def draw_piece_L(piece, x, y):
    
    x1 = piece.dimensions.l1 * general.factor
    x2 = piece.dimensions.l2 * general.factor
    y1 = -piece.dimensions.w1 * general.factor
    y2 = -piece.dimensions.w2 * general.factor
    tex.write(
        ' \\filldraw[color=black!150, fill=green!35, thin]'
        '(' + str(x) + ',' + str(y) + ') -- '
        '++(' + str(x2) + ',0) -- '
        '++(0,' + str(y1 - y2) + ') -- '
        '++(' + str(x1 - x2) + ',0) -- '
        '++(0,' + str(y2) + ') -- '
        '++(' + str(-x1) + ',0) -- '
        '++(0,' + str(-y1) + ');\n'
    )

def draw_piece_C_LL(pieceC, x, y):
    piece1 = general.pieces[pieceC.combination.piece1_id]
    piece2 = general.pieces[pieceC.combination.piece2_id]

    location = pieceC.combination.location

    if location == general.HORIZONTAL:
        aux_x = x
        aux_y = y
        # x += pieceC.l*general.factor

        if pieceC.dimensions.w > piece1.dimensions.w1:
            # y -= general.factor * piece1.dimensions.w2
            pass

        l1 = piece1.dimensions.l1
        l2 = piece1.dimensions.l2
        w1 = piece1.dimensions.w1
        w2 = piece1.dimensions.w2

        x1 = l1 * general.factor
        x2 = l2 * general.factor
        y1 = -w1 * general.factor
        y2 = -w2 * general.factor

        tex.write(
            ' \\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x2) + ',0) -- '
            '++(0,' + str(y1 - y2) + ') -- '
            '++(' + str(x1 - x2) + ',0) -- '
            '++(0,' + str(y2) + ') -- '
            '++(' + str(-x1) + ',0) -- '
            '++(0,' + str(-y1) +
            ');\n'
        )

        l1 = piece2.dimensions.l1
        l2 = piece2.dimensions.l2
        w1 = piece2.dimensions.w1
        w2 = piece2.dimensions.w2

        x += l2 * general.factor

        if pieceC.dimensions.w > piece1.dimensions.w1:
            # y += (2 * piece1.dimensions.w2 - piece1.dimensions.w1) * general.factor
            pass

        x1 = l1 * general.factor
        x2 = l2 * general.factor
        y1 = -w1 * general.factor
        y2 = -w2 * general.factor
        tex.write(
            ' \\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x1) + ',0) -- '
            '++(0,' + str(y1) + ') -- '
            '++(' + str(-x2) + ',0) -- '
            '++(0,' + str(y2 - y1) + ') -- '
            '++(' + str(x2 - x1) + ',0) -- '
            '++(0,' + str(-y2) +
            ');\n'
        )
        x = aux_x
    else:
        aux_x = x
        aux_y = y

        # y -= 0.5

        l1 = piece1.dimensions.l1
        l2 = piece1.dimensions.l2
        w1 = piece1.dimensions.w1
        w2 = piece1.dimensions.w2

        x1 = l1 * general.factor
        x2 = l2 * general.factor
        y1 = -w1 * general.factor
        y2 = -w2 * general.factor
        tex.write(
            ' \\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x2) + ',0) -- '
            '++(0,' + str(y1 - y2) + ') -- '
            '++(' + str(x1 - x2) + ',0) -- '
            '++(0,' + str(y2) + ') -- '
            '++(' + str(-x1) + ',0) -- '
            '++(0,' + str(-y1) +
            ');\n'
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
            ' \\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x1) + ',0) -- '
            '++(0,' + str(y1) + ') -- '
            '++(' + str(-x2) + ',0) -- '
            '++(0,' + str(y2 - y1) + ') -- '
            '++(' + str(x2 - x1) + ',0) -- '
            '++(0,' + str(-y2) +
            ');\n'
        )
        x = aux_x
        y = aux_y

def draw_piece_C_LR(pieceC, x, y):
    piece1_id = pieceC.combination.piece1_id
    piece2_id = pieceC.combination.piece2_id

    piece1 = general.pieces[piece1_id]
    piece2 = general.pieces[piece2_id]

    location = pieceC.combination.location

    # if location == general.VERTICAL:
    #     y -= piece2.dimensions.w * general.factor

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
        ');\n'
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
            str(y1) + ');\n'
        )

    else:
        aux_x = x
        aux_y = y
        
        y += w * general.factor

        x1 = x + l * general.factor
        y1 = y - w * general.factor
        tex.write(
            '\\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') rectangle (' + str(x1) + ',' +
            str(y1) + ');\n'
        )

    x = aux_x
    y = aux_y

def draw_plate(x, y):
    x1 = general.plate.L * general.factor
    y1 = general.plate.W * general.factor
    tex.write(
        '\\draw[color=black!150, fill=gray!35, thin]'
        '(' + str(x) + ',' + str(y) + ') rectangle (' +
        str(x1) + ',' + str(y1) + ');\n'
    )

    y = y1

def initial(piece_index, lost_area):
    # local x, y
    x = 0
    y = 0
    tex.new_page()
    tex.open_tikz()
    draw_plate(x, y)
    x = 0
    y = 0
    piece_type = general.pieces[piece_index].type_
    piece = copy(general.pieces[piece_index])

    if piece_type == general.REGULAR:
        n = general.plate.L // piece.dimensions.l
        m = general.plate.W // piece.dimensions.w
        for i in range(m):
            y = i * (piece.dimensions.w * general.factor)
            for j in range(n):
                x = j * (piece.dimensions.l * general.factor)
                draw_piece_R(piece, x, y)
    elif piece_type == general.IRREGULAR:
        n = general.plate.L // piece.dimensions.l1
        m = general.plate.W // piece.dimensions.w1
        aux1 = piece.dimensions.l1 * general.factor
        aux2 = piece.dimensions.w1 * general.factor
        for i in range(m):
            y = (i + 1) * aux2
            for j in range(n):
                x = j * aux1
                draw_piece_L(piece, x, y)
    else:
        n = general.plate.L // piece.dimensions.l
        m = general.plate.W // piece.dimensions.w
        # aux1 = general.pieces[piece.combination.piece1_id].dimensions.l1 * general.factor
        # aux2 = general.pieces[piece.combination.piece1_id].dimensions.w1 * general.factor
        # aux3 = general.pieces[piece.combination.piece2_id].dimensions.w2 * general.factor
        # for i in range(m):
        #     y = (i + 1) * aux2 + i * aux3
        #     for j in range(n):
        #         x = j * aux1
        #         draw_piece_C_LL(piece, x, y)

        for i in range(m):
            y = (i+1) * (piece.dimensions.w * general.factor)
            for j in range(n):
                x = j * (piece.dimensions.l * general.factor)
                if piece.combination.type_ == general.COMBINE_LL:
                    draw_piece_C_LL(piece, x, y)
                else:
                    draw_piece_C_LR(piece, x, y)

    tex.close_tikz()
    tex.new_page()

def restricted_initial(strips, strips_w):
    pieces = copy(general.pieces)
    # local x, y
    x = 0
    y = 0
    
    tex.new_page()
    tex.open_tikz()
    draw_plate(x, y)
    x = 0
    y = 0

    # print("restricted_initial {} {}".format(strips, strips_w))

    for i, strip in enumerate(strips):
        x = 0
        for piece_id in strip:
            piece = pieces[piece_id]

            if piece.type_ == general.REGULAR:
                l = piece.dimensions.l
                draw_piece_R(piece, x, y)
            elif piece.type_ == general.IRREGULAR:
                l = piece.dimensions.l1
                w = piece.dimensions.w1
                aux_y = y+(w * general.factor)
                draw_piece_L(piece, x, aux_y)

            x += l * general.factor

        y += strips_w[i] * general.factor
    
    tex.close_tikz()

def final(strips, strips_w, strips_pieces):
    pieces = copy(general.pieces)
    # local x, y
    x = 0
    y = 0
    
    tex.new_page()
    tex.open_tikz()
    draw_plate(x, y)

    y = 0

    for i, strip in enumerate(strips_pieces):
        x = 0
        for j, piece_id in enumerate(strip):
            num_piece_alocation = int(round(strips[i][j],1))
            if num_piece_alocation == 0:
                continue

            piece = pieces[piece_id]

            if piece.type_ == general.REGULAR:
                l = piece.dimensions.l
                aux_y = y
                draw_function = draw_piece_R
    
            elif piece.type_ == general.IRREGULAR:
                l = piece.dimensions.l1
                w = piece.dimensions.w1
                aux_y = y+(w * general.factor)
                draw_function = draw_piece_L
            else:
                l = piece.dimensions.l
                if piece.combination.type_ == general.COMBINE_LL:
                    w = pieces[piece.combination.piece1_id].dimensions.w1
                    aux_y = y+(w * general.factor)
                    draw_function = draw_piece_C_LL

                elif piece.combination.type_ == general.COMBINE_LR:
                    w = pieces[piece.combination.piece1_id].dimensions.w1
                    aux_y = y+(w * general.factor)
                    draw_function = draw_piece_C_LR

            for _ in range(num_piece_alocation):
                draw_function(piece, x, aux_y)
                x += l * general.factor

        y += strips_w[i] * general.factor
    
    tex.close_tikz()

