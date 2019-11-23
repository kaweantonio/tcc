import os
import sys
import argparse

from loguru import logger

from csp.config import general
from csp.helpers import tex, drawpiece, pattern
from csp.csp import cuttingStockProblem



def main(file_path):
    logger.remove()
    logger.add(sys.stderr, format="[<green>{time:YYYY-MM-DD   HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>] <level>{message}</level>", level="DEBUG" if general.DEBUG else "INFO", backtrace=True, diagnose=False)
    logger.info('Programa iniciado')

    if general.DRAW:
        logger.info('Preparando ambiente para desenho das peças e soluções')
        tex.preparation()

    problem = cuttingStockProblem(file_path)

    # if general.DRAW:
    #     drawpiece.draw_pieces()

    problem.get_solution()

    if general.DRAW:
        problem.print_initial_solution()
        problem.print_final_solution()

    # print(problem.solution, problem.solution_value, problem.solution_strips, problem.solution_strips_pieces, problem.solution_strips_w)

    if general.DRAW:
        tex.close_document()
        tex.generate_pdf()
    
    logger.info("Programa finalizado")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rotate', action='store_true', default=False, help='rotate regular pieces')
    parser.add_argument('-d', '--draw', action='store_true', default=False, help='draw pieces and solution in PDF')
    parser.add_argument('-R', '--RESTRICTED', action='store_true', default=False, help='solve the problem as a restricted problem')
    parser.add_argument('--debug', action='store_true', default=False, help='Give more output to help debugging.')
    parser.add_argument('--factor', action='store', type=float, default=0.01, help='Factor used to draw initial and final solution')
    parser.add_argument('input', help='input file, BiL format')
    parser.add_argument('output', help='output file, PDF format (default: output.pdf)', default="output.pdf", nargs='?')
    

    args = parser.parse_args()

    if args.rotate:
        general.ROTATE = True
    if args.draw:
        general.DRAW = True
    if args.RESTRICTED:
        general.RESTRICTED = True
    if args.debug:
        general.DEBUG = True

    general.factor = args.factor
    general.output_filename = args.output

    try:
        with open(args.input, 'r') as handle:
            pass
    except FileNotFoundError as msg:
        parser.error(msg)
    try:
        main(args.input)
    except Exception as error:
        logger.exception("Ocorreu um erro durante a execução do programa")
