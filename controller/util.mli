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
val dmove_of_masks : color -> mask -> mask -> dmove
val detect_promotion :
  position -> int * int * int * int -> position
val make_dmove : position list -> position -> dmove -> (position * position list)
val mask_of_position : position -> mask
val print_mask : mask -> unit
val parse_message : string -> mask option
