import subprocess as sp
import shlex

from csp.config import general


def preparation():
    general.doc = open('output.tex', 'w+')
    write(
        "\\documentclass{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{tikz}\n"
        "\\usetikzlibrary{positioning}\n"
        "\\usepackage[a4paper]{geometry}"
        "\n\n\\begin{document}\n"
    )


def open_tikz():
    write('\\begin{tikzpicture}\n')


def close_tikz():
    write('\\end{tikzpicture}\n')


def new_page():
    write('\\newpage\n')


def close_document():
    write('\\end{document}')
    general.doc.close()


def write(message):
    general.doc.write(message)


def generate_pdf():
    cmd = 'pdflatex output.tex'

    sp.run(shlex.split(cmd), shell=False, stdout=sp.DEVNULL)

# def generate_pdf():
#   preparation()
#   open_tikz()
#   draw_pieces()
#   close_tkiz()
#   close_document()
