open Types

val warning : string -> unit
val string_of_field : color -> field -> string
val string_of_position : position -> string
val mask_of_string : string -> mask
val diff_mask :
  mask ->
  mask -> ((int * int) * color option * color option) list
val consistent_line_and_color :
  int * int * int * int ->
  color * color * color * color -> bool
val chose_castle_side : int * int * int * int -> dmove
val dmove_of_masks : position -> mask -> mask -> dmove
val move_of_dmove : position -> dmove -> move option
val mask_of_position : position -> mask
val print_mask : mask -> unit
val print_diff : ((int * int) * color option * color option) list -> unit
val parse_message : string -> input_message
val possible_states_of_position : position -> possible_states
val mask_cleanup : possible_states -> mask -> mask -> mask
val make_move : position -> move -> position
