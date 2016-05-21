type color = Black | White
type piece_type = King | Queen | Rook | Bishop | Knight | Pawn
type piece = piece_type * color
type field = Piece of piece | Empty
type can_castle = bool * bool
type board = field array array
type position = {
  ar : board;
  turn : color;
  cas_w : can_castle;
  cas_b : can_castle;
  en_passant : int option;
  prev : position option;
  irr_change : int;
  king_w : int * int;
  king_b : int * int;
  number : int;
  eval : int;
}
type mask = color option array array
type move =
    Move of int * int * int * int
  | Kingside_castle
  | Queenside_castle
  | Promotion of piece_type * int * int
type dmove =
  | DNoMove
  | DMove of int * int * int * int
  | DEnPassant of color * (int * int * int * int) * (int * int)
  | DKingside_castle
  | DQueenside_castle
  | DUndo
  | DError
type smove =
  | GameOver of string
  | SuggestedMove of move
type input_message =
  | MASK of mask
  | OBST
  | NOCB
  | OTHER of string
type possible_states =
    { moves : move list;
      positions : position list;
      can_white : bool array array;
      can_black : bool array array;
      can_empty : bool array array;
      must_white : bool array array;
      must_black : bool array array;
      must_empty : bool array array; }

