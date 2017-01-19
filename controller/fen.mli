open Types

val long_string_of_smove : position -> smove -> string
val long_string_of_move : move -> position -> string
val piece_of_string : char -> piece
val print_fen : position -> unit

val fen_of_position : position -> string
val position_of_fen : string -> position

