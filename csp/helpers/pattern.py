from copy import deepcopy as copy

from csp.config import general
from csp.helpers import tex


def draw_piece_R(dimensions, id_, x, y):
    x1 = x + dimensions.l * .10
    y1 = y + dimensions.w * .10
    tex.write(
        ' \\filldraw[color=black!150, fill=green!35, thin]'
        '(' + str(x) + ',' + str(y) + ') rectangle (' + str(x1) +
        ',' + str(y1) + ') node [pos=.5] {' + str(id_) + '};\n'
    )


def draw_piece_L(dimensions, id_, x, y):
    x1 = dimensions.l1 * .10
    x2 = dimensions.l2 * .10
    y1 = -dimensions.w1 * .10
    y2 = -dimensions.w2 * .10
    tex.write(
        ' \\filldraw[color=black!150, fill=green!35, thin]'
        '(' + str(x) + ',' + str(y) + ') -- '
        '++(' + str(x2) + ',0) -- '
        '++(0,' + str(y1 - y2) + ') -- '
        '++(' + str(x1 - x2) + ',0) -- '
        '++(0,' + str(y2) + ') -- '
        '++(' + str(-x1) + ',0) -- '
        '++(0,' + str(-y1) + ') node [right, pos=0.5] {' + str(id_) + '};\n'
    )


def draw_piece_C(pieceC, x, y):
    piece1 = general.pieces[pieceC.combination.piece1_id]
    piece2 = general.pieces[pieceC.combination.piece2_id]

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

        x1 = l1 * .10
        x2 = l2 * .10
        y1 = -w1 * .10
        y2 = -w2 * .10

        tex.write(
            ' \\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x2) + ',0) -- '
            '++(0,' + str(y1 - y2) + ') -- '
            '++(' + str(x1 - x2) + ',0) -- '
            '++(0,' + str(y2) + ') -- '
            '++(' + str(-x1) + ',0) -- '
            '++(0,' + str(-y1) +
            ') node [right, pos=0.5] {' +
            str(pieceC.combination.piece1_id) + '};\n'
        )

        l1 = piece2.dimensions.l1
        l2 = piece2.dimensions.l2
        w1 = piece2.dimensions.w1
        w2 = piece2.dimensions.w2

        x += l2 * 0.10

        if pieceC.dimensions.w > piece1.dimensions.w1:
            y += (2 * piece1.dimensions.w2 - piece1.dimensions.w1) * 0.10

        x1 = l1 * .10
        x2 = l2 * .10
        y1 = -w1 * .10
        y2 = -w2 * .10
        tex.write(
            ' \\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x1) + ',0) -- '
            '++(0,' + str(y1) + ') -- '
            '++(' + str(-x2) + ',0) -- '
            '++(0,' + str(y2 - y1) + ') -- '
            '++(' + str(x2 - x1) + ',0) -- '
            '++(0,' + str(-y2) +
            ') node [right, pos=0.5] {' +
            str(pieceC.combination.piece2_id) + '};\n'
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

        x1 = l1 * .10
        x2 = l2 * .10
        y1 = -w1 * .10
        y2 = -w2 * .10
        tex.write(
            ' \\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x2) + ',0) -- '
            '++(0,' + str(y1 - y2) + ') -- '
            '++(' + str(x1 - x2) + ',0) -- '
            '++(0,' + str(y2) + ') -- '
            '++(' + str(-x1) + ',0) -- '
            '++(0,' + str(-y1) +
            ') node [right, pos=0.5] {' +
            str(pieceC.combination.piece1_id) + '};\n'
        )

        l1 = piece2.dimensions.l1
        l2 = piece2.dimensions.l2
        w1 = piece2.dimensions.w1
        w2 = piece2.dimensions.w2

        y += w2 * 0.10

        if pieceC.dimensions.l > piece1.dimensions.l1:
            x += (2 * piece1.dimensions.l2 - piece1.dimensions.l1) * 0.10

        x1 = l1 * .10
        x2 = l2 * .10
        y1 = -w1 * .10
        y2 = -w2 * .10
        tex.write(
            ' \\filldraw[color=black!150, fill=green!35, thin]'
            '(' + str(x) + ',' + str(y) + ') -- '
            '++(' + str(x1) + ',0) -- '
            '++(0,' + str(y1) + ') -- '
            '++(' + str(-x2) + ',0) -- '
            '++(0,' + str(y2 - y1) + ') -- '
            '++(' + str(x2 - x1) + ',0) -- '
            '++(0,' + str(-y2) +
            ') node [right, pos=0.5] {' +
            str(pieceC.combination.piece2_id) + '};\n'
        )
        x = aux_x
        y = aux_y


def draw_plate(x, y):
    x1 = general.plate.L * .10
    y1 = general.plate.W * .10

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

    tex.open_tikz()
    draw_plate(x, y)
    piece_type = general.pieces[piece_index].type_
    piece = copy(general.pieces[piece_index])

    if piece_type == general.REGULAR:
        n = general.plate.L // piece.dimensions.l
        m = general.plate.W // piece.dimensions.w
        for i in range(m):
            y = i * (piece.dimensions.w * .10)
            for j in range(n):
                x = j * (piece.dimensions.l * .10)
                draw_piece_R(piece.dimensions, piece.id_, x, y)
    elif piece_type == general.IRREGULAR:
        n = general.plate.L // piece.dimensions.l1
        m = general.plate.W // piece.dimensions.w1
        aux1 = piece.dimensions.l1 * .10
        aux2 = piece.dimensions.w1 * .10
        for i in range(m):
            y = (i + 1) * aux2
            for j in range(n):
                x = j * aux1
                draw_piece_L(piece.dimensions, piece.id_, x, y)
    else:
        n = general.plate.L // piece.dimensions.l
        m = general.plate.W // piece.dimensions.w
        aux1 = general.pieces[piece.combination.piece1_id].dimensions.l1 * .10
        aux2 = general.pieces[piece.combination.piece1_id].dimensions.w1 * .10
        aux3 = general.pieces[piece.combination.piece2_id].dimensions.w2 * .10
        for i in range(m):
            y = (i + 1) * aux2 + i * aux3
            for j in range(n):
                x = j * aux1
                draw_piece_C(piece, x, y)

    tex.close_tikz()
