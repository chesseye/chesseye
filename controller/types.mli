type color = Black | White
type piece_type = King | Queen | Rook | Bishop | Knight | Pawn
type piece = piece_type * color
type field = Piece of piece | Empty
type can_castle = bool * bool
type position = {
  ar : field array array;
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
