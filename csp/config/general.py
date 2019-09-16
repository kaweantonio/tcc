from collections import namedtuple
from dataclasses import dataclass, field
import itertools
from typing import Any

DEBUG = True

#   comb_location: str


@dataclass
class Piece:
    """
    A class to represent a piece.

    Holds all the data read and generated for each type of piece.

    '''

    Attributes
    ----------
    id_ : int
      a unique id generated dynamically
    type_ : int
      the type of the piece (REGULAR, IRREGULAR or COMBINED)
    dimensions : namedtuple
      a namedtuple containing the dimensions for each type of piece
      Each type have a specific group of fields:
        - type REGULAR or COMBINED - (l, w)
        - type IRREGULAR               - (l1, w1, l2, w2)
    b : int
      the maximum number the piece can appear in the pattern
    loss : int
      the loss produced by the piece in the pattern
    area : int
      the piece area
    rotated : bool
      define if the piece was rotated or not. ONLY APPLY TO REGULAR PIECES
    transformed : bool
      define if the piece was transformed or not. 
      ONLY APPLY TO IRREGULAR PIECES
    combination : namedtuple
      a namedtuple containing all the information related to COMBINED pieces
      ONLY USED BY COMBINED PIECES. The namedtuple will have the following fields:
      - piece1_id : int
        the id of one of the pieces used to create the COMBINED piece
      - piece2_id : int
        the same as piece1_id
      - type_ : int
        the type of combination (IRREGULAR with IRREGULAR or IRREGULAR with REGULAR)
      - location_ : int
        the local of the combination : VERTICAL or HORIZONTAL

    Methods
    -------
    __post_init()
      Set id and area attributes
    _calc_area()
      Calculate piece area based on piece type

    """
    id_: int = field(init=False)
    type_: int
    dimensions: Any
    area: int = field(init=False)
    b: int = 1
    loss: int = field(init=False)
    rotated: bool = False
    transformed: bool = False
    combination: Any = field(default=None)

    def __post_init__(self):
        self.id_ = next(id_iter)
        self.area = self._calc_area()
        self.loss = self._calc_loss()

    def _calc_area(self) -> int:
        if self.type_ == REGULAR:
            return self.dimensions.l * self.dimensions.w
        if self.type_ == COMBINED:
            return pieces[self.combination.piece1_id].area + pieces[self.combination.piece2_id].area

        return (self.dimensions.l1 * self.dimensions.w2) + ((self.dimensions.w1 - self.dimensions.w2) * self.dimensions.l2)

    def _calc_loss(self):
        if self.type_ == REGULAR:
            return 0

        if self.type_ == IRREGULAR:
            l, w = self.dimensions.l1, self.dimensions.w1
        else:
            l, w = self.dimensions.l, self.dimensions.w
        return (l * w) - self.area


# GLOBAL VARIABLES
ROTATE = False
REFLECT = True

IRREGULAR = 0
REGULAR = 1
COMBINED = 2

COMBINE_LL = 0
COMBINE_LR = 1

VERTICAL = True
HORIZONTAL = False

id_iter = itertools.count()

# plate information
NT_Plate = namedtuple("PlateNamedTuple", ["L", "W"])
plate = Any

Dimensions = namedtuple("Dimensions", ['l', 'w'])
Dimensions_IRREGULAR = namedtuple(
    "Dimensions_IRREGULAR", ['l1', 'w1', 'l2', 'w2'])
Combination = namedtuple(
    "Combination", ['piece1_id', 'piece2_id', 'type_', 'location'])

# total of all pieces and by type
num_pieces, num_pieces_R, num_pieces_L, num_pieces_C = 0, 0, 0, 0

# list of pieces by type
pieces_R, pieces_L, pieces_C = [], [], []

# list of all pieces
pieces = []

# holds the tex code to generate the pdf output
doc = None
