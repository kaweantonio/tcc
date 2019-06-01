import config.common as common

x, y = 0, 0

def preparation():
  global doc
  doc = open('output.tex', 'w+')
  doc.write(
    "\\documentclass{article}\n" \
    "\\usepackage[utf8]{inputenc}\n" \
    "\\usepackage{tikz}\n" \
    "\\usepackage[a4paper]{geometry}" \
    "\n\n\\begin{document}\n"
  )

def open_tikz():
  global doc
  doc.write('\\begin{tikzpicture}\n')

def tikz_draw_peca_R(l, w):
  global doc
  global x,y
  x1 = x+l*.10
  y1 = y-w*.10
  doc.write('\\draw[color=black!150, fill=gray!35, thin]' \
            '('+str(x)+','+str(y)+') rectangle ('+str(x1)+','+str(y1)+');\n')

  y = y1 - 0.5

def tikz_draw_peca_L(l1, w1, l2, w2):
  global doc
  global x,y
  x1 = l1*.10
  x2 = l2*.10
  y1 = -w1*.10
  y2 = -w2*.10
  doc.write(
    '\\draw[color=black!150, fill=gray!35, thin]' \
    '('+str(x)+','+str(y)+') -- ' \
    '++('+str(x2)+',0) -- ' \
    '++(0,'+str(y1-y2)+') -- ' \
    '++('+str(x1-x2)+',0) -- ' \
    '++(0,'+str(y2)+') -- ' \
    '++('+str(-x1)+',0) -- ' \
    '++(0,'+str(-y1)+');\n'
  )

  y = y - w1*.10 - 0.5

def close_tkiz():
  global doc
  doc.write('\\end{tikzpicture}\n')

def close_document():
  doc.write('\\end{document}')
  doc.close()

def generate_pdf():
  preparation()
  open_tikz()

  for _ in range(0, common.N_pecas_R):
    peca_R = common.lista_pecas_R[_]
    l, w = peca_R.l, peca_R.w
    tikz_draw_peca_R(l,w)

  for _ in range(0, common.N_pecas_L):
    peca_L = common.lista_pecas_L[_]
    l1, w1, l2, w2 = peca_L.l1, peca_L.w1, peca_L.l2, peca_L.w2
    tikz_draw_peca_L(l1, w1, l2, w2)

  close_tkiz()
  close_document()  
