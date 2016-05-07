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
