import subprocess as sp
import shlex

from loguru import logger

from csp.config import general

def preparation():
    general.doc = open(f'{general.output_filename}.tex', 'w+')
    write(
        "\\documentclass{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{tikz}\n"
        "\\usepackage{tikzscale}\n"
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
    logger.info("Gerando PDF")
    cmd = f'pdflatex {general.output_filename}.tex'

    sp.run(shlex.split(cmd), shell=False, stderr=sp.DEVNULL, stdout=sp.DEVNULL)

# def generate_pdf():
#   preparation()
#   open_tikz()
#   draw_pieces()
#   close_tkiz()
#   close_document()
