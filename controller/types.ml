type color = Black | White

type piece_type = King | Queen | Rook | Bishop | Knight | Pawn

type piece = piece_type * color

type field = Piece of piece | Empty

type can_castle = bool * bool

type board = field array array

type position = { ar: board;
                  turn: color;
                  cas_w : can_castle; cas_b : can_castle;
                  en_passant : int option;
                  prev : position option;
                  irr_change : int; (* number of moves since capture or pawn move *)
                  king_w : (int*int); king_b : (int * int); (* king positions are required often *)
                  number : int; (* position number, initial position is 0 *)
                  eval : int} (* essentially, memoized value of eval for this position *)

type mask = color option array array

type move = Move of int * int * int * int
          | Kingside_castle | Queenside_castle
          | Promotion of piece_type * int * int (* the int's are initial column and final column *)

type dmove =
  | DNoMove
  | DMove of int * int * int * int
  | DEnPassant of color * (int * int * int * int) * (int * int)
  | DKingside_castle
  | DQueenside_castle
  | DError

type smove =
  | GameOver of string
  | SuggestedMove of move

