# TCC - Geração de padrões de corte bidimensionais com itens regulares e irregulares do tipo L

Projeto final desenvolvido no último ano para obtenção do diploma no Curso de Bachalerado em Ciência da Computação pela Unesp de Bauru.

### Objetivo do projeto

Apresentar um método de resolução de problemas de corte bidimensional com itens regulares e irregulares do tipo L. 

A ideia é aplicar o método 2-estágios combinando itens regulares e irregulares (tipo L). A combinação tem como objetivo aumentar o conjunto de itens inicial do problema com novos itens que tem como característica a junção de dois itens. O intuito é que esses itens novos ajudem o método de 2-estágios a encontrar uma solução melhor em comparação a aplicação do método de 2-estágios sem os itens combinados. 

Para isso, foi desenvolvida uma ferramenta em *Python* com a implementação do método proposto. Além da resolução do problema de corte, a ferramenta também gera o desenho do padrão de corte em um arquivo PDF.

### Organização do repositório

O repositório está organizado da seguinte maneira:

```
├── code
│   ├── csp
│   ├── data
│   └── main.py
├── presentations
├── TCC Monografia Final.pdf
├── README.md
└── .gitignore
```

A pasta **code** armazena todo o código *Python* desenvolvido e arquivos relacionados, como a pasta **data** que possui exemplos de problemas de corte bidimensional para teste (há dois grupos de problemas, o grupo 1 possui problemas de corte bidimensional somente com peças retangulares; e o grupo 2, que possui problemas de corte bidimensional com peças retangulares e irregulares do tipo L. Na pasta **code** também fica o arquivo **main.py**, responsável por executar a solução desenvolvida.

A pasta **presentations** contém todas as apresentações criadas durante as disciplinas PIS I e PIS II (PIS é um acrônimo para Projeto de Implementação de Sistemas).

O arquivo **TCC Monografia Final.pdf** é a monografia final entregue no final do desenvolvimento do projeto e com as correções solicitadas pela banca.

### Dependências

Este projeto tem dependências a nível de sistema e de bibliotecas *Python*.

* Dependências de sistema:
  - IBM ILOG CPLEX
  - TeXLive (com pacote TikZ e programa pdflatex)

O **[IBM ILOG CPLEX](https://www.ibm.com/br-pt/products/ilog-cplex-optimization-studio)** é o *solver* utilizado para solucionar o problema de corte bidimensional e o **[TeXLive](https://www.tug.org/texlive/)** é utilizado para a geração do arquivo PDF através do LaTeX.

* Dependências do Python:
  - loguru
  - cplex

**[loguru](https://github.com/Delgan/loguru)** é uma biblioteca para geração de logs mais fácil e **[cplex](https://pypi.org/project/cplex/)** é uma API da IBM que possibilita chamadas ao CPLEX nos *scripts* desenvolvidos em *Python*.

### Utilização

Na pasta **code**, abra um terminal e execute o comando abaixo:

```
python main.py data/grupo1/gcut13
```

Este comando irá solucionar o problema *gcut13* que se encontra na pasta **data/grupo1** sem gerar a solução gráfica. Para acionar a solução gráfica, basta acrescentar o argumento `-d`.

```
python main.py data/grupo1/gcut13 -d
```

De forma automática é gerado um log do *script* no nível **INFO**. Para ver as mensagens de **DEBUG**, basta acresentar o argumento ``--debug``.

```
python main.py data/grupo1/gcut13 -d --debug
```

Outros argumentos podem ser encontrados atráves do comando *help*

```
python main.py --help

usage: main.py [-h] [-r] [-d] [-R] [--debug] [--factor FACTOR] input [output]

positional arguments:
  input             input file, BiL format
  output            output file, PDF format (default: output.pdf)

optional arguments:
  -h, --help        show this help message and exit
  -r, --rotate      rotate regular pieces
  -d, --draw        draw pieces and solution in PDF
  -R, --RESTRICTED  solve the problem as a restricted problem
  --debug           Give more output to help debugging.
  --factor FACTOR
```

### Autores

Kawe Antônio dos Santos Marcelino - :octocat: [Github](https://github.com/kaweantonio)
