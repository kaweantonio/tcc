import config.common as common
import subprocess as sp
from draw.draw_pieces import draw_pieces

def preparation():
  common.doc = open('output.tex', 'w+')
  common.doc.write(
    "\\documentclass{article}\n" \
    "\\usepackage[utf8]{inputenc}\n" \
    "\\usepackage{tikz}\n" \
    "\\usetikzlibrary{positioning}\n" \
    "\\usepackage[a4paper]{geometry}" \
    "\n\n\\begin{document}\n"
  )

def open_tikz():
  common.doc.write('\\begin{tikzpicture}\n')

def close_tikz():
  common.doc.write('\\end{tikzpicture}\n')

def new_page():
  common.doc.write('\\newpage\n')

def close_document():
  common.doc.write('\\end{document}')
  common.doc.close()

def generate_pdf():
  sp.run('pdflatex output.tex', shell=True)

# def generate_pdf():
#   preparation()
#   open_tikz()
#   draw_pieces()
#   close_tkiz()
#   close_document()

