open Types

val identical_positions : position -> position -> bool
val draw_by_repetition_aux : position -> position -> int -> bool
val draw_by_repetition : position -> bool
val draw_by_lack_of_progress : position -> bool
val draw : position -> bool
val opposite_color : color -> color
val color_sign : color -> int
val piece_chars : (piece_type * char) list
val char_of_piece_type : piece_type -> char
val rassoc : 'a -> ('b * 'a) list -> 'b
val piece_type_of_char : char -> piece_type
val int_of_letter : char -> int
val letter_of_int : int -> char
val print_board : field array array -> unit
val print_position : position -> unit
val init_position : position
val within_range : int -> bool
val within_range2 : int * int -> bool
val copy_matrix : 'a array array -> 'a array array
val no_k_castle : 'a * 'b -> 'a * bool
val no_q_castle : 'a * 'b -> bool * 'b
exception Illegal_move
val make_move : position -> move -> int -> position
val knight : (int * int) list
val rook : (int * int) list
val bishop : (int * int) list
val queen : (int * int) list
val pawn_white_mv : (int * int) list
val pawn_black_mv : (int * int) list
val pawn_white_cap : (int * int) list
val pawn_black_cap : (int * int) list
val add : int * int -> int * int -> int * int
val explore_direction :
  position ->
  int -> int -> int -> int -> int -> int -> int -> move list -> move list
val explore_directions :
  position -> int -> int -> (int * int) list -> int -> move list
val checked_direction :
  position ->
  color -> piece_type list -> int -> int -> int -> int -> int -> bool
val checked_directions :
  position ->
  color -> piece_type list -> int -> int -> (int * int) list -> int -> bool
val checked : position -> color -> int -> int -> bool
val find_king : position -> color -> (int * int) option
val king_checked : position -> color -> bool
val empty_segment : position -> int -> int -> int -> bool
val check_castle : position -> bool -> int -> int -> int -> int -> bool
val castle_moves : position -> move list
val possible_field_simple_moves : position -> int -> int -> move list
val possible_moves : position -> move list
val board_center : int array array
val mirror_y : color -> int -> int
val piece_value : piece_type -> int -> int -> color -> int
val field_value : position -> int -> int -> int
val win : int
val delta : position -> move -> int
exception Interrupt
val deadline : float option ref
val check_timer : unit -> unit
val set_timer : float -> unit
val del_timer : unit -> unit
exception Illegal_position
type best_move = Bad_moves | No_moves | Good of move
val alpha_beta : position -> int -> int -> int -> int * move option
val alpha_beta_search : position -> int -> int * move option
val legal_moves : position -> move list
val max_depth : int
val alpha_beta_deepening : position -> float -> int * move option
val previous : position -> position
val print_move : position -> move -> unit
val is_digit : char -> bool
val int_of_char : char -> int
val parse_move_string : string -> move option
val parse_move : position -> string -> move option
type game_status = Win of color | Draw | Play of move list
val game_status : position -> game_status
val best_move : position -> float -> move option

val suggest_move : position -> smove
val string_of_move : position -> smove -> string
val edwards_of_position : position -> string
val print_edwards : position -> unit
val full_suggestion : position -> string
val print_full_suggestion : position -> unit
    
type clock =
    Conventional of int * float
  | Incremental of float * float
  | Exact of float
val init_rem_time : clock -> float
val thinking_interval : int -> clock -> float -> float
val update_remaining : 'a -> clock -> float -> float -> float
type state = {
  pos : position;
  c : color;
  cl : clock;
  rem_time : float;
  gui : bool;
}
val parse_time : string -> float
val flush : unit -> unit
val parse_level : string -> string -> string -> clock
val main : unit -> unit

