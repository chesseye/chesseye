type color = Black | White

type piece_type = King | Queen | Rook | Bishop | Knight | Pawn

type piece = piece_type * color

type field = Piece of piece | Empty

type can_castle = bool * bool

type position = { ar: field array array; 
                  turn: color; 
                  cas_w : can_castle; cas_b : can_castle; 
                  en_passant : int option; 
                  prev : position option; 
                  irr_change : int; (* number of moves since capture or pawn move *)
                  king_w : (int*int); king_b : (int * int); (* king positions are required often *)
                  number : int; (* position number, initial position is 0 *)
                  eval : int} (* essentially, memoized value of eval for this position *)


